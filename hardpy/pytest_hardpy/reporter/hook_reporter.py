# Copyright (c) 2024 Everypin
# GNU General Public License v3.0 (see LICENSE or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import annotations

from copy import deepcopy
from logging import getLogger
from time import time

from natsort import natsorted
from tzlocal import get_localzone

from hardpy.pytest_hardpy.db import DatabaseField as DF  # noqa: N817
from hardpy.pytest_hardpy.reporter.base import BaseReporter
from hardpy.pytest_hardpy.utils import NodeInfo, TestStatus, machine_id


class HookReporter(BaseReporter):
    """Reporter for using in the hook HardPy plugin's hooks."""

    def __init__(self, is_clear_database: bool = False) -> None:
        super().__init__()
        if is_clear_database:
            self._statestore.clear()
            self._runstore.clear()
        self._log = getLogger(__name__)

    def init_doc(self, doc_name: str) -> None:
        """Initialize document.

        Args:
            doc_name (str): test run name
        """
        self.set_doc_value(DF.NAME, doc_name)
        self.set_doc_value(DF.USER, None)
        self.set_doc_value(DF.BATCH_SN, None)
        self.set_doc_value(DF.CAUSED_DUT_FAILURE_ID, None)
        self.set_doc_value(DF.ERROR_CODE, None)
        self.set_doc_value(DF.STATUS, TestStatus.READY)
        self.set_doc_value(DF.START_TIME, None)
        self.set_doc_value(DF.STOP_TIME, None)
        self.set_doc_value(DF.PROGRESS, 0, statestore_only=True)
        self.set_doc_value(DF.ARTIFACT, {}, runstore_only=True)
        self.set_doc_value(DF.OPERATOR_MSG, {}, statestore_only=True)
        self.set_doc_value(DF.ALERT, "", statestore_only=True)
        self.set_doc_value(DF.OPERATOR_DATA, {}, statestore_only=True)

        test_stand_tz = self.generate_key(DF.TEST_STAND, DF.TIMEZONE)
        self.set_doc_value(test_stand_tz, str(get_localzone().key))

        test_stand_id_key = self.generate_key(DF.TEST_STAND, DF.HW_ID)
        self.set_doc_value(test_stand_id_key, machine_id())

        operator_data_key = self.generate_key(DF.OPERATOR_DATA, DF.DIALOG)
        self.set_doc_value(operator_data_key, "", statestore_only=True)

    def start(self) -> None:
        """Start test."""
        self._log.debug("Starting test run.")
        start_time = int(time())
        self.set_doc_value(DF.START_TIME, start_time)
        self.set_doc_value(DF.STATUS, TestStatus.RUN)
        self.set_doc_value(DF.PROGRESS, 0, statestore_only=True)
        self.set_doc_value(DF.ALERT, "", statestore_only=True)

        operator_data_key = self.generate_key(DF.OPERATOR_DATA, DF.DIALOG)
        self.set_doc_value(operator_data_key, "", statestore_only=True)

    def finish(self, status: TestStatus) -> None:
        """Finish test.

        This method must be called at the end of test run.
        """
        self._log.debug("Finishing test run.")
        stop_time = int(time())
        self.set_doc_value(DF.STOP_TIME, stop_time)
        self.set_doc_value(DF.STATUS, status)

    def compact_all(self) -> None:
        """Compact all databases."""
        self._statestore.compact()
        self._runstore.compact()

    def set_progress(self, progress: int) -> None:
        """Set test progress.

        Args:
            progress (int): test progress
        """
        self.set_doc_value(DF.PROGRESS, progress, statestore_only=True)

    def set_assertion_msg(self, module_id: str, case_id: str, msg: str | None) -> None:
        """Set case assertion message.

        Args:
            module_id (str): test module id
            case_id (str): test case id
            msg (str): assertion message
        """
        key = self.generate_key(
            DF.MODULES,
            module_id,
            DF.CASES,
            case_id,
            DF.ASSERTION_MSG,
        )
        self.set_doc_value(key, msg)

    def add_case(self, node_info: NodeInfo) -> None:
        """Add test case to document.

        Args:
            node_info (NodeInfo): node info
        """
        key = DF.MODULES

        item_statestore = self._statestore.get_field(key)
        item_runstore = self._runstore.get_field(key)

        self._init_case(item_statestore, node_info, is_only_statestore=True)
        self._init_case(item_runstore, node_info, is_only_runstore=True)

        self.set_doc_value(key, item_statestore, statestore_only=True)
        self.set_doc_value(key, item_runstore, runstore_only=True)

    def set_case_status(self, module_id: str, case_id: str, status: TestStatus) -> None:
        """Set test case status.

        Args:
            module_id (str): module id
            case_id (str): case id
            status (TestStatus): test case status
        """
        key = self.generate_key(DF.MODULES, module_id, DF.CASES, case_id, DF.STATUS)
        self.set_doc_value(key, status)

    def get_case_status(self, module_id: str, case_id: str) -> str:
        """Set test case status.

        Args:
            module_id (str): module id
            case_id (str): case id

        Returns:
            str: test case status
        """
        key = self.generate_key(DF.MODULES, module_id, DF.CASES, case_id, DF.STATUS)
        return self._statestore.get_field(key)

    def set_case_start_time(self, module_id: str, case_id: str) -> None:
        """Set test case start_time.

        Args:
            module_id (str): module id
            case_id (str): case id
        """
        key = self.generate_key(DF.MODULES, module_id, DF.CASES, case_id, DF.START_TIME)
        self._set_time(key)

    def set_case_stop_time(self, module_id: str, case_id: str) -> None:
        """Set test case start_time.

        Args:
            module_id (str): module id
            case_id (str): case id
        """
        key = self.generate_key(DF.MODULES, module_id, DF.CASES, case_id, DF.STOP_TIME)
        self._set_time(key)

    def set_module_status(self, module_id: str, status: TestStatus) -> None:
        """Set test module status.

        Args:
            module_id (str): module id
            status (TestStatus): test module status
        """
        key = self.generate_key(DF.MODULES, module_id, DF.STATUS)
        self.set_doc_value(key, status)

    def get_module_status(self, module_id: str) -> str:
        """Get test module status.

        Args:
            module_id (str): module id

        Returns:
            str: test module status
        """
        key = self.generate_key(DF.MODULES, module_id, DF.STATUS)
        return self._statestore.get_field(key)

    def set_module_start_time(self, module_id: str) -> None:
        """Set test module status.

        Args:
            module_id (str): module id
        """
        key = self.generate_key(DF.MODULES, module_id, DF.START_TIME)
        self._set_time(key)

    def set_module_stop_time(self, module_id: str) -> None:
        """Set test module status.

        Args:
            module_id (str): module id
        """
        key = self.generate_key(DF.MODULES, module_id, DF.STOP_TIME)
        self._set_time(key)

    def set_case_attempt(self, module_id: str, case_id: str, attempt: int) -> None:
        """Set test case current attempt.

        Args:
            module_id (str): module id
            case_id (str): case id
            attempt (int): test case current attempt
        """
        key = self.generate_key(
            DF.MODULES,
            module_id,
            DF.CASES,
            case_id,
            DF.ATTEMPT,
        )
        self.set_doc_value(key, attempt)

    def get_module_start_time(self, module_id: str) -> int:
        """Get module start time.

        Returns:
            int: module time
        """
        key = self.generate_key(DF.MODULES, module_id, DF.START_TIME)
        return self._statestore.get_field(key)

    def get_case_start_time(self, module_id: str, case_id: str) -> int:
        """Get case start time.

        Returns:
            int: module time
        """
        key = self.generate_key(DF.MODULES, module_id, DF.CASES, case_id, DF.START_TIME)
        return self._statestore.get_field(key)

    def set_caused_dut_failure_id(self, module_id: str, case_id: str) -> None:
        """Set caused DUT failure id.

        Args:
            module_id (str): module id
            case_id (str): case id
        """
        key = self.generate_key(DF.CAUSED_DUT_FAILURE_ID)
        failure_id = f"{module_id}::{case_id}"
        self.set_doc_value(key, failure_id)

    def get_caused_dut_failure_id(self) -> str | None:
        """Get caused DUT failure id.

        Returns:
            str | None: failure id
        """
        key = self.generate_key(DF.CAUSED_DUT_FAILURE_ID)
        return self._statestore.get_field(key)

    def update_node_order(self, nodes: dict) -> None:
        """Update node order.

        Args:
            nodes (dict): modules and cases.
        """
        key = DF.MODULES
        old_modules = self._statestore.get_field(key)
        modules_copy = deepcopy(old_modules)

        rm_outdated_nodes = self._remove_outdate_node(old_modules, modules_copy, nodes)
        updated_case_order = self._update_case_order(rm_outdated_nodes, nodes)
        updated_module_order = self._update_module_order(updated_case_order)
        self.set_doc_value(key, updated_module_order, statestore_only=True)

    def _set_time(self, key: str) -> None:
        current_time = self._statestore.get_field(key)
        if current_time is None:
            self.set_doc_value(key, int(time()))

    def _init_case(
        self,
        item: dict,
        node_info: NodeInfo,
        is_only_runstore: bool = False,
        is_only_statestore: bool = False,
    ) -> None:
        module_default = {
            DF.STATUS: TestStatus.READY,
            DF.NAME: self._get_module_name(node_info),
            DF.GROUP: self._get_module_group(node_info),
            DF.START_TIME: None,
            DF.STOP_TIME: None,
            DF.CASES: {},
        }
        case_default = {
            DF.STATUS: TestStatus.READY,
            DF.NAME: self._get_case_name(node_info),
            DF.GROUP: self._get_case_group(node_info),
            DF.START_TIME: None,
            DF.STOP_TIME: None,
            DF.ASSERTION_MSG: None,
            DF.MSG: None,
            DF.ATTEMPT: 0,
            DF.MEASUREMENTS: [],
            DF.CHART: None,
        }

        if item.get(node_info.module_id) is None:
            if is_only_runstore:
                module_default[DF.ARTIFACT] = {}
            item[node_info.module_id] = module_default
        else:
            item[node_info.module_id][DF.STATUS] = TestStatus.READY
            item[node_info.module_id][DF.NAME] = self._get_module_name(node_info)
            item[node_info.module_id][DF.GROUP] = self._get_module_group(node_info)
            item[node_info.module_id][DF.START_TIME] = None
            item[node_info.module_id][DF.STOP_TIME] = None
        item[node_info.module_id][DF.NAME] = self._get_module_name(node_info)

        if is_only_runstore:
            case_default[DF.ARTIFACT] = {}

        if is_only_statestore:
            case_default[DF.DIALOG_BOX] = {}
        item[node_info.module_id][DF.CASES][node_info.case_id] = case_default

    def _remove_outdate_node(
        self,
        old_modules: dict,
        new_modules: dict,
        nodes: dict,
    ) -> dict:
        """Remove outdated nodes from StateStore database.

        Args:
            old_modules (dict): list of modules and cases.
            new_modules (dict): list of modules and cases.
            nodes (dict): modules and cases.

        Returns:
            dict: list of modules and cases.
        """
        for module_id, module in old_modules.items():
            # remove outdated modules
            if module_id not in nodes:
                new_modules.pop(module_id)
                continue
            # remove outdated cases in module
            for case_id in module[DF.CASES]:
                if case_id not in nodes[module_id]:
                    new_modules[module_id][DF.CASES].pop(case_id)

        return new_modules

    def _update_case_order(self, modules: dict, nodes: dict) -> dict:
        """Update test order for StateStore database.

        Args:
            modules (dict): list of modules and cases.
            nodes (dict): modules and cases.

        Returns:
            dict: list of modules and cases.
        """
        for module_id, module in modules.items():
            nodes_order = nodes.get(module_id, [])
            modules_order = list(module.get(DF.CASES).keys())
            if nodes_order != modules_order:
                # sort cases in module
                sorted_cases = {}
                for case_name in nodes_order:
                    case_data = module[DF.CASES].get(case_name, {})
                    sorted_cases[case_name] = case_data
                module[DF.CASES] = sorted_cases

        return modules

    def _update_module_order(self, modules: dict) -> dict:
        """Update test order for StateStore database.

        Args:
            modules (dict): list of modules and cases.

        Returns:
            dict: list of modules and cases.
        """
        sorted_modules = natsorted(modules.items(), key=lambda item: item[0])

        new_modules = {}
        for module_id, module in sorted_modules:
            new_modules[module_id] = module  # noqa: PERF403

        return new_modules

    def _get_module_name(self, node_info: NodeInfo) -> str:
        """Get module name from markers or use default.

        Args:
            node_info (NodeInfo): node info

        Returns:
            str: module name
        """
        return node_info.module_name if node_info.module_name else node_info.module_id

    def _get_module_group(self, node_info: NodeInfo) -> str:
        """Get module group from markers or use default.

        Args:
            node_info (NodeInfo): node info

        Returns:
            str: module group
        """
        return node_info.module_group

    def _get_case_group(self, node_info: NodeInfo) -> str:
        """Get case group from markers or use default.

        Args:
            node_info (NodeInfo): node info

        Returns:
            str: case group
        """
        return node_info.case_group

    def _get_case_name(self, node_info: NodeInfo) -> str:
        """Get case name from markers or use default.

        Args:
            node_info (NodeInfo): node info

        Returns:
            str: case name
        """
        return node_info.case_name if node_info.case_name else node_info.case_id
