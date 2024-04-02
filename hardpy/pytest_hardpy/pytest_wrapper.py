# Copyright (c) 2024 Everypin
# GNU General Public License v3.0 (see LICENSE or https://www.gnu.org/licenses/gpl-3.0.txt)

import sys
import signal
import subprocess
from platform import system

from hardpy.pytest_hardpy.utils.config_data import ConfigData


class PyTestWrapper(object):
    """Wrapper for pytest subprocess."""

    def __init__(self):
        self._proc = None
        self.python_executable = sys.executable

        # Make sure test structure is stored in DB
        # before clients come in
        self.config = ConfigData()
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
                    "--hardpy-dbp",
                    str(self.config.db_port),
                    "--hardpy-dbh",
                    self.config.db_host,
                    "--hardpy-dbu",
                    self.config.db_user,
                    "--hardpy-dbpw",
                    self.config.db_pswd,
                    "--hardpy-pt",
                ],
                cwd=self.config.tests_dir.absolute(),
            )
        elif system() == "Windows":
            self._proc = subprocess.Popen(  # noqa: S603
                [
                    self.python_executable,
                    "-m",
                    "pytest",
                    "--hardpy-dbp",
                    str(self.config.db_port),
                    "--hardpy-dbh",
                    self.config.db_host,
                    "--hardpy-dbu",
                    self.config.db_user,
                    "--hardpy-dbpw",
                    self.config.db_pswd,
                    "--hardpy-pt",
                ],
                cwd=self.config.tests_dir.absolute(),
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
                "--hardpy-dbp",
                str(self.config.db_port),
                "--hardpy-dbh",
                self.config.db_host,
                "--hardpy-dbu",
                self.config.db_user,
                "--hardpy-dbpw",
                self.config.db_pswd,
                "--hardpy-pt",
            ],
            cwd=self.config.tests_dir.absolute(),
        )
        return True

    def is_running(self) -> bool | None:
        """Check if pytest is running."""
        return self._proc and self._proc.poll() is None
