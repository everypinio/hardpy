# Copyright (c) 2024 Everypin
# GNU General Public License v3.0 (see LICENSE or https://www.gnu.org/licenses/gpl-3.0.txt)

import base64
from abc import ABC, abstractmethod
from ast import literal_eval
from copy import deepcopy
from dataclasses import dataclass
from enum import Enum
from typing import Any, Final

from hardpy.pytest_hardpy.utils.exception import WidgetInfoError


class WidgetType(Enum):
    """Dialog box widget type."""

    BASE = "base"
    TEXT_INPUT = "textinput"
    NUMERIC_INPUT = "numericinput"
    RADIOBUTTON = "radiobutton"
    CHECKBOX = "checkbox"
    IMAGE = "image"
    STEP = "step"
    MULTISTEP = "multistep"


class IWidget(ABC):
    """Dialog box widget interface."""

    def __init__(self, widget_type: WidgetType):
        self.type: Final[str] = widget_type.value
        self.info: dict = {}

    @abstractmethod
    def convert_data(self, input_data: str | None) -> Any | None:
        """Get the widget data in the correct format.

        Args:
            input_data (str | None): input string or nothing.

        Returns:
            Any: Widget data in the correct format
        """
        raise NotImplementedError


class BaseWidget(IWidget):
    """Widget info interface."""

    def __init__(self, widget_type: WidgetType = WidgetType.BASE):
        super().__init__(WidgetType.BASE)

    def convert_data(self, input_data: str | None = None) -> bool:  # noqa: WPS324
        """Get base widget data, i.e. None.

        Args:
            input_data (str): input string

        Returns:
            bool: True if confirm button is pressed
        """
        return True


class TextInputWidget(IWidget):
    """Text input widget."""

    def __init__(self):
        """Initialize the TextInputWidget."""
        super().__init__(WidgetType.TEXT_INPUT)

    def convert_data(self, input_data: str) -> str:
        """Get the text input data in the string format.

        Args:
            input_data (str): input string

        Returns:
            str: Text input string data
        """
        return input_data


class NumericInputWidget(IWidget):
    """Numeric input widget."""

    def __init__(self):
        """Initialize the NumericInputWidget."""
        super().__init__(WidgetType.NUMERIC_INPUT)

    def convert_data(self, input_data: str) -> float | None:
        """Get the numeric widget data in the correct format.

        Args:
            input_data (str): input string

        Returns:
            float | None: Numeric data or None if the input is not a number
        """
        try:
            return float(input_data)
        except ValueError:
            return None


class RadiobuttonWidget(IWidget):
    """Radiobutton widget."""

    def __init__(self, fields: list[str]):
        """Initialize the RadiobuttonWidget.

        Args:
            fields (list[str]): Radiobutton fields.

        Raises:
            ValueError: If the fields list is empty.
        """
        super().__init__(WidgetType.RADIOBUTTON)
        if not fields:
            raise ValueError("RadiobuttonWidget must have at least one field")
        self.info["fields"] = fields

    def convert_data(self, input_data: str) -> str:
        """Get the radiobutton widget data in the correct format.

        Args:
            input_data (str): input string

        Returns:
            str: Radiobutton string data
        """
        return input_data


class CheckboxWidget(IWidget):
    """Checkbox widget."""

    def __init__(self, fields: list[str]):
        """Initialize the CheckboxWidget.

        Args:
            fields (list[str]): Checkbox fields.

        Raises:
            ValueError: If the fields list is empty.
        """
        super().__init__(WidgetType.CHECKBOX)
        if not fields:
            raise ValueError("Checkbox must have at least one field")
        self.info["fields"] = fields

    def convert_data(self, input_data: str) -> list[str] | None:
        """Get the checkbox widget data in the correct format.

        Args:
            input_data (str): input string

        Returns:
            (list[str] | None): Checkbox string data or None if the input is not a list
        """
        try:
            return literal_eval(input_data)
        except ValueError:
            return None


class ImageWidget(IWidget):
    """Image widget."""

    def __init__(self, address: str, format: str = "image", width: int = 100):
        """Validate the image fields and defines the base64 if it does not exist.

        Args:
            address (str): image address
            format (str): image format
            width (int): image width

        Raises:
            WidgetInfoError: If both address and base64 are specified.
        """
        super().__init__(WidgetType.IMAGE)

        if width < 1:
            raise WidgetInfoError("Width must be positive")

        self.info["address"] = address
        self.info["format"] = format
        self.info["width"] = width

        try:
            with open(address, "rb") as file:
                file_data = file.read()
        except FileNotFoundError:
            raise WidgetInfoError("The image address is invalid")
        self.info["base64"] = base64.b64encode(file_data).decode("utf-8")

    def convert_data(self, input_data: str | None = None) -> bool:
        """Get the image widget data, i.e. None.

        Args:
            input_data (str | None): input string or nothing.

        Returns:
            bool: True if confirm button is pressed
        """
        return True


class StepWidget(IWidget):
    """Step widget.

    Args:
        title (str): Step title
        text (str | None): Step text
        widget (ImageWidget | None): Step widget

    Raises:
        WidgetInfoError: If the text or widget are not provided.
    """

    def __init__(self, title: str, text: str | None, widget: ImageWidget | None):
        super().__init__(WidgetType.STEP)
        if text is None and widget is None:
            raise WidgetInfoError("Text or widget must be provided")
        self.info["title"] = title
        if isinstance(text, str):
            self.info["text"] = text
        if isinstance(widget, ImageWidget):
            self.info["widget"] = widget.__dict__

    def convert_data(self, input_data: str) -> bool:
        """Get the step widget data in the correct format.

        Args:
            input_data (str): input string

        Returns:
            bool: True if confirm button is pressed
        """
        return True


class MultistepWidget(IWidget):
    """Multistep widget."""

    def __init__(self, steps: list[StepWidget]):
        """Initialize the MultistepWidget.

        Args:
            steps (list[StepWidget]): A list with info about the steps.

        Raises:
            ValueError: If the provided list of steps is empty.
        """
        super().__init__(WidgetType.MULTISTEP)
        if not steps:
            raise ValueError("MultistepWidget must have at least one step")
        self.info["steps"] = []
        for step in steps:
            self.info["steps"].append(step.__dict__)

    def convert_data(self, input_data: str) -> bool:
        """Get the multistep widget data in the correct format.

        Args:
            input_data (str): input string

        Returns:
            bool: True if confirm button is pressed
        """
        return True


@dataclass
class DialogBox:
    """Dialog box data.

    Args:
        dialog_text (str): dialog text
        title_bar (str | None): title bar
        widget (IWidget | None): widget info
    """

    def __init__(
        self,
        dialog_text: str,
        title_bar: str | None = None,
        widget: IWidget | None = None,
    ):
        self.widget: IWidget = BaseWidget() if widget is None else widget
        self.dialog_text: str = dialog_text
        self.title_bar: str | None = title_bar

    def to_dict(self) -> dict:
        """Convert DialogBox to dictionary.

        Returns:
            dict: DialogBox dictionary.
        """
        dbx_dict = deepcopy(self.__dict__)
        dbx_dict["widget"] = deepcopy(self.widget.__dict__)
        return dbx_dict
