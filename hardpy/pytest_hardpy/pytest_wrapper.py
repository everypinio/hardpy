# Copyright (c) 2024 Everypin
# GNU General Public License v3.0 (see LICENSE or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import annotations

import signal
import subprocess
import sys
from platform import system

from hardpy.common.config import ConfigManager
from hardpy.pytest_hardpy.db import DatabaseField as DF  # noqa: N817
from hardpy.pytest_hardpy.reporter import RunnerReporter


class PyTestWrapper:
    """Wrapper for pytest subprocess."""

    def __init__(self) -> None:
        self._proc = None
        self._reporter = RunnerReporter()
        self.python_executable = sys.executable

        # Make sure test structure is stored in DB
        # before clients come in
        self.config = ConfigManager().get_config()
        self.collect(is_clear_database=True)

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
            self.config.database.connection_url(),
            "--hardpy-tests-name",
            self.config.tests_name,
            "--sc-address",
            self.config.stand_cloud.address,
        ]
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
                cwd=ConfigManager().get_tests_path(),
                creationflags=subprocess.CREATE_NEW_PROCESS_GROUP,
            )
        if system() == "Linux":
            self._proc = subprocess.Popen(  # noqa: S603
                cmd,
                cwd=ConfigManager().get_tests_path(),
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
            self.config.database.connection_url(),
            "--hardpy-tests-name",
            self.config.tests_name,
            "--hardpy-pt",
        ]

        if is_clear_database:
            args.append("--hardpy-clear-database")

        subprocess.Popen(  # noqa: S603
            [self.python_executable, *args],
            cwd=ConfigManager().get_tests_path(),
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
        return ConfigManager().get_config().model_dump()
