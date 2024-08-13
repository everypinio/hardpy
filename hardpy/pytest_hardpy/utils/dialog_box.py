# Copyright (c) 2024 Everypin
# GNU General Public License v3.0 (see LICENSE or https://www.gnu.org/licenses/gpl-3.0.txt)

from enum import Enum
from dataclasses import dataclass
from typing import Any, List, Optional, Union

from hardpy.pytest_hardpy.utils.exception import WidgetInfoError


class DialogBoxWidgetType(Enum):
    """Dialog box widget type."""

    RADIOBUTTON = "radiobutton"
    CHECKBOX = "checkbox"
    TEXT_INPUT = "textinput"
    NUMERIC_INPUT = "numericinput"


@dataclass
class RadiobuttonInfo:
    fields: List[str]


@dataclass
class CheckboxInfo:
    fields: List[str]


@dataclass
class DialogBoxWidget:
    """Dialog box widget.

    Args:
        type (DialogBoxWidgetType): widget type
        info (Union[RadiobuttonInfo, CheckboxInfo, None]): widget info
    """

    type: DialogBoxWidgetType
    info: Optional[Union[RadiobuttonInfo, CheckboxInfo]] = None


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

    Raises:
        WidgetInfoError: If the widget info is not correct.
    """
    try:
        if dialog_box_data.widget is None:
            data_dict = {
                "title_bar": dialog_box_data.title_bar,
                "dialog_text": dialog_box_data.dialog_text,
                "widget": None,
            }
            return data_dict
        _validate_widget_info(dialog_box_data.widget)
        if dialog_box_data.widget.type in [
            DialogBoxWidgetType.NUMERIC_INPUT,
            DialogBoxWidgetType.TEXT_INPUT,
        ]:
            data_dict = {
                "title_bar": dialog_box_data.title_bar,
                "dialog_text": dialog_box_data.dialog_text,
                "widget": {
                    "info": dialog_box_data.widget.info,
                    "type": dialog_box_data.widget.type.value,
                },
            }
        elif dialog_box_data.widget.type in [
            DialogBoxWidgetType.RADIOBUTTON,
            DialogBoxWidgetType.CHECKBOX,
        ]:
            widget_info = dialog_box_data.widget.info
            widget_data = {
                "info": {
                    "fields": [str(field) for field in widget_info.fields],
                },
                "type": dialog_box_data.widget.type.value,
            }
            data_dict = {
                "title_bar": dialog_box_data.title_bar,
                "dialog_text": dialog_box_data.dialog_text,
                "widget": widget_data,
            }
        return data_dict

    except (WidgetInfoError, ValueError) as e:
        raise WidgetInfoError(f"Invalid dialog box data: {e}")


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
        case _:
            raise WidgetInfoError(f"Unsupported widget type: {widget.type}")
