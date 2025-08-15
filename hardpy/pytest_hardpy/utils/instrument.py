from dataclasses import dataclass
from datetime import datetime
from typing import Mapping


@dataclass
class Instrument:
    """Instrument information dataclass."""

    name: str | None = None
    revision: str | None = None
    number: int | None = None
    comment: str | None = None
    info: Mapping[str, str | int | float | datetime] | None = None
