# Copyright (c) 2025 Everypin
# GNU General Public License v3.0 (see LICENSE or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import annotations

import json
import sys
from contextlib import suppress
from copy import deepcopy
from datetime import datetime, timezone
from platform import system
from typing import TYPE_CHECKING

from keyring import delete_password, get_credential
from keyring.core import load_keyring
from keyring.errors import KeyringError
from requests_oauth2client import BearerToken

if TYPE_CHECKING:
    from keyring.backend import KeyringBackend


class TokenManager:
    """Token manager.

    Manage token in keyring storage.
    """

    def __init__(self, service_name: str) -> None:
        self._service_name = f"HardPy_{service_name}"

    def remove_token(self) -> bool:
        """Remove token from keyring storage.

        Returns:
            bool: True if successful else False
        """
        try:
            while cred := get_credential(self._service_name, None):
                delete_password(self._service_name, cred.username)
        except KeyringError:
            return False
        # TODO(xorialexandrov): fix keyring clearing
        # Windows does not clear refresh token by itself
        if system() == "Windows":
            storage_keyring, _ = self._get_store()
            with suppress(KeyringError):
                storage_keyring.delete_password(self._service_name, "refresh_token")
        return True

    def save_token_info(self, token: BearerToken | dict) -> None:
        """Save token to keyring storage.

        Args:
            token (BearerToken | dict): token
        """
        # fmt: off
        storage_keyring, mem_keyring = self._get_store()
        storage_keyring.set_password(self._service_name, "refresh_token", token["refresh_token"])  # noqa: E501

        token_info = deepcopy(token)
        token_info.pop("expires_in")
        token_info.pop("refresh_token")

        try:
            mem_keyring.set_password(self._service_name, "access_token", json.dumps(token_info))  # noqa: E501
        except KeyringError as e:
            print(e)  # noqa: T201
            sys.exit(1)
        # fmt: on

    def read_access_token(self) -> BearerToken:
        """Read access token from token store.

        Returns:
            BearerToken: access token
        """
        _, mem_keyring = self._get_store()
        token_info = mem_keyring.get_password(self._service_name, "access_token")
        secret = self._add_expires_in(json.loads(token_info))  # type: ignore
        return BearerToken(**secret)

    def read_refresh_token(self) -> str | None:
        """Read refresh token from token store.

        Returns:
            str | None: refresh token
        """
        storage_keyring, _ = self._get_store()
        service_name = self._service_name
        return storage_keyring.get_password(service_name, "refresh_token")

    def _get_store(self) -> tuple[KeyringBackend, KeyringBackend]:
        """Get token store.

        Returns:
            tuple[KeyringBackend, KeyringBackend]: token store
        """
        if system() == "Linux":
            storage_keyring = load_keyring("keyring.backends.SecretService.Keyring")
        elif system() == "Windows":
            storage_keyring = load_keyring("keyring.backends.Windows.WinVaultKeyring")
        # TODO(xorialexandrov): add memory keyring or other store
        mem_keyring = storage_keyring

        return storage_keyring, mem_keyring

    def _add_expires_in(self, secret: dict) -> dict:
        if "expires_at" in secret:
            expires_at = secret["expires_at"]
        elif "id_token" in secret and "exp" in secret["id_token"]:
            expires_at = secret["id_token"]["exp"]
        expires_at_datetime = datetime.fromtimestamp(expires_at, timezone.utc)

        expires_in_datetime = expires_at_datetime - datetime.now(timezone.utc)
        expires_in = int(expires_in_datetime.total_seconds())

        secret["expires_in"] = expires_in

        return secret
