# Copyright (c) 2025 Everypin
# GNU General Public License v3.0 (see LICENSE or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING, Mapping  # noqa: UP035

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
class SubUnit:
    """Sub unit of DUT."""

    name: str | None = None
    type: str | None = None
    serial_number: str | None = None
    part_number: str | None = None
    revision: str | None = None
    info: Mapping[str, str | int | float | datetime] | None = None
