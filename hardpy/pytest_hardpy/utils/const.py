# Copyright (c) 2024 Everypin
# GNU General Public License v3.0 (see LICENSE or https://www.gnu.org/licenses/gpl-3.0.txt)

from enum import Enum


class TestStatus(str, Enum):
    """Pytest test status.

    Statuses, that can be returned by Pytest.
    """

    PASSED = "passed"
    FAILED = "failed"
    SKIPPED = "skipped"
    ERROR = "error"
    RUN = "run"
    READY = "ready"
    STOPPED = "stopped"
