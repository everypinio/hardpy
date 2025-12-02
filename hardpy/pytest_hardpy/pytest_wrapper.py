# Copyright (c) 2024 Everypin
# GNU General Public License v3.0 (see LICENSE or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import annotations

import logging
import signal
import subprocess
import sys
from platform import system
from typing import TYPE_CHECKING

from hardpy.common.config import ConfigManager
from hardpy.pytest_hardpy.db import DatabaseField as DF  # noqa: N817
from hardpy.pytest_hardpy.reporter import RunnerReporter

if TYPE_CHECKING:
    from fastapi import FastAPI

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class PyTestWrapper:
    """Wrapper for pytest subprocess."""

    def __init__(self, app: FastAPI) -> None:
        self._proc = None
        self._reporter = RunnerReporter()
        self.python_executable = sys.executable
        self._app = app
        self._selected_tests = []

        # Make sure test structure is stored in DB
        # before clients come in
        self._config_manager = ConfigManager()
        self.config = self._config_manager.config

        # Check to see if there are any test configs defined in the TOML file
        if not self.config.test_configs:
            self.collect(is_clear_database=True)
        else:
            self._reporter.clear_database()
            # Check if there's a current test config selected in statestore
            config_name = self.config.current_test_config
            if config_name:
                try:
                    self.collect(is_clear_database=True)
                except Exception:
                    # No existing test configs in statestore, will be initialized later
                    msg = "Error retrieving current test config from statestore."
                    logger.exception(msg)
            else:
                logger.info("No existing test config selection found.")

        # Store the full test structure from collection
        self._full_test_structure = None
        self.collect(is_clear_database=True, is_update_full_tests=True)

    def start(self, start_args: dict | None = None) -> bool:
        """Start pytest subprocess.

        Args:
            start_args: Additional start arguments

        Returns:
            bool: True if pytest was started
        """
        if self.python_executable is None:
            return False

        if self.is_running():
            return False

        cmd = [
            self.python_executable,
            "-m",
            "pytest",
            "--hardpy-db-url",
            self.config.database.url,
            "--hardpy-tests-name",
            self._tests_name(),
            "--sc-address",
            self.config.stand_cloud.address,
        ]

        if self._selected_tests:
            pytest_test_paths = []
            for test_path in self._selected_tests:
                if "::" in test_path:
                    file_name, test_name = test_path.split("::", 1)
                    pytest_path = f"{file_name}.py::{test_name}"
                    pytest_test_paths.append(pytest_path)
                else:
                    pytest_test_paths.append(f"{test_path}.py")

            cmd.extend(pytest_test_paths)

        self._add_config_file(cmd)

        if self.config.stand_cloud.connection_only:
            cmd.append("--sc-connection-only")
        if self.config.stand_cloud.autosync:
            cmd.append("--sc-autosync")
        cmd.append("--hardpy-pt")

        if start_args:
            for key, value in start_args.items():
                arg_str = f"{key}={value}"
                cmd.extend(["--hardpy-start-arg", arg_str])

        # Store current selection before starting
        self._current_selection = self._selected_tests or []

        # Preserve full test structure in database before starting selected tests
        self._preserve_full_test_structure()

        if system() == "Windows":
            self._proc = subprocess.Popen(  # noqa: S603
                cmd,
                cwd=self._config_manager.tests_path,
                creationflags=subprocess.CREATE_NEW_PROCESS_GROUP,
            )
        else:
            self._proc = subprocess.Popen(  # noqa: S603
                cmd,
                cwd=self._config_manager.tests_path,
            )

        return True

    def stop(self) -> bool:
        """Stop pytest subprocess.

        Returns:
            bool: True if pytest was running and stopped
        """
        if self.is_running() and self._proc:
            if system() == "Windows":
                self._proc.send_signal(signal.CTRL_BREAK_EVENT)  # type: ignore
            else:
                self._proc.terminate()
            return True
        return False

    def collect(
        self,
        *,
        is_clear_database: bool = False,
        is_update_full_tests: bool = False,
    ) -> bool:
        """Perform pytest collection.

        Args:
            is_clear_database (bool): indicates whether database
                                      should be cleared. Defaults to False.
            is_update_full_tests (bool): indicates whether to update full test structure.
                                      Defaults to False.

        Returns:
            bool: True if collection was started
        """
        if self.python_executable is None:
            return False

        if self.is_running():
            return False

        args = [
            "-m",
            "pytest",
            "--collect-only",
            "--hardpy-db-url",
            self.config.database.url,
            "--hardpy-tests-name",
            self._tests_name(),
            "--hardpy-pt",
        ]

        if is_clear_database:
            args.append("--hardpy-clear-database")

        self._add_config_file(args)

        process = subprocess.Popen(  # noqa: S603
            [self.python_executable, *args],
            cwd=self._config_manager.tests_path,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )

        # Only wait and store structure if explicitly requested
        if is_update_full_tests:
            process.wait()
            self._store_full_test_structure()

        return True

    def send_data(self, data: str) -> bool:
        """Send data to pytest subprocess.

        Args:
            data (str): Data to be sent. Can be dialog
                        box output or operator message visibility.

        Returns:
            bool: True if dialog box was confirmed/closed, else False
        """
        try:
            self._reporter.update_doc_by_db()
            key = self._reporter.generate_key(DF.OPERATOR_DATA, DF.DIALOG)
            self._reporter.set_doc_value(key, data, statestore_only=True)
            self._reporter.update_db_by_doc()
        except Exception:  # noqa: BLE001
            return False
        return True

    def is_running(self) -> bool | None:
        """Check if pytest is running.

        Returns:
            bool | None: True if self._proc is not None
        """
        return self._proc and self._proc.poll() is None

    def get_config(self) -> dict:
        """Get HardPy configuration.

        Returns:
            dict: HardPy configuration
        """
        config_manager = ConfigManager()
        return config_manager.config.model_dump()

    def select_tests(self, selected_tests: list[str]) -> None:
        """Select tests for the manual run.

        Args:
            selected_tests: A list of selected tests.
        """
        self._selected_tests = selected_tests

    def _tests_name(self) -> str:
        return (
            self.config.tests_name + f" {self.config.current_test_config}"
            if self.config.current_test_config
            else self.config.tests_name
        )

    def _add_config_file(self, cmd: list) -> None:
        """Add test configuration file if specified."""
        config_name = self.config.current_test_config
        test_config_file = None

        if self.config.test_configs:
            for config in self.config.test_configs:
                if config.name == config_name:
                    test_config_file = config.file
                    break

        if test_config_file:
            logging.info(f"Using test configuration file: {test_config_file}")
            cmd.extend(["--config-file", test_config_file])

    def _store_full_test_structure(self) -> None:
        """Store the full test structure from the last collection."""
        try:
            self._reporter.update_doc_by_db()
            # Extract modules structure from the database
            modules_key = self._reporter.generate_key(DF.MODULES)
            full_structure = self._reporter.get_field(modules_key)
            self._full_test_structure = full_structure
        except Exception:  # noqa: BLE001
            self._full_test_structure = None

    def _preserve_full_test_structure(self) -> None:
        """Preserve full test structure in database when running selected tests.

        This method ensures that the complete test structure remains visible in the database
        even when only a subset of tests is executed. It handles two main scenarios:

        1. Manual collect mode: Marks non-selected tests as "skipped" with cleared timestamps
        and messages to indicate they were not executed.

        2. Automatic mode: Preserves all tests with their current statuses.

        The method creates a modified copy of the full test structure where:
        - Selected tests retain their original status and data
        - Non-selected tests (in manual mode) are marked as skipped with reset metadata
        - The complete hierarchy (modules → cases) is maintained

        This allows the UI to display the full test suite structure while clearly indicating
        which tests were actually executed in the current run.

        Note: The method fails silently if any errors occur during database operations.
        """
        if not self._full_test_structure:
            return

        try:
            self._reporter.update_doc_by_db()

            # Get current selected tests
            manual_collect_mode = getattr(self._app.state, "manual_collect_mode", False)

            # Create a copy of full structure with selection info
            preserved_structure = {}
            for module_name, module_data in self._full_test_structure.items():
                preserved_module = module_data.copy()
                preserved_module_cases = {}

                if module_data.get("cases"):
                    for case_name, case_data in module_data["cases"].items():
                        full_test_path = f"{module_name}::{case_name}"
                        if manual_collect_mode:
                            is_selected = full_test_path in self._selected_tests
                        else:
                            is_selected = True

                        preserved_case = case_data.copy()

                        if manual_collect_mode and not is_selected:
                            preserved_case["status"] = "skipped"
                            preserved_case["start_time"] = None
                            preserved_case["stop_time"] = None
                            preserved_case["assertion_msg"] = None
                            preserved_case["msg"] = None
                        else:
                            preserved_case["status"] = case_data.get("status", "ready")

                        preserved_module_cases[case_name] = preserved_case

                preserved_module["cases"] = preserved_module_cases
                preserved_structure[module_name] = preserved_module

            # Update database with preserved structure
            modules_key = self._reporter.generate_key(DF.MODULES)
            self._reporter.set_doc_value(modules_key, preserved_structure)
            self._reporter.update_db_by_doc()

        except Exception:  # noqa: BLE001, S110
            pass
