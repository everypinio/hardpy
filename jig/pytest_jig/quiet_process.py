# Copyright (c) 2026 Everypin
# GNU General Public License v3.0 (see LICENSE or https://www.gnu.org/licenses/gpl-3.0.txt)
"""Subprocess spawning that keeps the operator console clean."""

from __future__ import annotations

import subprocess
import threading
from dataclasses import dataclass
from logging import getLogger
from pathlib import Path

logger = getLogger(__name__)


@dataclass(frozen=True)
class SpawnedProcess:
    """A spawned process together with the thread logging its output."""

    process: subprocess.Popen
    output_logger: threading.Thread | None = None

    def wait(self, timeout: float | None = None) -> int:
        """Wait for the process to exit and for its output to be logged.

        Args:
            timeout (float | None): maximum wait duration in seconds

        Returns:
            int: process exit code
        """
        exit_code = self.process.wait(timeout=timeout)
        if self.output_logger is not None:
            self.output_logger.join(timeout=timeout)
        return exit_code


def spawn(
    args: list[str],
    cwd: str | Path,
    *,
    is_quiet: bool = True,
) -> SpawnedProcess:
    """Spawn a subprocess, optionally keeping its output off the console.

    The output of a quiet process is captured and logged once it exits:
    at debug level when it succeeds, at error level when it fails, so that
    a failure is never silently swallowed.

    Args:
        args (list[str]): command line of the process
        cwd (str | Path): working directory of the process
        is_quiet (bool): capture the output instead of writing
                         to the console streams

    Returns:
        SpawnedProcess: spawned process
    """
    if not is_quiet:
        return SpawnedProcess(subprocess.Popen(args, cwd=cwd))  # noqa: S603

    process = subprocess.Popen(  # noqa: S603
        args,
        cwd=cwd,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
    )
    output_logger = threading.Thread(
        target=_log_output,
        args=(process, args),
        daemon=True,
    )
    output_logger.start()
    return SpawnedProcess(process, output_logger)


def _log_output(process: subprocess.Popen, args: list[str]) -> None:
    output = process.stdout.read() if process.stdout else ""
    exit_code = process.wait()
    command = " ".join(str(arg) for arg in args)

    if exit_code == 0:
        logger.debug(f"{command} output:\n{output}")
    else:
        logger.error(f"{command} failed with exit code {exit_code}:\n{output}")
