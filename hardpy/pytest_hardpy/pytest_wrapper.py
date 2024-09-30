# Copyright (c) 2024 Everypin
# GNU General Public License v3.0 (see LICENSE or https://www.gnu.org/licenses/gpl-3.0.txt)

import signal
import subprocess  # noqa: S404
import sys
from platform import system
from socket import socket

from hardpy.common.config import ConfigManager


class PyTestWrapper:
    """Wrapper for pytest subprocess."""

    def __init__(self):
        self._proc = None
        self.python_executable = sys.executable

        # Make sure test structure is stored in DB
        # before clients come in
        self.config = ConfigManager().get_config()
        self.collect(is_clear_database=True)

    def start(self) -> bool:
        """Start pytest subprocess.

        Returns:
            bool: True if pytest was started
        """
        if self.python_executable is None:
            return False

        if self.is_running():
            return False

        if system() == "Linux":
            self._proc = subprocess.Popen(  # noqa: S603
                [
                    self.python_executable,
                    "-m",
                    "pytest",
                    "--hardpy-db-url",
                    self.config.database.connection_url(),
                    "--hardpy-sp",
                    str(self.config.socket.port),
                    "--hardpy-sh",
                    self.config.socket.host,
                    "--hardpy-pt",
                ],
                cwd=ConfigManager().get_tests_path(),
            )
        elif system() == "Windows":
            self._proc = subprocess.Popen(  # noqa: S603
                [
                    self.python_executable,
                    "-m",
                    "pytest",
                    "--hardpy-db-url",
                    self.config.database.connection_url(),
                    "--hardpy-sp",
                    str(self.config.socket.port),
                    "--hardpy-sh",
                    self.config.socket.host,
                    "--hardpy-pt",
                ],
                cwd=ConfigManager().get_tests_path(),
                creationflags=subprocess.CREATE_NEW_PROCESS_GROUP,
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
                self._proc.send_signal(signal.CTRL_BREAK_EVENT)
            return True
        return False

    def collect(self, is_clear_database: bool = False) -> bool:
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
            "--hardpy-sp",
            str(self.config.socket.port),
            "--hardpy-sh",
            self.config.socket.host,
            "--hardpy-pt",
        ]

        if is_clear_database:
            args.append("--hardpy-clear-database")
            args.append(str(is_clear_database))

        subprocess.Popen(  # noqa: S603
            [self.python_executable, *args],
            cwd=ConfigManager().get_tests_path(),
        )
        return True

    def send_data(self, data: str):
        """Send data to pytest subprocess.

        Args:
            data (str): Data to be sent. Can be dialog
                        box output or operator message visibility.

        Returns:
            bool: True if dialog box was confirmed/closed, else False
        """
        try:
            client = socket()
            client.connect((self.config.socket.host, self.config.socket.port))
            client.sendall(data.encode("utf-8"))
            client.close()
        except Exception:
            return False
        return True

    def is_running(self) -> bool | None:
        """Check if pytest is running.

        Returns:
            bool | None: True if self._proc is not None
        """
        return self._proc and self._proc.poll() is None
