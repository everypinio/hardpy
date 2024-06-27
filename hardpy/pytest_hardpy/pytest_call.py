# Copyright (c) 2024 Everypin
# GNU General Public License v3.0 (see LICENSE or https://www.gnu.org/licenses/gpl-3.0.txt)

from enum import Enum
from os import environ
from dataclasses import dataclass
from typing import Optional
from uuid import uuid4

from pycouchdb.exceptions import NotFound
from pydantic import ValidationError

from hardpy.pytest_hardpy.db import (
    DatabaseField as DF,
    ResultRunStore,
    RunStore,
)
from hardpy.pytest_hardpy.utils import DuplicateSerialNumberError
from hardpy.pytest_hardpy.reporter import RunnerReporter


@dataclass
class CurrentTestInfo(object):
    """Current test info."""

    module_id: str
    case_id: str


class DialogBoxWidgetType(Enum):
    """Dialog box widget type."""

    RADIOBUTTON = "radiobutton"
    CHECKBOX = "checkbox"
    TEXT_INPUT = "textinput"
    NUMERIC_INPUT = "numericinput"


class DialogBoxWidget:
    """Dialog box widget."""

    widget_type: DialogBoxWidgetType
    widget_info: dict | tuple


@dataclass
class DialogBoxData:
    """Dialog box data.

    Args:
        title_bar (str): title bar
        dialog_text (str): dialog text
        widget_info (DialogBoxWidget | None): widget info
    """

    title_bar: str
    dialog_text: str
    widget_info: DialogBoxWidget | None


class DialogBoxResponse:
    """Represents the response from a dialog box."""

    def __init__(self, action: str, input_data: str | None = None):
        self.action = action
        self.input_data = input_data


def get_current_report() -> ResultRunStore | None:
    """Get current report from runstore database.

    Returns:
        ResultRunStore | None: report, or None if not found or invalid
    """
    runstore = RunStore()
    try:
        return runstore.get_document()
    except NotFound:
        return None
    except ValidationError:
        return None
    except TypeError:
        return None


def set_dut_info(info: dict):
    """Add DUT info to document.

    Args:
        info (dict): DUT info
    """
    reporter = RunnerReporter()
    for dut_key, dut_value in info.items():
        key = reporter.generate_key(DF.DUT, DF.INFO, dut_key)
        reporter.set_doc_value(key, dut_value)
    reporter.update_db_by_doc()


def set_dut_serial_number(serial_number: str):
    """Add DUT serial number to document.

    Args:
        serial_number (str): DUT serial number

    Raises:
        DuplicateSerialNumberError: if serial number is already set
    """
    reporter = RunnerReporter()
    key = reporter.generate_key(DF.DUT, DF.SERIAL_NUMBER)
    if reporter.get_field(key):
        raise DuplicateSerialNumberError
    reporter.set_doc_value(key, serial_number)
    reporter.update_db_by_doc()


def set_stand_info(info: dict):
    """Add test stand info to document.

    Args:
        info (dict): test stand info
    """
    reporter = RunnerReporter()
    for stand_key, stand_value in info.items():
        key = reporter.generate_key(DF.TEST_STAND, stand_key)
        reporter.set_doc_value(key, stand_value)
    reporter.update_db_by_doc()


def set_message(msg: str, msg_key: Optional[str] = None) -> None:
    """Add or update message in current test.

    Args:
        msg (str): Message content.
        msg_key (Optional[str]): Message ID.
                                     If not specified, a random ID will be generated.
    """
    current_test = _get_current_test()
    reporter = RunnerReporter()

    if msg_key is None:
        msg_key = str(uuid4())

    key = reporter.generate_key(
        DF.MODULES,
        current_test.module_id,
        DF.CASES,
        current_test.case_id,
        DF.MSG,
    )

    msgs = reporter.get_field(key)
    if msgs is None:
        msgs = {}

    msgs[msg_key] = msg

    reporter.set_doc_value(key, msgs)
    reporter.update_db_by_doc()


def set_case_artifact(data: dict):
    """Add data to current test case.

    Artifact saves only in RunStore database
    because state in StateStore and case artifact must be separated.

    Args:
        data (dict): data
    """
    current_test = _get_current_test()
    reporter = RunnerReporter()
    for stand_key, stand_value in data.items():
        key = reporter.generate_key(
            DF.MODULES,
            current_test.module_id,
            DF.CASES,
            current_test.case_id,
            DF.ARTIFACT,
            stand_key,
        )
        reporter.set_doc_value(key, stand_value, runstore_only=True)
    reporter.update_db_by_doc()


def set_module_artifact(data: dict):
    """Add data to current test module.

    Artifact saves only in RunStore database
    because state in StateStore and module artifact must be separated.

    Args:
        data (dict): data
    """
    current_test = _get_current_test()
    reporter = RunnerReporter()
    for artifact_key, artifact_value in data.items():
        key = reporter.generate_key(
            DF.MODULES,
            current_test.module_id,
            DF.ARTIFACT,
            artifact_key,
        )
        reporter.set_doc_value(key, artifact_value, runstore_only=True)
    reporter.update_db_by_doc()


def set_run_artifact(data: dict):
    """Add data to current test run.

    Artifact saves only in RunStore database
    because state in StateStore and run artifact must be separated.

    Args:
        data (dict): data
    """
    reporter = RunnerReporter()
    for artifact_key, artifact_value in data.items():
        key = reporter.generate_key(
            DF.ARTIFACT,
            artifact_key,
        )
        reporter.set_doc_value(key, artifact_value, runstore_only=True)
    reporter.update_db_by_doc()


def set_driver_info(drivers: dict) -> None:
    """Adds or updates drivers data.

    Driver data is stored in both StateStore and RunStore databases.

    Args:
        drivers (dict): A dictionary of drivers, where keys are driver names
                        and values are driver-specific data.
    """
    reporter = RunnerReporter()

    for driver_name, driver_data in drivers.items():
        key = reporter.generate_key(
            DF.DRIVERS,
            driver_name,
        )
        reporter.set_doc_value(key, driver_data)
    reporter.update_db_by_doc()


def run_dialog_box(data: DialogBoxData):
    """Displays a dialog box and updates the 'dialog_box' field in the statestore database.

    Args:
        title_bar (str): The title of the dialog box.
        dialog_text (str): The main text of the dialog box, which the operator will read.
        widget_info (DialogBoxWidget | None): Individual information for each dialog box type.

    Returns:
        DialogBoxResponse: An object containing the user's response.

    Raises:
        ValueError: If the 'message' argument is empty.
    """

    if not data.dialog_text:
        raise ValueError("The 'dialog_text' argument cannot be empty.")

    dialog_box = DialogBoxData(
        title_bar=data.title_bar,
        dialog_text=data.dialog_text,
        widget_info=data.widget_info,
    )

    user_response = {
        "action": "ok",  # Possible actions: "ok", "cancel", "other"
        "input_data": "This is the user's input",
    }

    response = DialogBoxResponse(
        action=user_response["action"],
        input_data=user_response.get("input_data"),
    )

    current_test = _get_current_test()
    reporter = RunnerReporter()
    key = reporter.generate_key(
        DF.MODULES,
        current_test.module_id,
        DF.CASES,
        current_test.case_id,
        DF.DIALOG_BOX,
    )
    reporter.set_doc_value(key, dialog_box)
    reporter.update_db_by_doc()

    return response


def _get_current_test() -> CurrentTestInfo:
    current_node = environ.get("PYTEST_CURRENT_TEST")

    if current_node is None:
        raise RuntimeError("PYTEST_CURRENT_TEST variable is not set")

    module_delimiter = ".py::"
    module_id_end_index = current_node.find(module_delimiter)
    module_id = current_node[:module_id_end_index]

    folder_delimeter = "/"
    folder_delimeter_index = current_node.rfind(folder_delimeter)
    if folder_delimeter_index != -1:
        module_id = module_id[folder_delimeter_index + 1 :]

    case_with_stage = current_node[module_id_end_index + len(module_delimiter) :]
    case_delimiter = " "
    case_id_end_index = case_with_stage.find(case_delimiter)
    case_id = case_with_stage[:case_id_end_index]

    return CurrentTestInfo(module_id=module_id, case_id=case_id)
