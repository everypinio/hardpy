# Copyright (c) 2025 Everypin
# GNU General Public License v3.0 (see LICENSE or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING, Mapping  # noqa: UP035

from hardpy.pytest_hardpy.db import DatabaseField as DF  # noqa: N817

if TYPE_CHECKING:
    from datetime import datetime


@dataclass
class Instrument:
    """Test stand instrument (equipment)."""

    name: str | None = None
    revision: str | None = None
    number: int | None = None
    comment: str | None = None
    info: Mapping[str, str | int | float | datetime] | None = None


@dataclass
class DUT:
    """DUT."""

    name: str | None = None
    type: str | None = None
    serial_number: str | None = None
    part_number: str | None = None
    revision: str | None = None
    sub_duts: list[DUT] | None = None
    info: Mapping[str, str | int | float | datetime] | None = None

    def to_dict(self) -> dict:
        """Convert ImageComponent to dictionary.

        Returns:
            dict: ImageComponent dictionary
        """
        return {
            DF.NAME: self.name,
            DF.TYPE: self.type,
            DF.SERIAL_NUMBER: self.serial_number,
            DF.PART_NUMBER: self.part_number,
            DF.REVISION: self.revision,
            DF.SUB_DUTS: self.sub_duts if self.sub_duts else [],
            DF.INFO: self.info,
        }
