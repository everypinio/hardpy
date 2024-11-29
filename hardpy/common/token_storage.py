# Copyright (c) 2024 Everypin
# GNU General Public License v3.0 (see LICENSE or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import annotations

from typing import TYPE_CHECKING

from keyring.core import load_keyring

if TYPE_CHECKING:
    from keyring.backend import KeyringBackend


def get_token_store() -> tuple[KeyringBackend, KeyringBackend]:
    """Get token store.

    Returns:
        tuple[KeyringBackend, KeyringBackend]: token store
    """
    storage_keyring = load_keyring("keyring.backends.SecretService.Keyring")
    # TODO(xorialexandrov): add memory keyring or other store
    mem_keyring = storage_keyring

    return storage_keyring, mem_keyring
