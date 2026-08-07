# Copyright (c) 2026 Everypin
# GNU General Public License v3.0 (see LICENSE or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import annotations

from typing import TYPE_CHECKING

from jig.common.config import ConfigManager, StorageType
from jig.common.singleton import SingletonMeta
from jig.pytest_jig.db.couchdb import CouchDBRunStore
from jig.pytest_jig.db.json import JsonRunStore

if TYPE_CHECKING:
    from jig.pytest_jig.db.common import StorageInterface


class RunStore(metaclass=SingletonMeta):
    """Jig run storage factory for test run data.

    Creates appropriate storage backend based on configuration:
    - JSON file storage when storage_type is "json"
    - CouchDB storage when storage_type is "couchdb"

    Save state and case artifact. Supports multiple storage backends
    through the factory pattern.

    Note: This class acts as a factory. When instantiated, it returns
    the appropriate concrete implementation (JsonRunStore or CouchDBRunStore).
    """

    def __new__(cls) -> StorageInterface:  # type: ignore[misc]
        """Create and return the appropriate storage implementation.

        Returns:
            StorageInterface: Concrete storage implementation based on config
        """
        config = ConfigManager()
        storage_type = config.config.database.storage_type

        if storage_type == StorageType.JSON:
            return JsonRunStore()
        if storage_type == StorageType.COUCHDB:
            return CouchDBRunStore()
        msg = f"Unknown storage type: {storage_type}"
        raise ValueError(msg)
