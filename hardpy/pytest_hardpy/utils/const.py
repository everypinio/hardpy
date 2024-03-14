# Copyright (c) 2024 Everypin
# GNU General Public License v3.0 (see LICENSE or https://www.gnu.org/licenses/gpl-3.0.txt)

from enum import Enum


class TestStatus(str, Enum):  # noqa: WPS600
    """Pytest test status."""

    PASSED = "passed"
    FAILED = "failed"
    SKIPPED = "skipped"
    ERROR = "error"
    RUN = "run"
    READY = "ready"
    STOPPED = "stopped"


class RunStatus(str, Enum):  # noqa: WPS600
    """Pytest run status."""

    PASSED = "passed"
    FAILED = "failed"
    STOPPED = "stopped"
    STARTED = "started"
    COLLECTED = "collected"
    BUSY = "busy"
    READY = "ready"
    ERROR = "error"
