# Copyright (c) 2024 Everypin
# GNU General Public License v3.0 (see LICENSE or https://www.gnu.org/licenses/gpl-3.0.txt)

from hardpy.pytest_hardpy.result import CouchdbLoader
from hardpy.pytest_hardpy.utils import (
    DuplicateSerialNumberError,
    DuplicatePartNumberError,
    DuplicateTestStandNameError,
    DuplicateDialogBoxError,
)
from hardpy.pytest_hardpy.result.couchdb_config import CouchdbConfig
from hardpy.pytest_hardpy.utils import (
    DialogBox,
    TextInputWidget,
    NumericInputWidget,
    CheckboxWidget,
    RadiobuttonWidget,
    ImageWidget,
    StepWidget,
    MultistepWidget,
)
from hardpy.pytest_hardpy.pytest_call import (
    get_current_report,
    set_dut_info,
    set_dut_serial_number,
    set_dut_part_number,
    set_stand_name,
    set_stand_info,
    set_case_artifact,
    set_module_artifact,
    set_run_artifact,
    set_message,
    set_driver_info,
    run_dialog_box,
    set_operator_message,
)

__all__ = [
    # CouchDB
    "CouchdbLoader",
    "CouchdbConfig",
    "get_current_report",
    # Errors
    "DuplicateSerialNumberError",
    "DuplicatePartNumberError",
    "DuplicateTestStandNameError",
    "DuplicateDialogBoxError",
    # Database info
    "set_dut_info",
    "set_dut_serial_number",
    "set_dut_part_number",
    "set_stand_name",
    "set_stand_info",
    "set_case_artifact",
    "set_module_artifact",
    "set_run_artifact",
    "set_message",
    "set_driver_info",
    "set_operator_message",
    # Dialog boxes
    "run_dialog_box",
    "DialogBox",
    "TextInputWidget",
    "NumericInputWidget",
    "CheckboxWidget",
    "RadiobuttonWidget",
    "ImageWidget",
    "StepWidget",
    "MultistepWidget",
]
