# Copyright (c) 2024 Everypin
# GNU General Public License v3.0 (see LICENSE or https://www.gnu.org/licenses/gpl-3.0.txt)


class HardpyError(Exception):
    """Base HardPy exception."""

    def __init__(self, msg: str):
        super().__init__(f"HardPy error: {msg}")


class DuplicateSerialNumberError(HardpyError):
    """The serial number has already been determined."""

    def __init__(self):
        super().__init__(self.__doc__)  # type: ignore
