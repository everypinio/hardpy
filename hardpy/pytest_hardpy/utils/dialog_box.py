# Copyright (c) 2024 Everypin
# GNU General Public License v3.0 (see LICENSE or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import annotations

import base64
from abc import ABC, abstractmethod
from ast import literal_eval
from copy import deepcopy
from dataclasses import dataclass
from enum import Enum
from typing import Any, Final
from uuid import uuid4

from hardpy.pytest_hardpy.utils.exception import ImageError, WidgetInfoError


class WidgetType(Enum):
    """Dialog box widget type."""

    BASE = "base"
    TEXT_INPUT = "textinput"
    NUMERIC_INPUT = "numericinput"
    RADIOBUTTON = "radiobutton"
    CHECKBOX = "checkbox"
    STEP = "step"
    MULTISTEP = "multistep"


class IWidget(ABC):
    """Dialog box widget interface."""

    def __init__(self, widget_type: WidgetType) -> None:
        self.type: Final[str] = widget_type.value
        self.info: dict = {}

    @abstractmethod
    def convert_data(self, input_data: str | None) -> Any | None:  # noqa: ANN401
        """Get the widget data in the correct format.

        Args:
            input_data (str | None): input string or nothing.

        Returns:
            Any: Widget data in the correct format
        """
        raise NotImplementedError


class BaseWidget(IWidget):
    """Widget info interface."""

    def __init__(
        self,
        widget_type: WidgetType = WidgetType.BASE,
    ) -> None:
        super().__init__(widget_type)

    def convert_data(self, input_data: str | None = None) -> bool:  # noqa: ARG002
        """Get base widget data, i.e. None.

        Args:
            input_data (str): input string

        Returns:
            bool: True if confirm button is pressed
        """
        return True


class TextInputWidget(IWidget):
    """Text input widget."""

    def __init__(self) -> None:
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

    def __init__(self) -> None:
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

    def __init__(self, fields: list[str]) -> None:
        """Initialize the RadiobuttonWidget.

        Args:
            fields (list[str]): Radiobutton fields.

        Raises:
            ValueError: If the fields list is empty.
        """
        super().__init__(WidgetType.RADIOBUTTON)
        if not fields:
            msg = "RadiobuttonWidget must have at least one field"
            raise ValueError(msg)
        if len(fields) != len(set(fields)):
            msg = "RadiobuttonWidget fields must be unique"
            raise ValueError(msg)
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

    def __init__(self, fields: list[str]) -> None:
        """Initialize the CheckboxWidget.

        Args:
            fields (list[str]): Checkbox fields.

        Raises:
            ValueError: If the fields list is empty.
        """
        super().__init__(WidgetType.CHECKBOX)
        if not fields:
            msg = "Checkbox must have at least one field"
            raise ValueError(msg)
        if len(fields) != len(set(fields)):
            msg = "CheckboxWidget fields must be unique"
            raise ValueError(msg)
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


class StepWidget(IWidget):
    """Step widget.

    Args:
        title (str): Step title
        text (str | None): Step text
        image (ImageComponent | None): Step image
        html (HTMLComponent | None): Step html

    Raises:
        WidgetInfoError: If the text or widget are not provided.
    """

    def __init__(
        self,
        title: str,
        text: str | None,
        image: ImageComponent | None = None,
        html: HTMLComponent | None = None,
    ) -> None:
        super().__init__(WidgetType.STEP)
        if text is None and image is None and html is None:
            msg = "Text, image and html must be provided"
            raise WidgetInfoError(msg)
        self.info["title"] = title
        if isinstance(text, str):
            self.info["text"] = text
        if isinstance(image, ImageComponent):
            self.info["image"] = image.__dict__
        if isinstance(html, HTMLComponent):
            self.info["html"] = html.__dict__

    def convert_data(self, input_data: str) -> bool:  # noqa: ARG002
        """Get the step widget data in the correct format.

        Args:
            input_data (str): input string

        Returns:
            bool: True if confirm button is pressed
        """
        return True


class MultistepWidget(IWidget):
    """Multistep widget."""

    def __init__(self, steps: list[StepWidget]) -> None:
        """Initialize the MultistepWidget.

        Args:
            steps (list[StepWidget]): A list with info about the steps.

        Raises:
            ValueError: If the provided list of steps is empty.
        """
        super().__init__(WidgetType.MULTISTEP)
        if not steps:
            msg = "MultistepWidget must have at least one step"
            raise ValueError(msg)
        title_set = set()
        self.info["steps"] = []
        for step in steps:
            title = step.info["title"]
            if title in title_set:
                msg = "MultistepWidget must have unique step titles"
                raise ValueError(msg)
            title_set.add(title)
            self.info["steps"].append(step.__dict__)

    def convert_data(self, input_data: str) -> bool:  # noqa: ARG002
        """Get the multistep widget data in the correct format.

        Args:
            input_data (str): input string

        Returns:
            bool: True if confirm button is pressed
        """
        return True


class ImageComponent:
    """Image component."""

    def __init__(
        self,
        address: str,
        width: int = 100,
        border: int = 0,
    ) -> None:
        """Initialize the image component.

        Args:
            address (str): image address
            width (int): image width
            border (int): image border

        Raises:
            ImageError: If both address and base64data are specified
        """
        if width < 1:
            msg = "Width must be positive"
            raise WidgetInfoError(msg)

        if border < 0:
            msg = "Border must be non-negative"
            raise WidgetInfoError(msg)

        try:
            with open(address, "rb") as file:  # noqa: PTH123
                file_data = file.read()
        except FileNotFoundError as exc:
            msg = "The image address is invalid"
            raise ImageError(msg) from exc
        self.address = address
        self.width = width
        self.border = border
        self.base64 = base64.b64encode(file_data).decode("utf-8")

    def to_dict(self) -> dict:
        """Convert ImageComponent to dictionary.

        Returns:
            dict: ImageComponent dictionary
        """
        return {
            "address": self.address,
            "width": self.width,
            "base64": self.base64,
            "border": self.border,
        }


class HTMLComponent:
    """HTML component."""

    def __init__(
        self,
        html: str,
        width: int = 100,
        border: int = 0,
        is_raw_html: bool = True,
    ) -> None:
        """Initialize the HTML component.

        Args:
            html (str): html string or URL
            width (int): html component width
            border (int): html component border
            is_raw_html (bool): True if the html code is raw, else False
        """
        if width < 1:
            msg = "Width must be positive"
            raise WidgetInfoError(msg)

        if border < 0:
            msg = "Border must be non-negative"
            raise WidgetInfoError(msg)

        self.code_or_url = html
        self.width = width
        self.border = border
        self.is_raw_html = is_raw_html

    def to_dict(self) -> dict:
        """Convert HtmlComponent to dictionary.

        Returns:
            dict: HtmlComponent dictionary.
        """
        return {
            "code_or_url": self.code_or_url,
            "width": self.width,
            "border": self.border,
            "is_raw_html": self.is_raw_html,
        }


@dataclass
class DialogBox:
    """Dialog box data.

    Args:
        dialog_text (str): dialog text
        title_bar (str | None): title bar
        widget (IWidget | None): widget info
        image (ImageComponent | None): image
        font_size (int): font size
    """

    def __init__(  # noqa: PLR0913
        self,
        dialog_text: str,
        title_bar: str | None = None,
        widget: IWidget | None = None,
        image: ImageComponent | None = None,
        html: HTMLComponent | None = None,
        font_size: int = 14,
    ) -> None:
        self.widget: IWidget = BaseWidget() if widget is None else widget
        self.image: ImageComponent | None = image
        self.html: HTMLComponent | None = html
        self.dialog_text: str = dialog_text
        self.title_bar: str | None = title_bar
        self.visible: bool = True
        self.id = str(uuid4())
        self.font_size = font_size

        if font_size < 1:
            msg = "The 'font_size' argument cannot be less than 1"
            raise ValueError(msg)

    def to_dict(self) -> dict:
        """Convert DialogBox to dictionary.

        Returns:
            dict: DialogBox dictionary.
        """
        dbx_dict = deepcopy(self.__dict__)
        dbx_dict["widget"] = deepcopy(self.widget.__dict__)
        if self.image:
            dbx_dict["image"] = deepcopy(self.image.__dict__)
        if self.html:
            dbx_dict["html"] = deepcopy(self.html.__dict__)
        return dbx_dict
