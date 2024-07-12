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
    """Dialog box widget."""

    widget_type: DialogBoxWidgetType
    widget_info: dict


@dataclass
class DialogBoxData:
    """Dialog box data.

    Args:
        title_bar (str): title bar
        dialog_text (str): dialog text
        widget_info (DialogBoxWidget | None): widget info
    """

    title_bar: str | None
    dialog_text: str
    widget_info: DialogBoxWidget | None
