# Copyright (c) 2026 Everypin
# GNU General Public License v3.0 (see LICENSE or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import annotations

from typing import TYPE_CHECKING

from jig.common.config import ConfigManager, StorageType
from jig.common.singleton import SingletonMeta
from jig.pytest_jig.db.couchdb import CouchDBTempStore
from jig.pytest_jig.db.json import JsonTempStore

if TYPE_CHECKING:
    from jig.pytest_jig.db.common import TempStorageInterface


class TempStore(metaclass=SingletonMeta):
    """Jig temporary storage factory for data synchronization.

    Creates appropriate storage backend based on configuration:
    - JSON file storage when storage_type is "json"
    - CouchDB storage when storage_type is "couchdb"

    This ensures temporary reports are stored in the same backend as the main data.

    Note: This class acts as a factory. When instantiated, it returns
    the appropriate concrete implementation (JsonTempStore or CouchDBTempStore).
    """

    def __new__(cls) -> TempStorageInterface:
        """Create and return the appropriate storage implementation.

        Returns:
            TempStoreInterface: Concrete storage implementation based on config
        """
        config = ConfigManager()
        storage_type = config.config.database.storage_type

        if storage_type == StorageType.JSON:
            return JsonTempStore()
        if storage_type == StorageType.COUCHDB:
            return CouchDBTempStore()
        msg = f"Unknown storage type: {storage_type}"
        raise ValueError(msg)
