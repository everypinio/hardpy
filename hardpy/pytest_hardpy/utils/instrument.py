from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING, Mapping  # noqa: UP035

if TYPE_CHECKING:
    from datetime import datetime


@dataclass
class Instrument:
    """Instrument information dataclass."""

    name: str | None = None
    revision: str | None = None
    number: int | None = None
    comment: str | None = None
    info: Mapping[str, str | int | float | datetime] | None = None
