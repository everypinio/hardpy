# Copyright (c) 2024 Everypin
# GNU General Public License v3.0 (see LICENSE or https://www.gnu.org/licenses/gpl-3.0.txt)

from enum import Enum
from dataclasses import dataclass
from typing import Any


class DialogBoxWidgetType(Enum):
    """Dialog box widget type."""

    RADIOBUTTON = "radiobutton"
    CHECKBOX = "checkbox"
    TEXT_INPUT = "textinput"
    NUMERIC_INPUT = "numericinput"
    IMAGE = "image"


@dataclass
class DialogBoxWidget:
    """Dialog box widget.

    Args:
        type (DialogBoxWidgetType): widget type
        info (dict | None): widget info
    """

    type: DialogBoxWidgetType
    info: dict | None = None


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
        data_dict = {
            "title_bar": dialog_box_data.title_bar,
            "dialog_text": dialog_box_data.dialog_text,
            "widget": None,
        }
    else:
        data_dict = {
            "title_bar": dialog_box_data.title_bar,
            "dialog_text": dialog_box_data.dialog_text,
            "widget": {
                "info": dialog_box_data.widget.info,
                "type": dialog_box_data.widget.type.value,
            },
        }
    return data_dict


def get_dialog_box_data(input_data: str, widget: DialogBoxWidget | None) -> Any:
    """Get the dialog box data in the correct format.

    Args:
        input_data (str): input string
        widget (DialogBoxWidget | None): widget info

    Returns:
        Any: Dialog box data in the correct format
    """
    if widget is None:
        return None

    if widget.type is None:
        raise ValueError("Widget type is `None`, but widget data is not empty")

    match widget.type:
        case DialogBoxWidgetType.NUMERIC_INPUT:
            try:
                return float(input_data)
            except ValueError:
                return None
        case DialogBoxWidgetType.TEXT_INPUT:
            return input_data
        case DialogBoxWidgetType.RADIOBUTTON:
            try:
                return input_data
            except ValueError:
                return None
        case DialogBoxWidgetType.CHECKBOX:
            try:
                return input_data
            except ValueError:
                return None
        case _:
            return None
