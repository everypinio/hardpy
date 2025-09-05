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


class Group(str, Enum):
    """Test group."""

    SETUP = "setup"
    MAIN = "main"
    TEARDOWN = "teardown"


class MeasurementType(str, Enum):
    """Measurement type."""

    NUMERIC = "numeric"
    """Numeric measurement"""

    STRING = "string"
    """String measurement"""


class ComparisonOperation(str, Enum):
    """Comparison operator."""

    EQ = "eq"
    """Equal"""

    NE = "ne"
    """Not equal"""

    GT = "gt"
    """Greater than"""

    GE = "ge"
    """Greater or equal"""

    LT = "lt"
    """Less than"""

    LE = "le"
    """Less or equal"""

    GTLT = "gtlt"
    """Greater than lower limit, less than upper limit"""

    GELE = "gele"
    """Greater or equal than lower limit, less or equal than upper limit"""

    GELT = "gelt"
    """Greater or equal than lower limit, less than upper limit"""

    GTLE = "gtle"
    """Greater than lower limit, less or equal than upper limit"""

    LTGT = "ltgt"
    """Less than lower limit or greater than upper limit"""

    LEGE = "lege"
    """Less or equal than lower limit or greater or equal than upper limit"""

    LEGT = "legt"
    """Less or equal than lower limit or greater than upper limit"""

    LTGE = "ltge"
    """Less than lower limit or greater or equal than upper limit"""

class ChartType(str, Enum):
    """Chart type."""

    LINE = "line"
    LINE_LOG_X = "line_log_x"
    LINE_LOG_Y = "line_log_y"
    LOG_X_Y = "log_x_y"
