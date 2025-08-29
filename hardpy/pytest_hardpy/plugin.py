# Copyright (c) 2024 Everypin
# GNU General Public License v3.0 (see LICENSE or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import annotations

import copy
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
        "--hardpy-tests-name",
        action="store",
        help="HardPy tests suite name",
    )
    # TODO (xorialexandrov): Remove --hardpy-sp and --hardpy-sh in HardPy major version.
    # Addoptions left for compatibility with version 0.10.1 and below
    parser.addoption(
        "--hardpy-sp",
        action="store",
        help="DEPRECATED, UNUSED: internal socket port",
    )
    parser.addoption(
        "--hardpy-sh",
        action="store",
        help="DEPRECATED, UNUSED: internal socket host",
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
    parser.addoption(
        "--hardpy-start-arg",
        action="append",
        default=[],
        help="Dynamic arguments for test execution (key=value format)",
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
        self._tests_name: str = ""
        self._is_critical_not_passed = False
        self._start_args = {}

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

        tests_name = config.getoption("--hardpy-tests-name")
        if tests_name:
            self._tests_name = str(tests_name)
        else:
            self._tests_name = str(PurePath(config.rootpath).name)

        is_clear_database = config.getoption("--hardpy-clear-database")

        sc_address = config.getoption("--sc-address")
        if sc_address:
            con_data.sc_address = str(sc_address)  # type: ignore

        sc_connection_only = config.getoption("--sc-connection-only")
        if sc_connection_only:
            con_data.sc_connection_only = bool(sc_connection_only)  # type: ignore

        _args = config.getoption("--hardpy-start-arg") or []
        if _args:
            self._start_args = dict(arg.split("=", 1) for arg in _args if "=" in arg)

        config.addinivalue_line("markers", "case_name")
        config.addinivalue_line("markers", "module_name")
        config.addinivalue_line("markers", "dependency")
        config.addinivalue_line("markers", "attempt")
        config.addinivalue_line("markers", "critical")
        config.addinivalue_line("markers", "case_group")
        config.addinivalue_line("markers", "module_group")

        # must be init after config data is set
        try:
            self._reporter = HookReporter(bool(is_clear_database))
        except RuntimeError as exc:
            exit(str(exc), ExitCode.INTERNAL_ERROR)

    def pytest_sessionfinish(self, session: Session, exitstatus: int) -> None:
        """Call at the end of test session."""
        if "--collect-only" in session.config.invocation_params.args:
            return
        status = self._get_run_status(exitstatus)
        if status == TestStatus.STOPPED:
            self._stop_tests()
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
        config: Config,  # noqa: ARG002
        items: list[Item],  # noqa: ARG002
    ) -> None:
        """Call after collection phase."""
        self._reporter.init_doc(self._tests_name)

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
                exit(error_msg, ExitCode.NO_TESTS_COLLECTED)

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

        # running tests depends on a connection to StandCloud
        if con_data.sc_connection_only:
            try:
                sc_connector = StandCloudConnector(addr=con_data.sc_address)
            except StandCloudError as exc:
                msg = str(exc)
                self._reporter.set_alert(msg)
                exit(msg, ExitCode.INTERNAL_ERROR)
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
                exit(msg, ExitCode.INTERNAL_ERROR)

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
        is_skip_test = self._is_critical_not_passed or self._is_skip_test(node_info)
        self._reporter.set_module_start_time(node_info.module_id)
        if not is_skip_test:
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
        self._reporter.set_case_attempt(node_info.module_id, node_info.case_id, 1)
        self._reporter.update_db_by_doc()

    def pytest_runtest_makereport(self, item: Item, call: CallInfo) -> None:
        """Call after call of each test item."""
        if call.when != "call" or not call.excinfo:
            return

        # failure item
        node_info = NodeInfo(item)
        attempt = node_info.attempt
        module_id = node_info.module_id
        case_id = node_info.case_id
        casusd_dut_failure_id = self._reporter.get_caused_dut_failure_id()
        is_dut_failure = True

        if node_info.critical:
            self._is_critical_not_passed = True

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
                self._is_critical_not_passed = False
                is_dut_failure = False
                self._reporter.set_case_status(module_id, case_id, TestStatus.PASSED)
                break
            except AssertionError:
                self._reporter.set_case_status(module_id, case_id, TestStatus.FAILED)
                is_dut_failure = True
                if current_attempt == attempt:
                    break

        if is_dut_failure and casusd_dut_failure_id is None:
            self._reporter.set_caused_dut_failure_id(module_id, case_id)

    # Reporting hooks

    def pytest_runtest_logreport(self, report: TestReport) -> bool | None:
        """Call after call of each test item."""
        is_skipped_by_plugin: bool = False
        if report.when == "setup" and report.skipped is True:
            # plugin-skipped tests should not have start and stop times
            is_skipped_by_plugin = True
        elif report.when != "call" and report.failed is False:
            # ignore setup and teardown phase or continue processing setup
            # and teardown failure (fixture exception handler)
            return True

        module_id = Path(report.fspath).stem
        case_id = report.nodeid.rpartition("::")[2]

        self._reporter.set_case_status(module_id, case_id, TestStatus(report.outcome))
        # update case stop_time in non-skipped tests or user-skipped tests
        if report.skipped is False or is_skipped_by_plugin is False:
            self._reporter.set_case_stop_time(module_id, case_id)

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

    @fixture(scope="session")
    def hardpy_start_args(self) -> dict:
        """Get HardPy start arguments.

        Returns:
            dict: Parsed start arguments (key-value pairs)
        """
        return copy.deepcopy(self._start_args)

    # Not hooks

    def _stop_handler(self, signum: int, frame: Any) -> None:  # noqa: ANN401, ARG002
        exit("Tests stopped by user", ExitCode.INTERRUPTED)

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
                return TestStatus.STOPPED
            case _:
                return TestStatus.FAILED

    def _stop_tests(self) -> None:
        """Update module and case statuses to stopped and skipped."""
        is_module_stopped = False
        is_case_stopped = False
        valid_statuses = {TestStatus.PASSED, TestStatus.FAILED, TestStatus.SKIPPED}
        for module_id, module_data in self._results.items():
            module_status = self._reporter.get_module_status(module_id)
            if module_status in valid_statuses:
                continue

            is_module_stopped = self._stop_module(module_id, is_module_stopped)
            for module_data_key in module_data:
                # skip module status
                if module_data_key == "module_status":
                    continue
                case_id = module_data_key
                case_status = self._reporter.get_case_status(module_id, case_id)
                if case_status in valid_statuses:
                    continue
                is_case_stopped = self._stop_case(module_id, case_id, is_case_stopped)

        self._reporter.update_db_by_doc()

    def _stop_module(self, module_id: str, is_module_stopped: bool) -> bool:
        # stopped status is set only once other statuses are skipped
        if is_module_stopped is False:
            module_status = TestStatus.STOPPED
            is_module_stopped = True
            if not self._reporter.get_module_start_time(module_id):
                self._reporter.set_module_start_time(module_id)
            self._reporter.set_module_stop_time(module_id)
        else:
            module_status = TestStatus.SKIPPED
        self._results[module_id]["module_status"] = module_status
        self._reporter.set_module_status(module_id, module_status)
        return is_module_stopped

    def _stop_case(self, module_id: str, case_id: str, is_case_stopped: bool) -> bool:
        # stopped status is set only once other statuses are skipped
        if is_case_stopped is False:
            case_status = TestStatus.STOPPED
            is_case_stopped = True
            if not self._reporter.get_case_start_time(module_id, case_id):
                self._reporter.set_case_start_time(module_id, case_id)
            self._reporter.set_case_stop_time(module_id, case_id)
        else:
            case_status = TestStatus.SKIPPED
        self._results[module_id][case_id] = case_status
        self._reporter.set_case_status(module_id, case_id, case_status)
        return is_case_stopped

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
        dependency_tests = self._dependencies.get(
            TestDependencyInfo(node_info.module_id, node_info.case_id),
        )
        is_skip = False
        if dependency_tests:
            wrong_status = {TestStatus.FAILED, TestStatus.SKIPPED, TestStatus.ERROR}
            for dependency_test in dependency_tests:
                module_id, case_id = dependency_test
                module_data = self._results[module_id]
                # case result is the reason for the skipping
                if case_id is not None and module_data[case_id] in wrong_status:  # noqa: SIM114
                    is_skip = True
                    break
                # module result is the reason for the skipping
                elif case_id is None and module_data["module_status"] in wrong_status:  # noqa: RET508
                    is_skip = True
                    break
            if is_skip and node_info.critical is True:
                self._is_critical_not_passed = True
        return is_skip

    def _add_dependency(self, node_info: NodeInfo, nodes: dict) -> None:
        dependencies = node_info.dependency
        if dependencies is None:
            return
        for dependency in dependencies:
            module_id, case_id = dependency
            # incorrect module id in dependency
            if module_id not in nodes:
                continue
            # incorrect case id in dependency
            if case_id not in nodes[module_id] and case_id is not None:
                continue
            test_key = TestDependencyInfo(node_info.module_id, node_info.case_id)
            if test_key not in self._dependencies:
                self._dependencies[test_key] = set()
            self._dependencies[test_key].add(dependency)
