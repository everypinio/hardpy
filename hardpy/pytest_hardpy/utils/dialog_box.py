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


@dataclass
class DialogBoxWidget:
    """Dialog box widget.

    Args:
        widget_type (DialogBoxWidgetType): widget type
        widget_info (dict): widget info
    """

    widget_type: DialogBoxWidgetType
    widget_info: dict


@dataclass
class DialogBoxData:
    """Dialog box data.

    Args:
        dialog_text (str): dialog text
        title_bar (str | None): title bar
        widget_info (DialogBoxWidget | None): widget info
    """

    dialog_text: str
    title_bar: str | None = None
    widget_info: DialogBoxWidget | None = None


def generate_dialog_box_dict(dialog_box_data: DialogBoxData) -> dict:
    """Generate dialog box dictionary.

    Args:
        dialog_box_data (DialogBoxData): dialog box data

    Returns:
        dict: dialog box dictionary
    """
    if dialog_box_data.widget_info is None:
        data_dict = {
            "title_bar": dialog_box_data.title_bar,
            "dialog_text": dialog_box_data.dialog_text,
            "widget_info": None,
        }
    else:
        data_dict = {
            "title_bar": dialog_box_data.title_bar,
            "dialog_text": dialog_box_data.dialog_text,
            "widget_info": {
                "info": dialog_box_data.widget_info.widget_info,
                "type": dialog_box_data.widget_info.widget_type.value,
            },
        }
    return data_dict


def get_dialog_box_data(
    input_data: str, widget_info: DialogBoxWidget | None
) -> Any:
    """Get the dialog box data in the correct format.

    Args:
        input_data (str): input string
        widget_info (DialogBoxWidget | None): widget info

    Returns:
        Any: Dialog box data in the correct format
    """
    if widget_info is None:
        return None

    if widget_info.widget_type is None:
        raise ValueError("Widget type is `None`, but widget data is not empty")

    match widget_info.widget_type:
        case DialogBoxWidgetType.NUMERIC_INPUT:
            try:
                return float(input_data)
            except ValueError:
                return None
        case DialogBoxWidgetType.TEXT_INPUT:
            return input_data
        case _:
            return None
