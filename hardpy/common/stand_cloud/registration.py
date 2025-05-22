# Copyright (c) 2025 Everypin
# GNU General Public License v3.0 (see LICENSE or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import annotations

from contextlib import suppress
from datetime import timedelta
from platform import system

import requests
from keyring import delete_password, get_credential
from keyring.errors import KeyringError
from oauthlib.oauth2.rfc6749.errors import (
    InvalidGrantError,
    TokenExpiredError,
)
from requests.exceptions import HTTPError
from requests_oauth2client.tokens import ExpiredAccessToken

from hardpy.common.stand_cloud.connector import StandCloudConnector, StandCloudError
from hardpy.common.stand_cloud.oauth2 import SERVICE_NAME, OAuth2
from hardpy.common.stand_cloud.token_storage import get_token_store


def login(addr: str) -> None:
    """Login HardPy in StandCloud.

    Args:
        addr (str): StandCloud address
    """
    try:
        sc_connector = StandCloudConnector(addr=addr)
    except StandCloudError as exc:
        print(str(exc))
        return

    try:
        requests.get(
            url=sc_connector.url.api,
            auth=OAuth2(sc_connector),
            verify=sc_connector.verify_ssl,
            timeout=10,
        )
    except ExpiredAccessToken as e:
        time_diff = timedelta(seconds=abs(e.args[0].expires_in))
        print(f"API access error: token is expired for {time_diff}")
    except TokenExpiredError as e:
        print(f"API access error: {e.description}")
    except InvalidGrantError as e:
        print(f"Refresh token error: {e.description}")
    except HTTPError as e:
        print(e)


def logout() -> bool:
    """Logout HardPy from StandCloud.

    Returns:
        bool: True if successful else False
    """
    try:
        while cred := get_credential(SERVICE_NAME, None):
            delete_password(SERVICE_NAME, cred.username)
    except KeyringError:
        return False
    # TODO(xorialexandrov): fix keyring clearing
    # Windows does not clear refresh token by itself
    if system() == "Windows":
        storage_keyring, _ = get_token_store()
        with suppress(KeyringError):
            storage_keyring.delete_password(SERVICE_NAME, "refresh_token")
    return True
