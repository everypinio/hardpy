# Copyright (c) 2025 Everypin
# GNU General Public License v3.0 (see LICENSE or https://www.gnu.org/licenses/gpl-3.0.txt)

from enum import Enum


class DatabaseField(str, Enum):
    """Database field."""

    # common
    NAME = "name"
    USER = "user"
    BATCH_SN = "batch_serial_number"
    CAUSED_DUT_FAILURE_ID = "caused_dut_failure_id"
    GROUP = "group"
    ERROR_CODE = "error_code"
    STATUS = "status"
    START_TIME = "start_time"
    STOP_TIME = "stop_time"
    NUMBER = "number"
    REVISION = "revision"
    INFO = "info"
    TIMEZONE = "timezone"
    MSG = "msg"
    ASSERTION_MSG = "assertion_msg"
    PART_NUMBER = "part_number"
    SERIAL_NUMBER = "serial_number"
    SUB_UNITS = "sub_units"
    ATTEMPT = "attempt"
    LOCATION = "location"
    HW_ID = "hw_id"
    DRIVERS = "drivers"
    TYPE = "type"
    CHART = "chart"

    # table name
    DUT = "dut"
    TEST_STAND = "test_stand"
    PROCESS = "process"

    # collection
    MODULES = "modules"
    CASES = "cases"
    INSTRUMENTS = "instruments"
    MEASUREMENTS = "measurements"

    # statestore
    PROGRESS = "progress"
    DIALOG_BOX = "dialog_box"
    OPERATOR_MSG = "operator_msg"
    FONT_SIZE = "font_size"
    ALERT = "alert"
    OPERATOR_DATA = "operator_data"
    DIALOG = "dialog"
    VISIBLE = "visible"
    TITLE = "title"
    IMAGE = "image"
    HTML = "html"
    ID = "id"

    # runstore
    ARTIFACT = "artifact"
