# Copyright (c) 2024 Everypin
# GNU General Public License v3.0 (see LICENSE or https://www.gnu.org/licenses/gpl-3.0.txt)

import signal
from logging import getLogger
from pathlib import Path, PurePath
from platform import system
from re import compile as re_compile
from typing import Any, Callable

from natsort import natsorted
from pytest import (
    skip,
    exit,
    TestReport,
    Item,
    Session,
    Config,
    Parser,
    fixture,
    ExitCode,
)
from _pytest._code.code import (
    ExceptionRepr,
    ReprFileLocation,
    ExceptionInfo,
    ReprExceptionInfo,
    TerminalRepr,
)

from hardpy.pytest_hardpy.reporter import HookReporter
from hardpy.pytest_hardpy.utils import (
    TestStatus,
    NodeInfo,
    ProgressCalculator,
    ConnectionData,
)
from hardpy.pytest_hardpy.utils.node_info import TestDependencyInfo


def pytest_addoption(parser: Parser):
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
        action="store",
        default=False,
        help="clear hardpy local database",
    )
    parser.addoption(
        "--hardpy-pt",
        action="store_true",
        default=False,
        help="enable pytest-hardpy plugin",
    )


# Bootstrapping hooks
def pytest_load_initial_conftests(early_config, parser, args):
    if "--hardpy-pt" in args:
        plugin = HardpyPlugin()
        early_config.pluginmanager.register(plugin)


class HardpyPlugin:
    """HardPy integration plugin for pytest.

    Extends hook functions from pytest API.
    """

    def __init__(self):
        self._progress = ProgressCalculator()
        self._results = {}
        self._post_run_functions: list[Callable] = []
        self._dependencies = {}

        if system() == "Linux":
            signal.signal(signal.SIGTERM, self._stop_handler)
        elif system() == "Windows":
            signal.signal(signal.SIGBREAK, self._stop_handler)
        self._log = getLogger(__name__)

    # Initialization hooks

    def pytest_configure(self, config: Config):
        """Configure pytest."""
        con_data = ConnectionData()

        database_url = config.getoption("--hardpy-db-url")
        if database_url:
            con_data.database_url = str(database_url)

        is_clear_database = config.getoption("--hardpy-clear-database")
        is_clear_statestore = is_clear_database == str(True)

        socket_port = config.getoption("--hardpy-sp")
        if socket_port:
            con_data.socket_port = int(socket_port)  # type: ignore

        socket_host = config.getoption("--hardpy-sh")
        if socket_host:
            con_data.socket_host = str(socket_host)

        config.addinivalue_line("markers", "case_name")
        config.addinivalue_line("markers", "module_name")
        config.addinivalue_line("markers", "dependency")

        # must be init after config data is set
        try:
            self._reporter = HookReporter(is_clear_statestore)
        except RuntimeError as exc:
            exit(str(exc), 1)

    def pytest_sessionfinish(self, session: Session, exitstatus: int):
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
        self, session: Session, config: Config, items: list[Item]
    ):
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
            except ValueError:
                error_msg = f"Error creating NodeInfo for item: {item}\n"
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

    def pytest_runtestloop(self, session: Session):
        """Call at the start of test run."""
        self._progress.set_test_amount(session.testscollected)
        if session.config.option.collectonly:
            # ignore collect only mode
            return True

        # testrun entrypoint
        self._reporter.start()
        self._reporter.update_db_by_doc()

    def pytest_runtest_setup(self, item: Item):
        """Call before each test setup phase."""
        if item.parent is None:
            self._log.error(f"Test module name for test {item.name} not found.")
            return

        node_info = NodeInfo(item)

        self._handle_dependency(node_info)

        self._reporter.set_module_status(node_info.module_id, TestStatus.RUN)
        self._reporter.set_module_start_time(node_info.module_id)
        self._reporter.set_case_status(
            node_info.module_id,
            node_info.case_id,
            TestStatus.RUN,
        )
        self._reporter.set_case_start_time(
            node_info.module_id,
            node_info.case_id,
        )
        self._reporter.update_db_by_doc()

    # Reporting hooks

    def pytest_runtest_logreport(self, report: TestReport):
        """Call after call of each test item."""
        if report.when != "call" and report.failed is False:
            # ignore setup and teardown phase
            # or continue processing setup and teardown failure (fixture exception handler)
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
        self._results[module_id][case_id] = report.outcome  # noqa: WPS204

        if None not in self._results[module_id].values():
            self._collect_module_result(module_id)
        self._reporter.update_db_by_doc()

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

    def _stop_handler(self, signum: int, frame: Any):
        exit("Tests stopped by user")

    def _init_case_result(self, module_id: str, case_id: str):
        if self._results.get(module_id) is None:
            self._results[module_id] = {
                "module_status": TestStatus.READY,
                case_id: None,
            }
        else:
            self._results[module_id][case_id] = None

    def _collect_module_result(self, module_id: str):
        if TestStatus.ERROR in self._results[module_id].values():
            status = TestStatus.ERROR
        elif TestStatus.FAILED in self._results[module_id].values():
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
                return TestStatus.ERROR

    def _stop_tests(self):  # noqa: WPS231
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
        error: (  # noqa: WPS320
            ExceptionInfo[BaseException]  # noqa: DAR101,DAR201
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
            case tuple() if len(error) == 3:
                return error[2]
            case ExceptionInfo():
                error_repr = error.getrepr()
                if isinstance(error_repr, ReprExceptionInfo) and error_repr.reprcrash:
                    return error_repr.reprcrash.message
            case TerminalRepr():
                if isinstance(error, ExceptionRepr) and isinstance(  # noqa: WPS337
                    error.reprcrash, ReprFileLocation
                ):
                    # remove ansi codes
                    ansi_pattern = re_compile(
                        r"(?:\x1B[@-Z\\-_]|[\x80-\x9A\x9C-\x9F]|(?:\x1B\[|\x9B)[0-?]*[ -/]*[@-~])"  # noqa: E501
                    )
                    return ansi_pattern.sub("", error.reprcrash.message)
                return str(error)
            case _:
                return None

    def _handle_dependency(self, node_info: NodeInfo):
        dependency = self._dependencies.get(
            TestDependencyInfo(
                node_info.module_id,
                node_info.case_id,
            )
        )
        if dependency and self._is_dependency_failed(dependency):
            self._log.debug(f"Skipping test due to dependency: {dependency}")
            self._results[node_info.module_id][node_info.case_id] = TestStatus.SKIPPED
            self._reporter.set_progress(
                self._progress.calculate(f"{node_info.module_id}::{node_info.case_id}")
            )
            skip(f"Test {node_info.module_id}::{node_info.case_id} is skipped")

    def _is_dependency_failed(self, dependency) -> bool:
        if isinstance(dependency, TestDependencyInfo):
            incorrect_status = {
                TestStatus.FAILED,
                TestStatus.SKIPPED,
                TestStatus.ERROR,
            }
            module_id, case_id = dependency
            if case_id is not None:
                return self._results[module_id][case_id] in incorrect_status
            return any(
                status in incorrect_status
                for status in set(self._results[module_id].values())
            )
        return False

    def _add_dependency(self, node_info, nodes):
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
