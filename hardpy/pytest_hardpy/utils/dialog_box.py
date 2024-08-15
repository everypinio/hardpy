# Copyright (c) 2024 Everypin
# GNU General Public License v3.0 (see LICENSE or https://www.gnu.org/licenses/gpl-3.0.txt)

from enum import Enum
import base64
import re
from dataclasses import dataclass, asdict
from typing import Any, List, Optional, Union

from hardpy.pytest_hardpy.utils.exception import WidgetInfoError


class DialogBoxWidgetType(Enum):
    """Dialog box widget type."""

    TEXT_INPUT = "textinput"
    NUMERIC_INPUT = "numericinput"
    RADIOBUTTON = "radiobutton"
    CHECKBOX = "checkbox"
    IMAGE = "image"


@dataclass
class RadiobuttonInfo:
    fields: List[str]

    def __post_init__(self):
        if not self.fields:
            raise ValueError("RadiobuttonInfo must have at least one field")


@dataclass
class CheckboxInfo:
    fields: List[str]

    def __post_init__(self):
        if not self.fields:
            raise ValueError("CheckboxInfo must have at least one field")


@dataclass
class ImageInfo:
    image_address: str


@dataclass
class ImageInfoAfterEncode:
    image_data: str
    image_format: str


@dataclass
class DialogBoxWidget:
    """Dialog box widget.

    Args:
        type (DialogBoxWidgetType): widget type
        info (Union[RadiobuttonInfo, CheckboxInfo, ImageInfo, ImageInfoAfterEncode, None]): widget info
    """

    type: DialogBoxWidgetType
    info: Optional[Union[RadiobuttonInfo, CheckboxInfo, ImageInfo, ImageInfoAfterEncode]] = None


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
    if dialog_box_data.widget.type == DialogBoxWidgetType.IMAGE:
        widget_info = dialog_box_data.widget.info
        default_image_path = "assets/test.jpg"

        try:
            with open(
                widget_info.image_address if widget_info else default_image_path, "rb"
            ) as file:
                file_data = file.read()
                base64_data = base64.b64encode(file_data)
                base64_string = base64_data.decode("utf-8")
            match = re.search(r".+\.(\w+)", base64_string)
            image_format = match.group(1) if match else "jpg"
            dialog_box_data.widget.info = ImageInfoAfterEncode(
                image_data=base64_string, image_format=image_format
            )
        except FileNotFoundError:
            raise WidgetInfoError("The image address is invalid")

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
    match widget.type:
        case DialogBoxWidgetType.TEXT_INPUT:
            if widget.info:
                raise WidgetInfoError("Expected None for widget info")
        case DialogBoxWidgetType.NUMERIC_INPUT:
            if widget.info:
                raise WidgetInfoError("Expected None for widget info")
        case DialogBoxWidgetType.RADIOBUTTON:
            if not isinstance(widget.info, RadiobuttonInfo):
                raise WidgetInfoError("Expected RadiobuttonInfo for widget info")
        case DialogBoxWidgetType.CHECKBOX:
            if not isinstance(widget.info, CheckboxInfo):
                raise WidgetInfoError("Expected CheckboxInfo for widget info")
        case DialogBoxWidgetType.IMAGE:
            if not isinstance(widget.info, ImageInfo):
                raise WidgetInfoError("Expected ImageInfo for widget info")
        case _:
            raise WidgetInfoError(f"Unsupported widget type: {widget.type}")
