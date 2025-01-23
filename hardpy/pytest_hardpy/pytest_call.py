# Copyright (c) 2024 Everypin
# GNU General Public License v3.0 (see LICENSE or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import annotations

import socket
from dataclasses import dataclass
from os import environ
from select import select
from typing import Any
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
    ConnectionData,
    DialogBox,
    DuplicatePartNumberError,
    DuplicateSerialNumberError,
    DuplicateTestStandLocationError,
    DuplicateTestStandNameError,
    ImageComponent,
)


@dataclass
class CurrentTestInfo:
    """Current test info."""

    module_id: str
    case_id: str


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


def set_dut_info(info: dict) -> None:
    """Add DUT info to document.

    Args:
        info (dict): DUT info
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
        DuplicateSerialNumberError: if serial number is already set
    """
    reporter = RunnerReporter()
    key = reporter.generate_key(DF.DUT, DF.SERIAL_NUMBER)
    if reporter.get_field(key):
        raise DuplicateSerialNumberError
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
        DuplicatePartNumberError: if part number is already set
    """
    reporter = RunnerReporter()
    key = reporter.generate_key(DF.DUT, DF.PART_NUMBER)
    if reporter.get_field(key):
        raise DuplicatePartNumberError
    reporter.set_doc_value(key, part_number)
    reporter.update_db_by_doc()


def set_stand_name(name: str) -> None:
    """Add test stand name to document.

    Args:
        name (str): test stand name

    Raises:
        DuplicateTestStandNameError: if test stand name is already set
    """
    reporter = RunnerReporter()
    key = reporter.generate_key(DF.TEST_STAND, DF.NAME)
    if reporter.get_field(key):
        raise DuplicateTestStandNameError
    reporter.set_doc_value(key, name)
    reporter.update_db_by_doc()


def set_stand_info(info: dict) -> None:
    """Add test stand info to document.

    Args:
        info (dict): test stand info
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
    """
    reporter = RunnerReporter()
    key = reporter.generate_key(DF.TEST_STAND, DF.LOCATION)
    if reporter.get_field(key):
        raise DuplicateTestStandLocationError
    reporter.set_doc_value(key, location)
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
    current_test = _get_current_test()
    reporter = RunnerReporter()
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

    # get socket data
    input_dbx_data = _get_socket_raw_data()

    _cleanup_widget(reporter, key)
    return dialog_box_data.widget.convert_data(input_dbx_data)


def set_operator_message(
    msg: str,
    title: str | None = None,
    block: bool = True,
    image: ImageComponent | None = None,
    font_size: int = 14,
) -> None:
    """Set operator message.

    The function should be used to handle events outside of testing.
    For messages to the operator during testing, there is the function `run_dialog_box`.

    Args:
        msg (str): message
        title (str | None): title
        image (ImageComponent | None): operator message info
        block (bool): if True, the function will block until the message is closed
        font_size (int): font size
    """
    reporter = RunnerReporter()
    key = reporter.generate_key(DF.OPERATOR_MSG)
    _cleanup_widget(reporter, key)

    if font_size < 1:
        msg = "The 'font_size' argument cannot be less than 1"
        raise ValueError(msg)

    msg_data = {
        DF.MSG: msg,
        DF.TITLE: title,
        DF.VISIBLE: True,
        DF.IMAGE: image.to_dict() if image else None,
        DF.ID: str(uuid4()),
        DF.FONT_SIZE: int(font_size),
    }
    reporter.set_doc_value(key, msg_data, statestore_only=True)
    reporter.update_db_by_doc()

    if block:
        # get socket data
        is_msg_visible = _get_socket_raw_data()

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
        msg = "PYTEST_CURRENT_TEST variable is not set"
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


def _get_socket_raw_data() -> str:
    # create socket connection
    with socket.socket() as server:
        server.setblocking(False)
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        con_data = ConnectionData()
        try:
            server.bind((con_data.socket_host, con_data.socket_port))
        except OSError as exc:
            msg = "Socket creating error"
            server.close()
            raise RuntimeError(msg) from exc
        server.listen(1)

        client = None
        while True:
            ready_to_read, _, _ = select([server], [], [], 0.5)
            if ready_to_read:
                client, _ = server.accept()
                break

        # receive data
        max_input_data_len = 1024
        socket_data = client.recv(max_input_data_len).decode("utf-8")

        # close connection
        client.close()
        server.close()

        return socket_data


def _cleanup_widget(reporter: RunnerReporter, key: str) -> None:
    reporter.set_doc_value(key, {}, statestore_only=True)
    reporter.update_db_by_doc()
