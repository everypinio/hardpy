# Copyright (c) 2024 Everypin
# GNU General Public License v3.0 (see LICENSE or https://www.gnu.org/licenses/gpl-3.0.txt)


class HardpyError(Exception):
    """Base HardPy exception."""

    def __init__(self, msg: str) -> None:
        super().__init__(f"HardPy error: {msg}")


class DuplicateFieldError(HardpyError):
    """A field has already been determined in the specified method."""

    def __init__(self, method_name: str) -> None:
        super().__init__(f"Field has already been determined in method '{method_name}'")


class TestStandNumberError(HardpyError):
    """The test stand number is in the incorrect format."""

    def __init__(self) -> None:
        super().__init__(self.__doc__)  # type: ignore


class WidgetInfoError(HardpyError):
    """The widget info is not correct."""

    def __init__(self, message: str) -> None:
        super().__init__(message)


class ImageError(HardpyError):
    """The image info is not correct."""

    def __init__(self, message: str) -> None:
        super().__init__(message)
