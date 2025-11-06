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
            logger.info(
                "No test configurations defined in the HardPy configuration. "
                "Loading from tests directory.",
            )
            self.collect(is_clear_database=True)
        else:
            self.clear_database()
            # Check if there's a current test config selected in statestore
            try:
                current_config_name = self.config.current_test_config
                if current_config_name != "":
                    self.collect(
                        is_clear_database=True,
                        test_config=current_config_name,
                    )
                else:
                    logger.info("No existing test config selection found.")

            except Exception:
                # No existing test configs in statestore, will be initialized later
                logger.exception(
                    "Error retrieving current test config from statestore.",
                )

    def start(self, start_args: dict | None = None) -> bool:
        """Start pytest subprocess.

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
            self.config.tests_name,
            "--sc-address",
            self.config.stand_cloud.address,
        ]

        # Add test configuration file if specified
        test_config_file = self._config_manager.get_test_config_file(
            self.config.current_test_config,
        )
        if test_config_file is not None:
            logging.info("Using test configuration file: %s", test_config_file)
            cmd.extend(["--config-file", test_config_file])

        if self.config.stand_cloud.connection_only:
            cmd.append("--sc-connection-only")
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
        if self.is_running() and self._proc:
            if system() == "Linux":
                self._proc.terminate()
            elif system() == "Windows":
                self._proc.send_signal(signal.CTRL_BREAK_EVENT)  # type: ignore
            return True
        return False

    def collect(
        self,
        *,
        is_clear_database: bool = False,
        test_config: str | None = None,
    ) -> bool:
        """Perform pytest collection.

        Args:
            is_clear_database (bool): indicates whether database
                                      should be cleared. Defaults to False.
            test_config (str | None): test configuration name. Defaults to None.

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

        # Add test configuration file if specified
        if test_config:
            test_config_file = self._config_manager.get_test_config_file(test_config)
            if test_config_file is not None:
                logging.info("Using test configuration file: %s", test_config_file)
                args.extend(["--config-file", test_config_file])

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

    def clear_database(self) -> None:
        """Clear both statestore and runstore databases directly."""
        try:
            self._reporter._statestore.clear()  # noqa: SLF001
            self._reporter._runstore.clear()  # noqa: SLF001
            logging.info("Database cleared successfully")
        except Exception:
            logging.exception("Failed to clear database")
