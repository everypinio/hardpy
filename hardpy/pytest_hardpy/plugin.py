# Copyright (c) 2024 Everypin
# GNU General Public License v3.0 (see LICENSE or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import annotations

import signal
from logging import getLogger
from pathlib import Path, PurePath
from platform import system
from re import compile as re_compile
from time import sleep
from typing import Any, Callable

from _pytest._code.code import (
    ExceptionInfo,
    ExceptionRepr,
    ReprExceptionInfo,
    ReprFileLocation,
    TerminalRepr,
)
from natsort import natsorted
from pytest import (
    CallInfo,
    Config,
    ExitCode,
    Item,
    Parser,
    Session,
    TestReport,
    exit,  # noqa: A004
    fixture,
    skip,
)

from hardpy.common.stand_cloud.connector import StandCloudConnector, StandCloudError
from hardpy.pytest_hardpy.reporter import HookReporter
from hardpy.pytest_hardpy.utils import (
    ConnectionData,
    NodeInfo,
    ProgressCalculator,
    TestStatus,
)
from hardpy.pytest_hardpy.utils.node_info import TestDependencyInfo

if __debug__:
    from urllib3 import disable_warnings
    from urllib3.exceptions import InsecureRequestWarning

    disable_warnings(InsecureRequestWarning)

def pytest_addoption(parser: Parser) -> None:
    """Register argparse-style options."""
    con_data = ConnectionData()
    parser.addoption(
        "--hardpy-db-url",
        action="store",
        default=con_data.database_url,
        help="database url",
    )
    parser.addoption(
        "--hardpy-sp",
        action="store",
        default=con_data.socket_port,
        help="internal socket port",
    )
    parser.addoption(
        "--hardpy-sh",
        action="store",
        default=con_data.socket_host,
        help="internal socket host",
    )
    parser.addoption(
        "--hardpy-clear-database",
        action="store_true",
        default=False,
        help="clear hardpy local database",
    )
    parser.addoption(
        "--hardpy-pt",
        action="store_true",
        default=False,
        help="enable pytest-hardpy plugin",
    )
    parser.addoption(
        "--sc-address",
        action="store",
        default=con_data.sc_address,
        help="StandCloud address",
    )
    parser.addoption(
        "--sc-connection-only",
        action="store_true",
        default=con_data.sc_connection_only,
        help="check StandCloud availability",
    )


# Bootstrapping hooks
def pytest_load_initial_conftests(
    early_config: Config,
    parser: Parser,  # noqa: ARG001
    args: Any,  # noqa: ANN401
) -> None:
    """Load initial conftests."""
    if "--hardpy-pt" in args:
        plugin = HardpyPlugin()
        early_config.pluginmanager.register(plugin)


class HardpyPlugin:
    """HardPy integration plugin for pytest.

    Extends hook functions from pytest API.
    """

    def __init__(self) -> None:
        self._progress = ProgressCalculator()
        self._results = {}
        self._post_run_functions: list[Callable] = []
        self._dependencies = {}

        if system() == "Linux":
            signal.signal(signal.SIGTERM, self._stop_handler)
        elif system() == "Windows":
            signal.signal(signal.SIGBREAK, self._stop_handler)  # type: ignore
        self._log = getLogger(__name__)

    # Initialization hooks

    def pytest_configure(self, config: Config) -> None:
        """Configure pytest."""
        con_data = ConnectionData()

        database_url = config.getoption("--hardpy-db-url")
        if database_url:
            con_data.database_url = str(database_url)  # type: ignore

        is_clear_database = config.getoption("--hardpy-clear-database")

        socket_port = config.getoption("--hardpy-sp")
        if socket_port:
            con_data.socket_port = int(socket_port)  # type: ignore

        socket_host = config.getoption("--hardpy-sh")
        if socket_host:
            con_data.socket_host = str(socket_host)  # type: ignore

        sc_address = config.getoption("--sc-address")
        if sc_address:
            con_data.sc_address = str(sc_address)  # type: ignore

        sc_connection_only = config.getoption("--sc-connection-only")
        if sc_connection_only:
            con_data.sc_connection_only = bool(sc_connection_only)  # type: ignore

        config.addinivalue_line("markers", "case_name")
        config.addinivalue_line("markers", "module_name")
        config.addinivalue_line("markers", "dependency")
        config.addinivalue_line("markers", "attempt")

        # must be init after config data is set
        try:
            self._reporter = HookReporter(bool(is_clear_database))
        except RuntimeError as exc:
            exit(str(exc), 1)

    def pytest_sessionfinish(self, session: Session, exitstatus: int) -> None:
        """Call at the end of test session."""
        if "--collect-only" in session.config.invocation_params.args:
            return
        status = self._get_run_status(exitstatus)
        self._reporter.finish(status)
        self._reporter.update_db_by_doc()
        self._reporter.compact_all()

        # call post run methods
        if self._post_run_functions:
            for action in self._post_run_functions:
                action()

    # Collection hooks

    def pytest_collection_modifyitems(
        self,
        session: Session,
        config: Config,
        items: list[Item],  # noqa: ARG002
    ) -> None:
        """Call after collection phase."""
        self._reporter.init_doc(str(PurePath(config.rootpath).name))

        nodes = {}
        modules = set()

        session.items = natsorted(
            session.items,
            key=lambda x: x.parent.name if x.parent is not None else x.name,
        )
        for item in session.items:
            if item.parent is None:
                continue
            try:
                node_info = NodeInfo(item)
            except ValueError as exc:
                error_msg = f"Error creating NodeInfo for item: {item}. {exc}"
                exit(error_msg, 1)

            self._init_case_result(node_info.module_id, node_info.case_id)
            if node_info.module_id not in nodes:
                nodes[node_info.module_id] = [node_info.case_id]
            else:
                nodes[node_info.module_id].append(node_info.case_id)

            self._reporter.add_case(node_info)

            self._add_dependency(node_info, nodes)
            modules.add(node_info.module_id)
        for module_id in modules:
            self._reporter.set_module_status(module_id, TestStatus.READY)
        self._reporter.update_node_order(nodes)
        self._reporter.update_db_by_doc()

    # Test running (runtest) hooks

    def pytest_runtestloop(self, session: Session) -> bool | None:
        """Call at the start of test run."""
        self._progress.set_test_amount(session.testscollected)
        if session.config.option.collectonly:
            # ignore collect only mode
            return True

        con_data = ConnectionData()

        if con_data.sc_connection_only:  # check
            try:
                sc_connector = StandCloudConnector(addr=con_data.sc_address)
            except StandCloudError as exc:
                msg = str(exc)
                self._reporter.set_alert(msg)
                exit(msg)
            try:
                sc_connector.healthcheck()
            except Exception:  # noqa: BLE001
                addr = con_data.sc_address
                msg = (
                    f"StandCloud service at the address {addr} "
                    "not available or HardPy user is not authorized"
                )
                self._reporter.set_alert(msg)
                self._reporter.update_db_by_doc()
                exit(msg)

        # testrun entrypoint
        self._reporter.start()
        self._reporter.update_db_by_doc()
        return None

    def pytest_runtest_setup(self, item: Item) -> None:
        """Call before each test setup phase."""
        if item.parent is None:
            self._log.error(f"Test module name for test {item.name} not found.")
            return

        node_info = NodeInfo(item)

        status = TestStatus.RUN
        is_skip_test = self._is_skip_test(node_info)
        if not is_skip_test:
            self._reporter.set_module_start_time(node_info.module_id)
            self._reporter.set_case_start_time(node_info.module_id, node_info.case_id)
        else:
            status = TestStatus.SKIPPED
            self._results[node_info.module_id][node_info.case_id] = status
            progress = self._progress.calculate(item.nodeid)
            self._reporter.set_progress(progress)

        self._reporter.set_module_status(node_info.module_id, status)
        self._reporter.set_case_status(node_info.module_id, node_info.case_id, status)
        self._reporter.update_db_by_doc()

        if is_skip_test:
            skip(f"Test {item.nodeid} is skipped")

    def pytest_runtest_call(self, item: Item) -> None:
        """Call the test item."""
        node_info = NodeInfo(item)
        self._reporter.set_case_attempt(
            node_info.module_id,
            node_info.case_id,
            1,
        )
        self._reporter.update_db_by_doc()

    def pytest_runtest_makereport(self, item: Item, call: CallInfo) -> None:
        """Call after call of each test item."""
        if call.when != "call" or not call.excinfo:
            return

        node_info = NodeInfo(item)
        attempt = node_info.attempt
        module_id = node_info.module_id
        case_id = node_info.case_id

        # first attempt was in pytest_runtest_call
        for current_attempt in range(2, attempt + 1):
            # add pause between attempts to verify STOP condition
            sleep(1)

            self._reporter.set_module_status(module_id, TestStatus.RUN)
            self._reporter.set_case_status(module_id, case_id, TestStatus.RUN)
            self._reporter.set_case_attempt(module_id, case_id, current_attempt)
            self._reporter.update_db_by_doc()

            try:
                item.runtest()
                call.excinfo = None
                self._reporter.set_case_status(module_id, case_id, TestStatus.PASSED)
                break
            except AssertionError:
                self._reporter.set_case_status(module_id, case_id, TestStatus.FAILED)
                if current_attempt == attempt:
                    return

    # Reporting hooks

    def pytest_runtest_logreport(self, report: TestReport) -> bool | None:
        """Call after call of each test item."""
        if report.when != "call" and report.failed is False:
            # ignore setup and teardown phase or continue processing setup
            # and teardown failure (fixture exception handler)
            return True

        module_id = Path(report.fspath).stem
        case_id = report.nodeid.rpartition("::")[2]

        self._reporter.set_case_status(
            module_id,
            case_id,
            TestStatus(report.outcome),
        )
        self._reporter.set_case_stop_time(
            module_id,
            case_id,
        )

        assertion_msg = self._decode_assertion_msg(report.longrepr)
        self._reporter.set_assertion_msg(module_id, case_id, assertion_msg)
        self._reporter.set_progress(self._progress.calculate(report.nodeid))
        self._results[module_id][case_id] = report.outcome

        if None not in self._results[module_id].values():
            self._collect_module_result(module_id)
        self._reporter.update_db_by_doc()
        return None

    # Fixture

    @fixture(scope="session")
    def post_run_functions(self) -> list[Callable]:
        """Get post run methods list.

        Fill this list in conftest.py and functions from this
        list will be called after tests running (in the end of pytest_sessionfinish).

        Returns:
            list[Callable]: list of post run methods
        """
        return self._post_run_functions

    # Not hooks

    def _stop_handler(self, signum: int, frame: Any) -> None:  # noqa: ANN401, ARG002
        exit("Tests stopped by user")

    def _init_case_result(self, module_id: str, case_id: str) -> None:
        if self._results.get(module_id) is None:
            self._results[module_id] = {
                "module_status": TestStatus.READY,
                case_id: None,
            }
        else:
            self._results[module_id][case_id] = None

    def _collect_module_result(self, module_id: str) -> None:
        if (
            TestStatus.FAILED in self._results[module_id].values()
            or TestStatus.ERROR in self._results[module_id].values()
        ):
            status = TestStatus.FAILED
        elif TestStatus.SKIPPED in self._results[module_id].values():
            status = TestStatus.SKIPPED
        else:
            status = TestStatus.PASSED
        self._results[module_id]["module_status"] = status
        self._reporter.set_module_status(module_id, status)
        self._reporter.set_module_stop_time(module_id)

    def _get_run_status(self, exitstatus: int) -> TestStatus:
        match exitstatus:
            case ExitCode.OK:
                return TestStatus.PASSED
            case ExitCode.TESTS_FAILED:
                return TestStatus.FAILED
            case ExitCode.INTERRUPTED:
                self._stop_tests()
                return TestStatus.STOPPED
            case _:
                return TestStatus.FAILED

    def _stop_tests(self) -> None:
        """Update module and case statuses from READY or RUN to STOPPED."""
        for module_id, module_data in self._results.items():
            module_status = module_data["module_status"]

            # skip not ready and running modules
            if module_status not in {TestStatus.READY, TestStatus.RUN}:
                continue

            # update module statuses
            self._results[module_id]["module_status"] = TestStatus.STOPPED
            self._reporter.set_module_status(module_id, TestStatus.STOPPED)

            # update case statuses
            for module_key, module_value in module_data.items():
                # module status is not a case_id
                if module_key == "module_status":
                    continue
                # case value is empty - case is not finished
                if module_value is None:
                    case_id = module_key
                    self._results[module_id][case_id] = TestStatus.STOPPED
                    self._reporter.set_case_status(
                        module_id,
                        case_id,
                        TestStatus.STOPPED,
                    )
        self._reporter.update_db_by_doc()

    def _decode_assertion_msg(
        self,
        error: (
            ExceptionInfo[BaseException]
            | tuple[str, int, str]
            | str
            | TerminalRepr
            | None
        ),
    ) -> str | None:
        """Parse pytest assertion error message."""
        if error is None:
            return None

        match error:
            case str():
                return error
            case tuple() if len(error) == 3:  # noqa: PLR2004
                return error[2]
            case ExceptionInfo():
                error_repr = error.getrepr()
                if isinstance(error_repr, ReprExceptionInfo) and error_repr.reprcrash:
                    return error_repr.reprcrash.message
                return None
            case TerminalRepr():
                if isinstance(error, ExceptionRepr) and isinstance(
                    error.reprcrash,
                    ReprFileLocation,
                ):
                    # remove ansi codes
                    ansi_pattern = re_compile(
                        r"(?:\x1B[@-Z\\-_]|[\x80-\x9A\x9C-\x9F]|(?:\x1B\[|\x9B)[0-?]*[ -/]*[@-~])",  # noqa: E501
                    )
                    return ansi_pattern.sub("", error.reprcrash.message)
                return str(error)
            case _:
                return None

    def _is_skip_test(self, node_info: NodeInfo) -> bool:
        """Is need to skip a test because it depends on another test."""
        is_dependency_test_exist = self._dependencies.get(
            TestDependencyInfo(node_info.module_id, node_info.case_id),
        )
        is_dependency_test_failed = False
        if is_dependency_test_exist:
            wrong_status = {TestStatus.FAILED, TestStatus.SKIPPED, TestStatus.ERROR}
            module_id, case_id = is_dependency_test_exist
            if case_id is not None:
                is_dependency_test_failed = (
                    self._results[module_id][case_id] in wrong_status
                )
            else:
                result_set = set(self._results[module_id].values())
                is_dependency_test_failed = any(
                    status in wrong_status for status in result_set
                )
        return bool(is_dependency_test_exist and is_dependency_test_failed)

    def _add_dependency(self, node_info: NodeInfo, nodes: dict) -> None:
        dependency = node_info.dependency
        if dependency is None or dependency == "":
            return
        module_id, case_id = dependency
        if module_id not in nodes:
            error_message = f"Error: Module dependency '{dependency}' not found."
            exit(error_message, 1)
        elif case_id not in nodes[module_id] and case_id is not None:
            error_message = f"Error: Case dependency '{dependency}' not found."
            exit(error_message, 1)

        self._dependencies[
            TestDependencyInfo(node_info.module_id, node_info.case_id)
        ] = dependency
