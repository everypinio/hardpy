# Copyright (c) 2024 Everypin
# GNU General Public License v3.0 (see LICENSE or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import annotations

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


class PyTestWrapper:
    """Wrapper for pytest subprocess."""

    def __init__(self, app: FastAPI) -> None:
        self._proc = None
        self._reporter = RunnerReporter()
        self.python_executable = sys.executable
        self._app = app

        # Make sure test structure is stored in DB
        # before clients come in
        self._config_manager = ConfigManager()
        self.config = self._config_manager.config

        # Store the full test structure from collection
        self._full_test_structure = None
        self.collect(is_clear_database=True)

    def start(self, start_args: dict | None = None) -> bool:
        """Start pytest subprocess.

        Args:
            start_args: Additional start arguments

        Returns:
            bool: True if pytest was started
        """
        # Check if manual collect mode is active
        if getattr(self._app.state, "manual_collect_mode", False):
            return False

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
            self.config.tests_name,
            "--sc-address",
            self.config.stand_cloud.address,
        ]

        selected_tests = getattr(self._app.state, "selected_tests", None)
        if selected_tests:
            pytest_test_paths = []
            for test_path in selected_tests:
                if "::" in test_path:
                    file_name, test_name = test_path.split("::", 1)
                    pytest_path = f"{file_name}.py::{test_name}"
                    pytest_test_paths.append(pytest_path)
                else:
                    pytest_test_paths.append(f"{test_path}.py")

            cmd.extend(pytest_test_paths)

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
        self._current_selection = selected_tests or []

        # Preserve full test structure in database before starting selected tests
        self._preserve_full_test_structure()

        if system() == "Windows":
            self._proc = subprocess.Popen(  # noqa: S603
                cmd,
                cwd=self._config_manager.tests_path,
                creationflags=subprocess.CREATE_NEW_PROCESS_GROUP,
            )
        if system() == "Linux":
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
        # Check if manual collect mode is active
        if getattr(self._app.state, "manual_collect_mode", False):
            return False

        if self.is_running() and self._proc:
            if system() == "Linux":
                self._proc.terminate()
            elif system() == "Windows":
                self._proc.send_signal(signal.CTRL_BREAK_EVENT)  # type: ignore
            return True
        return False

    def collect(self, *, is_clear_database: bool = False) -> bool:
        """Perform pytest collection.

        Args:
            is_clear_database (bool): indicates whether database
                                      should be cleared. Defaults to False.

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
            self.config.tests_name,
            "--hardpy-pt",
        ]

        if is_clear_database:
            args.append("--hardpy-clear-database")

        # Run collection and store the full test structure
        process = subprocess.Popen(  # noqa: S603
            [self.python_executable, *args],
            cwd=self._config_manager.tests_path,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )

        # Wait for collection to complete and store the structure
        process.wait()
        self._store_full_test_structure()

        return True

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
        """Preserve full test structure when running selected tests."""
        if not self._full_test_structure:
            return

        try:
            self._reporter.update_doc_by_db()

            # Get current selected tests
            selected_tests = getattr(self._app.state, "selected_tests", [])
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
                            is_selected = full_test_path in selected_tests
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

    def send_selected_tests(self, selected_tests: list[str]) -> bool:
        """Send selected tests to the FastAPI application's state.

        Args:
            selected_tests: A list of selected test paths.

        Returns:
            bool: True if the data was sent successfully.
        """
        try:
            self._app.state.selected_tests = selected_tests
        except Exception:  # noqa: BLE001
            return False
        else:
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
