# Copyright (c) 2024 Everypin
# GNU General Public License v3.0 (see LICENSE or https://www.gnu.org/licenses/gpl-3.0.txt)


class HardpyError(Exception):
    """Base HardPy exception."""

    def __init__(self, msg: str) -> None:
        super().__init__(f"HardPy error: {msg}")


class DuplicateSerialNumberError(HardpyError):
    """The serial number has already been determined."""

    def __init__(self) -> None:
        super().__init__(self.__doc__)  # type: ignore


class DuplicatePartNumberError(HardpyError):
    """The part number has already been determined."""

    def __init__(self) -> None:
        super().__init__(self.__doc__)  # type: ignore


class DuplicateTestStandNameError(HardpyError):
    """The test stand name has already been determined."""

    def __init__(self) -> None:
        super().__init__(self.__doc__)  # type: ignore


class DuplicateTestStandLocationError(HardpyError):
    """The test stand location has already been determined."""

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
