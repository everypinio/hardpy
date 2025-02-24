# Copyright (c) 2024 Everypin
# GNU General Public License v3.0 (see LICENSE or https://www.gnu.org/licenses/gpl-3.0.txt)

from enum import Enum


class DatabaseField(str, Enum):
    """Database field."""

    NAME = "name"
    STATUS = "status"
    START_TIME = "start_time"
    STOP_TIME = "stop_time"
    ASSERTION_MSG = "assertion_msg"
    MSG = "msg"
    MODULES = "modules"
    CASES = "cases"
    TIMEZONE = "timezone"
    PROGRESS = "progress"
    ARTIFACT = "artifact"
    DUT = "dut"
    PART_NUMBER = "part_number"
    INFO = "info"
    TEST_STAND = "test_stand"
    SERIAL_NUMBER = "serial_number"
    DRIVERS = "drivers"
    DIALOG_BOX = "dialog_box"
    OPERATOR_MSG = "operator_msg"
    ATTEMPT = "attempt"
    LOCATION = "location"
    HW_ID = "hw_id"
    TITLE = "title"
    VISIBLE = "visible"
    IMAGE = "image"
    ID = "id"
    FONT_SIZE = "font_size"
    ALERT = "alert"
