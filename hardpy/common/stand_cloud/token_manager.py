# Copyright (c) 2025 Everypin
# GNU General Public License v3.0 (see LICENSE or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import annotations

import json
import sys
from contextlib import suppress
from copy import deepcopy
from platform import system
from typing import TYPE_CHECKING

from keyring import delete_password, get_credential
from keyring.core import load_keyring
from keyring.errors import KeyringError

if TYPE_CHECKING:
    from keyring.backend import KeyringBackend
    from requests_oauth2client import BearerToken



class TokenManager:
    """Token manager."""
    def __init__(self, service_name: str) -> None:
        self._service_name = f"HardPy_{service_name}"

    @property
    def service_name(self) -> str:
        """Get the service HardPy token name for StandCloud."""
        return self._service_name

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
            storage_keyring, _ = self.get_store()
            with suppress(KeyringError):
                storage_keyring.delete_password(self._service_name, "refresh_token")
        return True

    def save_token_info(self, token: BearerToken | dict) -> None:
        """Save token to keyring storage.

        Args:
            token (BearerToken | dict): token
        """
        storage_keyring, mem_keyring = self.get_store()
        storage_keyring.set_password(
            self._service_name,
            "refresh_token",
            token["refresh_token"],
        )

        token_info = deepcopy(token)
        token_info.pop("expires_in")
        token_info.pop("refresh_token")

        try:
            mem_keyring.set_password(
                self._service_name,
                "access_token",
                json.dumps(token_info),
            )
        except KeyringError as e:
            print(e)  # noqa: T201
            sys.exit(1)

    def get_store(self) -> tuple[KeyringBackend, KeyringBackend]:
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
