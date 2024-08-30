# Copyright (c) 2024 Everypin
# GNU General Public License v3.0 (see LICENSE or https://www.gnu.org/licenses/gpl-3.0.txt)

import sys
import signal
import subprocess
from socket import socket
from platform import system

from hardpy.config import ConfigManager


class PyTestWrapper(object):
    """Wrapper for pytest subprocess."""

    def __init__(self):
        self._proc = None
        self.python_executable = sys.executable

        # Make sure test structure is stored in DB
        # before clients come in
        self.config = ConfigManager().get_config()
        self.collect()

    def start(self):
        """Start pytest subprocess.

        Returns True if pytest was started.
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

        Returns True if pytest was running and stopped.
        """
        if self.is_running() and self._proc:
            if system() == "Linux":
                self._proc.terminate()
            elif system() == "Windows":
                self._proc.send_signal(signal.CTRL_BREAK_EVENT)
            return True
        return False

    def collect(self) -> bool:
        """Perform pytest collection.

        Returns True if collection was started.
        """
        if self.python_executable is None:
            return False

        if self.is_running():
            return False

        subprocess.Popen(  # noqa: S603
            [
                self.python_executable,
                "-m" "pytest",
                "--collect-only",
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
        return True

    def confirm_dialog_box(self, dialog_box_output: str):
        """Set dialog box data to pytest subprocess.

        Args:
            dialog_box_output (str): dialog box output data

        Returns:
            bool: True if dialog box was confirmed, else False
        """
        try:
            client = socket()
            client.connect((self.config.socket.host, self.config.socket.port))
            client.sendall(dialog_box_output.encode("utf-8"))
            client.close()
        except Exception:
            return False
        return True

    def is_running(self) -> bool | None:
        """Check if pytest is running."""
        return self._proc and self._proc.poll() is None
