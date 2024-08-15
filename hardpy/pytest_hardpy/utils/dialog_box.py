# Copyright (c) 2024 Everypin
# GNU General Public License v3.0 (see LICENSE or https://www.gnu.org/licenses/gpl-3.0.txt)

import base64
from dataclasses import dataclass, asdict
from enum import Enum
from typing import Any

from hardpy.pytest_hardpy.utils.exception import WidgetInfoError


class DialogBoxWidgetType(Enum):
    """Dialog box widget type."""

    TEXT_INPUT = "textinput"
    NUMERIC_INPUT = "numericinput"
    RADIOBUTTON = "radiobutton"
    CHECKBOX = "checkbox"
    IMAGE = "image"


@dataclass
class IWidgetInfo:
    """Widget info interface."""

    ...  # noqa: WPS604


@dataclass
class RadiobuttonInfo(IWidgetInfo):
    """Radiobutton info.

    Args:
        fields (list[str]): list of radiobutton fields.
    """

    fields: list[str]

    def __post_init__(self):
        """Validate the fields.

        Raises:
            ValueError: If the fields list is empty.
        """
        if not self.fields:
            raise ValueError("RadiobuttonInfo must have at least one field")


@dataclass
class CheckboxInfo(IWidgetInfo):
    """Checkbox info.

    Args:
        fields (list[str]): list of checkbox fields.
    """

    fields: list[str]

    def __post_init__(self):
        """Validate the fields.

        Raises:
            ValueError: If the fields list is empty.
        """
        if not self.fields:
            raise ValueError("CheckboxInfo must have at least one field")


@dataclass
class ImageInfo(IWidgetInfo):
    """Image info.

    Args:
        address (str): image address
        format (str): image format
        width (int): image width
        base64 (str | None): image base64

    Raises:
        WidgetInfoError: If both address and base64 are specified.
        WidgetInfoError: If the width is not positive.

    Notes:
        The base64 field is optional. If it is not specified, the image is read
        from the file at the specified address.
    """

    address: str
    format: str = "image"
    width: int = 100
    base64: str | None = None

    def __post_init__(self):
        """Validate the image fields and defines the base64 if it does not exist.

        Raises:
            WidgetInfoError: If both address and base64 are specified.
        """
        if self.address and self.base64:
            raise WidgetInfoError(
                "Either address or base64 must be specified, but not both"
            )
        if self.width < 1:
            raise WidgetInfoError("Width must be positive")
        if self.base64:
            return
        try:
            with open(self.address, "rb") as file:
                file_data = file.read()
        except FileNotFoundError:
            raise WidgetInfoError("The image address is invalid")
        self.base64 = base64.b64encode(file_data).decode("utf-8")  # noqa: WPS601


@dataclass
class DialogBoxWidget:
    """Dialog box widget.

    Args:
        type (DialogBoxWidgetType): widget type
        info (Union[RadiobuttonInfo, CheckboxInfo, ImageInfo, None]): widget info
    """

    type: DialogBoxWidgetType
    info: IWidgetInfo | None = None


@dataclass
class DialogBox:
    """Dialog box data.

    Args:
        dialog_text (str): dialog text
        title_bar (str | None): title bar
        widget (DialogBoxWidget | None): widget info
    """

    dialog_text: str
    title_bar: str | None = None
    widget: DialogBoxWidget | None = None


def generate_dialog_box_dict(dialog_box_data: DialogBox) -> dict:
    """Generate dialog box dictionary.

    Args:
        dialog_box_data (DialogBox): dialog box data

    Returns:
        dict: dialog box dictionary
    """
    if dialog_box_data.widget is None:
        return asdict(dialog_box_data)
    _validate_widget_info(dialog_box_data.widget)

    def _enum_to_value(data):
        def convert_value(obj):
            if isinstance(obj, Enum):
                return obj.value
            return obj

        return {k: convert_value(v) for k, v in data}

    return asdict(dialog_box_data, dict_factory=_enum_to_value)


def get_dialog_box_data(input_data: str, widget: DialogBoxWidget | None) -> Any:
    """Get the dialog box data in the correct format.

    Args:
        input_data (str): input string
        widget (DialogBoxWidget | None): widget info

    Returns:
        Any: Dialog box data in the correct format

    Raises:
        ValueError: If the widget.type is empty.
    """
    if widget is None:
        return None

    if widget.type is None:
        raise ValueError("Widget type is `None`, but widget data is not empty")

    dbx_answer = None

    match widget.type:
        case DialogBoxWidgetType.NUMERIC_INPUT:
            try:
                dbx_answer = float(input_data)
            except ValueError:
                dbx_answer = None
        case DialogBoxWidgetType.TEXT_INPUT:
            dbx_answer = input_data
        case DialogBoxWidgetType.RADIOBUTTON:
            dbx_answer = input_data
        case DialogBoxWidgetType.CHECKBOX:
            dbx_answer = input_data
        case _:
            pass  # noqa: WPS420

    return dbx_answer


def _validate_widget_info(widget: DialogBoxWidget) -> None:
    """
    Validate the information associated with the given widget.

    Args:
        widget (DialogBoxWidget): The widget to validate.

    Raises:
        WidgetInfoError: If the widget type is not supported or the info object
            is not of the expected type for the widget type.
    """
    widget_type_to_info = {
        DialogBoxWidgetType.TEXT_INPUT: None,
        DialogBoxWidgetType.NUMERIC_INPUT: None,
        DialogBoxWidgetType.RADIOBUTTON: RadiobuttonInfo,
        DialogBoxWidgetType.CHECKBOX: CheckboxInfo,
        DialogBoxWidgetType.IMAGE: ImageInfo,
    }

    if widget.type not in widget_type_to_info:
        raise WidgetInfoError(f"Unsupported widget type: {widget.type}")

    expected_info = widget_type_to_info[widget.type]

    if expected_info is not None and not isinstance(widget.info, expected_info):
        raise WidgetInfoError(f"Expected {expected_info.__name__} for widget info")
    elif expected_info is None and widget.info is not None:
        raise WidgetInfoError("Expected None for widget info")

