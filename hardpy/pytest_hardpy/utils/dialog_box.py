# Copyright (c) 2024 Everypin
# GNU General Public License v3.0 (see LICENSE or https://www.gnu.org/licenses/gpl-3.0.txt)

from enum import Enum
from dataclasses import dataclass


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
        title_bar (str | None): title bar
        dialog_text (str): dialog text
        widget_info (DialogBoxWidget | None): widget info
    """

    title_bar: str | None
    dialog_text: str
    widget_info: DialogBoxWidget | None
