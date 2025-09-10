# Copyright (c) 2024 Everypin
# GNU General Public License v3.0 (see LICENSE or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import annotations

from dataclasses import dataclass
from inspect import stack
from os import environ
from time import sleep
from typing import TYPE_CHECKING, Any
from uuid import uuid4

from pycouchdb.exceptions import NotFound
from pydantic import ValidationError

from hardpy.pytest_hardpy.db import (
    DatabaseField as DF,  # noqa: N817
    ResultRunStore,
    RunStore,
)
from hardpy.pytest_hardpy.reporter import RunnerReporter
from hardpy.pytest_hardpy.utils import (
    Chart,
    DialogBox,
    DuplicateParameterError,
    HTMLComponent,
    ImageComponent,
    Instrument,
    NumericMeasurement,
    StringMeasurement,
    SubUnit,
    TestStandNumberError,
)

if TYPE_CHECKING:
    from collections.abc import Mapping


@dataclass
class CurrentTestInfo:
    """Current test info."""

    module_id: str
    case_id: str


class ErrorCodeMeta(type):
    """Error code metaclass."""

    def __call__(cls, code: int, message: str | None = None) -> str | None:
        """Add error code to document.

        Args:
            code (int): non-negative error code.
            message (str | None): error message.

        Returns:
            str | None: error message
        """
        if code < 0:
            msg = "error code must be greater than 0"
            raise ValueError(msg)
        reporter = RunnerReporter()
        key = reporter.generate_key(DF.ERROR_CODE)
        if reporter.get_field(key) is None:
            reporter.set_doc_value(key, code)
            reporter.update_db_by_doc()
        if message:  # noqa: RET503
            return message


class ErrorCode(metaclass=ErrorCodeMeta):
    """Save error code and return error message.

    It must be called from an assert.

    Args:
        code (int): error code.
        message (str): error message.
    """


def get_current_report() -> ResultRunStore | None:
    """Get current report from runstore database.

    Returns:
        ResultRunStore | None: report, or None if not found or invalid
    """
    runstore = RunStore()
    try:
        return runstore.get_document()  # type: ignore
    except NotFound:
        return None
    except ValidationError:
        return None
    except TypeError:
        return None


def set_user_name(name: str) -> None:
    """Set operator panel user name.

    Args:
        name (str): user name

    Raises:
        DuplicateParameterError: if user name is already set
    """
    reporter = RunnerReporter()
    key = reporter.generate_key(DF.USER)
    if reporter.get_field(key):
        msg = "user_name"
        raise DuplicateParameterError(msg)
    reporter.set_doc_value(key, name)
    reporter.update_db_by_doc()


def set_batch_serial_number(serial_number: str) -> None:
    """Add batch serial number to document.

    Args:
        serial_number (str): batch serial number

    Raises:
        DuplicateParameterError: if batch serial number is already set
    """
    reporter = RunnerReporter()
    key = reporter.generate_key(DF.BATCH_SN)
    if reporter.get_field(key):
        msg = "batch_serial_number"
        raise DuplicateParameterError(msg)
    reporter.set_doc_value(key, serial_number)
    reporter.update_db_by_doc()


def set_dut_sub_unit(sub_unit: SubUnit) -> int:
    """Add sub unit to DUT sub units list.

    Args:
        sub_unit (SubUnit): Sub unit object of DUT.

    Returns:
        int: sub unit index
    """
    reporter = RunnerReporter()
    key = reporter.generate_key(DF.DUT, DF.SUB_UNITS)

    sub_units = reporter.get_field(key) or []
    sub_units.append({k: v for k, v in vars(sub_unit).items() if v is not None})

    reporter.set_doc_value(key, sub_units)
    reporter.update_db_by_doc()

    return len(sub_units) - 1


def set_dut_info(info: Mapping[str, str | int | float]) -> None:
    """Set DUT info to document.

    Args:
        info (Mapping): DUT info
    """
    reporter = RunnerReporter()
    for dut_key, dut_value in info.items():
        key = reporter.generate_key(DF.DUT, DF.INFO, dut_key)
        reporter.set_doc_value(key, dut_value)
    reporter.update_db_by_doc()


def set_dut_serial_number(serial_number: str) -> None:
    """Add DUT serial number to document.

    Args:
        serial_number (str): DUT serial number

    Raises:
        DuplicateParameterError: if serial number is already set
    """
    reporter = RunnerReporter()
    key = reporter.generate_key(DF.DUT, DF.SERIAL_NUMBER)
    if reporter.get_field(key):
        msg = "dut_serial_number"
        raise DuplicateParameterError(msg)
    reporter.set_doc_value(
        key,
        serial_number if isinstance(serial_number, str) else str(serial_number),
    )
    reporter.update_db_by_doc()


def set_dut_part_number(part_number: str) -> None:
    """Add DUT part number to document.

    Args:
        part_number (str): DUT part number

    Raises:
        DuplicateParameterError: if part number is already set
    """
    reporter = RunnerReporter()
    key = reporter.generate_key(DF.DUT, DF.PART_NUMBER)
    if reporter.get_field(key):
        msg = "dut_part_number"
        raise DuplicateParameterError(msg)
    reporter.set_doc_value(key, part_number)
    reporter.update_db_by_doc()


def set_dut_name(name: str) -> None:
    """Set DUT name to document.

    Args:
        name (str): DUT name

    Raises:
        DuplicateParameterError: if DUT name is already set
    """
    reporter = RunnerReporter()
    key = reporter.generate_key(DF.DUT, DF.NAME)
    if reporter.get_field(key):
        msg = "dut_name"
        raise DuplicateParameterError(msg)
    reporter.set_doc_value(key, name)
    reporter.update_db_by_doc()


def set_dut_type(dut_type: str) -> None:
    """Set DUT type to document.

    Args:
        dut_type (str): DUT type

    Raises:
        DuplicateParameterError: if DUT type is already set
    """
    reporter = RunnerReporter()
    key = reporter.generate_key(DF.DUT, DF.TYPE)
    if reporter.get_field(key):
        msg = "dut_type"
        raise DuplicateParameterError(msg)
    reporter.set_doc_value(key, dut_type)
    reporter.update_db_by_doc()


def set_dut_revision(revision: str) -> None:
    """Set DUT revision to document.

    Args:
        revision (str): DUT revision

    Raises:
        DuplicateParameterError: if DUT revision is already set
    """
    reporter = RunnerReporter()
    key = reporter.generate_key(DF.DUT, DF.REVISION)
    if reporter.get_field(key):
        msg = "dut_revision"
        raise DuplicateParameterError(msg)
    reporter.set_doc_value(key, revision)
    reporter.update_db_by_doc()


def set_stand_name(name: str) -> None:
    """Add test stand name to document.

    Args:
        name (str): test stand name

    Raises:
        DuplicateParameterError: if test stand name is already set
    """
    reporter = RunnerReporter()
    key = reporter.generate_key(DF.TEST_STAND, DF.NAME)
    if reporter.get_field(key):
        msg = "stand_name"
        raise DuplicateParameterError(msg)
    reporter.set_doc_value(key, name)
    reporter.update_db_by_doc()


def set_stand_info(info: Mapping[str, str | int | float]) -> None:
    """Add test stand info to document.

    Args:
        info (Mapping[str, str | int | float ]): test stand info as a mapping
            where keys are strings and values can be strings, integers, floats objects
    """
    reporter = RunnerReporter()
    for stand_key, stand_value in info.items():
        key = reporter.generate_key(DF.TEST_STAND, DF.INFO, stand_key)
        reporter.set_doc_value(key, stand_value)
    reporter.update_db_by_doc()


def set_stand_location(location: str) -> None:
    """Add test stand location to document.

    Args:
        location (str): test stand location

    Raises:
        DuplicateParameterError: if test stand location is already set
    """
    reporter = RunnerReporter()
    key = reporter.generate_key(DF.TEST_STAND, DF.LOCATION)
    if reporter.get_field(key):
        msg = "stand_location"
        raise DuplicateParameterError(msg)
    reporter.set_doc_value(key, location)
    reporter.update_db_by_doc()


def set_stand_number(number: int) -> None:
    """Add test stand number to document.

    Args:
        number (int): test stand number (non negative integer)

    Raises:
        DuplicateParameterError: if stand number is already set
        TestStandNumberError: if stand number is incorrect (negative or non integer)
    """
    reporter = RunnerReporter()
    key = reporter.generate_key(DF.TEST_STAND, DF.NUMBER)
    if not isinstance(number, int) or number < 0:
        raise TestStandNumberError
    if reporter.get_field(key):
        msg = "stand_number"
        raise DuplicateParameterError(msg)
    reporter.set_doc_value(key, number)
    reporter.update_db_by_doc()


def set_stand_revision(revision: str) -> None:
    """Add test stand revision to document.

    Args:
        revision (str): test stand revision

    Raises:
        DuplicateParameterError: if test stand revision is already set
    """
    reporter = RunnerReporter()
    key = reporter.generate_key(DF.TEST_STAND, DF.REVISION)
    if reporter.get_field(key):
        msg = "stand_revision"
        raise DuplicateParameterError(msg)
    reporter.set_doc_value(key, revision)
    reporter.update_db_by_doc()


def set_message(msg: str, msg_key: str | None = None) -> None:
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


def set_case_artifact(data: dict) -> None:
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


def set_module_artifact(data: dict) -> None:
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


def set_run_artifact(data: dict) -> None:
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
    """Add or update test stand drivers data.

    Driver data is stored in both StateStore and RunStore databases.

    Args:
        drivers (dict): A dictionary of drivers, where keys are driver names
                        and values are driver-specific data.
    """
    reporter = RunnerReporter()

    for driver_name, driver_data in drivers.items():
        key = reporter.generate_key(
            DF.TEST_STAND,
            DF.DRIVERS,
            driver_name,
        )
        reporter.set_doc_value(key, driver_data)
    reporter.update_db_by_doc()


def set_instrument(instrument: Instrument) -> int:
    """Add instrument to test stand instruments list.

    Args:
        instrument (Instrument): Instrument object containing all instrument data

    Returns:
        int: instrument index
    """
    reporter = RunnerReporter()
    key = reporter.generate_key(DF.TEST_STAND, DF.INSTRUMENTS)

    instruments = reporter.get_field(key) or []
    instruments.append({k: v for k, v in vars(instrument).items() if v is not None})

    reporter.set_doc_value(key, instruments)
    reporter.update_db_by_doc()

    return len(instruments) - 1


def set_process_name(name: str) -> None:
    """Set process name to document.

    Args:
        name (str): process name

    Raises:
        DuplicateParameterError: if process name is already set
    """
    reporter = RunnerReporter()
    key = reporter.generate_key(DF.PROCESS, DF.NAME)
    if reporter.get_field(key):
        msg = "process_name"
        raise DuplicateParameterError(msg)
    reporter.set_doc_value(key, name)
    reporter.update_db_by_doc()


def set_process_number(number: int) -> None:
    """Set process number to document.

    Args:
        number (int): process number

    Raises:
        DuplicateParameterError: if process number is already set
    """
    reporter = RunnerReporter()
    key = reporter.generate_key(DF.PROCESS, DF.NUMBER)
    if reporter.get_field(key):
        msg = "process_number"
        raise DuplicateParameterError(msg)
    reporter.set_doc_value(key, number)
    reporter.update_db_by_doc()


def set_process_info(info: Mapping[str, str | int | float]) -> None:
    """Set process info to document.

    Args:
        info (Mapping): process info
    """
    reporter = RunnerReporter()
    for key, value in info.items():
        full_key = reporter.generate_key(DF.PROCESS, DF.INFO, key)
        reporter.set_doc_value(full_key, value)
    reporter.update_db_by_doc()


def set_case_measurement(measurement: NumericMeasurement | StringMeasurement) -> int:
    """Add measurement to document.

    Args:
        measurement (NumericMeasurement | StringMeasurement): measurement object

    Returns:
        int: measurement index from measurements list
    """
    current_test = _get_current_test()
    reporter = RunnerReporter()

    key = reporter.generate_key(
        DF.MODULES,
        current_test.module_id,
        DF.CASES,
        current_test.case_id,
        DF.MEASUREMENTS,
    )

    measurements = reporter.get_field(key) or []
    measurements.append({k: v for k, v in vars(measurement).items() if v is not None})

    reporter.set_doc_value(key, measurements)
    reporter.update_db_by_doc()

    return len(measurements) - 1


def set_case_chart(chart: Chart) -> None:
    """Add chart to document.

    Args:
        chart (Chart): chart object
    """
    if not chart.x_data or not chart.y_data:
        msg = "x_data and y_data must be set"
        raise ValueError(msg)
    current_test = _get_current_test()
    reporter = RunnerReporter()

    key = reporter.generate_key(
        DF.MODULES,
        current_test.module_id,
        DF.CASES,
        current_test.case_id,
        DF.CHART,
    )

    if reporter.get_field(key):
        msg = "chart"
        raise DuplicateParameterError(msg)

    chart_dict = {k: v for k, v in vars(chart).items() if v is not None}

    reporter.set_doc_value(key, chart_dict)
    reporter.update_db_by_doc()


def run_dialog_box(dialog_box_data: DialogBox) -> Any:  # noqa: ANN401
    """Display a dialog box.

    Args:
        dialog_box_data (DialogBox): Data for creating the dialog box.

        DialogBox attributes:

        - dialog_text (str): The text of the dialog box.
        - title_bar (str | None): The title bar of the dialog box.
          If the title_bar field is missing, it is the case name.
        - widget (DialogBoxWidget | None): Widget information.
        - image (ImageComponent | None): Image information.
        - html (HTMLComponent | None): HTML information.

    Returns:
        Any: An object containing the user's response.

        The type of the return value depends on the widget type:

        - BASE: bool.
        - TEXT_INPUT: str.
        - NUMERIC_INPUT: float.
        - RADIOBUTTON: str.
        - CHECKBOX: list[str].
        - MULTISTEP: bool.

    Raises:
        ValueError: If the 'message' argument is empty.
    """
    if not dialog_box_data.dialog_text:
        msg = "The 'dialog_text' argument cannot be empty."
        raise ValueError(msg)
    reporter = RunnerReporter()
    current_test = _get_current_test()
    key = reporter.generate_key(
        DF.MODULES,
        current_test.module_id,
        DF.CASES,
        current_test.case_id,
        DF.DIALOG_BOX,
    )
    _cleanup_widget(reporter, key)

    reporter.set_doc_value(key, dialog_box_data.to_dict(), statestore_only=True)
    reporter.update_db_by_doc()

    input_dbx_data = _get_operator_data()

    _cleanup_widget(reporter, key)
    return dialog_box_data.widget.convert_data(input_dbx_data)


def set_operator_message(  # noqa: PLR0913
    msg: str,
    title: str | None = None,
    block: bool = True,
    image: ImageComponent | None = None,
    html: HTMLComponent | None = None,
    font_size: int = 14,
) -> None:
    """Set operator message.

    The function should be used to handle events outside of testing.
    For messages to the operator during testing, there is the function `run_dialog_box`.

    Args:
        msg (str): message
        title (str | None): title
        image (ImageComponent | None): operator message image
        html (HTMLComponent | None): operator message html page
        block (bool): if True, the function will block until the message is closed
        font_size (int): font size
    """
    reporter = RunnerReporter()
    key = reporter.generate_key(DF.OPERATOR_MSG)
    _cleanup_widget(reporter, key)

    if font_size < 1:
        msg = "The 'font_size' argument cannot be less than 1"
        raise ValueError(msg)

    if not msg:
        msg = "The 'msg' argument cannot be empty"
        raise ValueError(msg)

    msg_data = {
        DF.MSG: msg,
        DF.TITLE: title,
        DF.VISIBLE: True,
        DF.IMAGE: image.to_dict() if image else None,
        DF.HTML: html.to_dict() if html else None,
        DF.ID: str(uuid4()),
        DF.FONT_SIZE: int(font_size),
    }
    reporter.set_doc_value(key, msg_data, statestore_only=True)
    reporter.update_db_by_doc()

    if block:
        is_msg_visible = _get_operator_data()
        msg_data[DF.VISIBLE] = is_msg_visible

        reporter.set_doc_value(key, msg_data, statestore_only=True)
        reporter.update_db_by_doc()

        _cleanup_widget(reporter, key)


def clear_operator_message() -> None:
    """Clear operator message.

    Clears the current message to the operator if it exists, otherwise does nothing.
    """
    reporter = RunnerReporter()
    key = reporter.generate_key(DF.OPERATOR_MSG)

    _cleanup_widget(reporter, key)


def get_current_attempt() -> int:
    """Get current attempt.

    Returns:
        int: current attempt
    """
    reporter = RunnerReporter()
    module_id, case_id = _get_current_test().module_id, _get_current_test().case_id
    return reporter.get_current_attempt(module_id, case_id)


def _get_current_test() -> CurrentTestInfo:
    current_node = environ.get("PYTEST_CURRENT_TEST")

    if current_node is None:
        reporter = RunnerReporter()
        caller = stack()[1].function
        msg = f"Function {caller} can't be called outside of the test."
        reporter.set_alert(msg)
        raise RuntimeError(msg)

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


def _get_operator_data() -> str:
    """Get operator panel data.

    Returns:
        str: operator panel data
    """
    reporter = RunnerReporter()

    data = ""
    key = reporter.generate_key(DF.OPERATOR_DATA, DF.DIALOG)
    while not data:
        reporter.update_doc_by_db()

        data = reporter.get_field(key)
        if data:
            reporter.set_doc_value(key, "", statestore_only=True)
            break
        sleep(0.1)
    return data


def _cleanup_widget(reporter: RunnerReporter, key: str) -> None:
    reporter.set_doc_value(key, {}, statestore_only=True)
    reporter.update_db_by_doc()
