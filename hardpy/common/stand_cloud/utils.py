# Copyright (c) 2024 Everypin
# GNU General Public License v3.0 (see LICENSE or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import annotations

from enum import Enum
from typing import NamedTuple


class StandCloudAddr(NamedTuple):
    """StandCloud address.

    domain: StandCloud address
    api: API address
    token: token address
    auth: auth address
    device: device-authorization address
    """

    domain: str
    api: str
    token: str
    auth: str
    device: str


class StandCloudAPIMode(str, Enum):
    """StandCloud API mode.

    HARDPY for test stand, integration for third-party service.
    """

    HARDPY = "hardpy"
    INTEGRATION = "integration"
