# Copyright (c) 2024 Everypin
# GNU General Public License v3.0 (see LICENSE or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import annotations

import logging
import signal
import subprocess
import sys
from platform import system

from hardpy.common.config import ConfigManager
from hardpy.pytest_hardpy.db import DatabaseField as DF  # noqa: N817
from hardpy.pytest_hardpy.reporter import RunnerReporter

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class PyTestWrapper:
    """Wrapper for pytest subprocess."""

    def __init__(self) -> None:
        self._proc = None
        self._reporter = RunnerReporter()
        self.python_executable = sys.executable

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

    def start(
        self,
        start_args: dict | None = None,
        selected_tests: list[str] | None = None,
    ) -> bool:
        """Start pytest subprocess.

        Args:
            start_args: Additional start arguments
            selected_tests: List of selected tests

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

        if selected_tests:
            selected_test_cases = self._select_test_cases(selected_tests)
            cmd.extend(selected_test_cases)

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
        selected_tests: list[str] | None = None,
    ) -> bool:
        """Perform pytest collection.

        Args:
            is_clear_database (bool): indicates whether database
                                      should be cleared. Defaults to False.
            selected_tests (list[str]): list of selected tests

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

        if selected_tests:
            selected_test_cases = self._select_test_cases(selected_tests)
            args.extend(selected_test_cases)

        subprocess.Popen(  # noqa: S603
            [self.python_executable, *args],
            cwd=self._config_manager.tests_path,
        )
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

    def _tests_name(self) -> str:
        manual_str = ""
        if self.config.frontend.manual_collect:
            manual_str = " Manual mode"

        tests_name = (
            self.config.tests_name + f" {self.config.current_test_config}"
            if self.config.current_test_config
            else self.config.tests_name
        )
        return tests_name + manual_str

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

    def _select_test_cases(self, selected_tests: list[str]) -> list[str]:
        test_cases = []
        for test_path in selected_tests:
            if "::" in test_path:
                module_name, case_name = test_path.split("::", 1)
                case_path = f"{module_name}.py::{case_name}"
                test_cases.append(case_path)
            else:
                test_cases.append(f"{test_path}.py")
        return test_cases
