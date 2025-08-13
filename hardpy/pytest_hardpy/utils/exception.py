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


class DuplicateTestStandNumberError(HardpyError):
    """The test stand number has already been determined."""

    def __init__(self) -> None:
        super().__init__(self.__doc__)  # type: ignore


class DuplicateUserNameError(HardpyError):
    """The user name has already been determined."""

    def __init__(self) -> None:
        super().__init__(self.__doc__)  # type: ignore


class DuplicateBatchSerialNumberError(HardpyError):
    """The batch serial number has already been determined."""

    def __init__(self) -> None:
        super().__init__(self.__doc__)  # type: ignore


class DuplicateDutNameError(HardpyError):
    """The DUT name has already been determined."""

    def __init__(self) -> None:
        super().__init__(self.__doc__)  # type: ignore


class DuplicateDutTypeError(HardpyError):
    """The DUT type has already been determined."""

    def __init__(self) -> None:
        super().__init__(self.__doc__)  # type: ignore


class DuplicateDutRevisionError(HardpyError):
    """The DUT revision has already been determined."""

    def __init__(self) -> None:
        super().__init__(self.__doc__)  # type: ignore


class DuplicateStandRevisionError(HardpyError):
    """The test stand revision has already been determined."""

    def __init__(self) -> None:
        super().__init__(self.__doc__)  # type: ignore


class DuplicateProcessNameError(HardpyError):
    """The process name has already been determined."""

    def __init__(self) -> None:
        super().__init__(self.__doc__)  # type: ignore


class DuplicateProcessNumberError(HardpyError):
    """The process number has already been determined."""

    def __init__(self) -> None:
        super().__init__(self.__doc__)  # type: ignore


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
