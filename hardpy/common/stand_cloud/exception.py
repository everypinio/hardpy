# Copyright (c) 2024 Everypin
# GNU General Public License v3.0 (see LICENSE or https://www.gnu.org/licenses/gpl-3.0.txt)


class StandCloudError(Exception):
    """Base StandCloud error."""

    def __init__(self, msg: str) -> None:
        super().__init__(f"StandCloud error: {msg}")
