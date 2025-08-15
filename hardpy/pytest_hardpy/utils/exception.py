# Copyright (c) 2024 Everypin
# GNU General Public License v3.0 (see LICENSE or https://www.gnu.org/licenses/gpl-3.0.txt)


from typing import Any


class HardpyError(Exception):
    """Base HardPy exception."""

    def __init__(self, msg: str) -> None:
        super().__init__(f"HardPy error: {msg}")


class DuplicateParameterError(HardpyError):
    """A parameter has already been defined."""

    def __init__(self, param_name: Any) -> None:  # noqa: ANN401
        super().__init__(f"Parameter {param_name} is already defined")


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
