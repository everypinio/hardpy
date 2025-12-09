# GNU General Public License v3.0 (see LICENSE or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import annotations

from logging import getLogger
from typing import TYPE_CHECKING

from hardpy.common.config import ConfigManager, StorageType

if TYPE_CHECKING:
    from hardpy.pytest_hardpy.db.storage_interface import Storage

logger = getLogger(__name__)


class StorageFactory:
    """Factory for creating storage instances based on configuration.

    This factory pattern allows HardPy to support multiple storage backends
    (CouchDB, JSON files, etc.) and switch between them based on configuration.
    """

    @staticmethod
    def create_storage(store_name: str) -> Storage:
        """Create storage instance based on configuration.

        Args:
            store_name (str): Name of the storage (e.g., "runstore", "statestore")

        Returns:
            Storage: Storage instance

        Raises:
            ValueError: If storage type is unknown or unsupported
            ImportError: If required dependencies for storage type are not installed
        """
        config = ConfigManager().config
        storage_type = config.database.storage_type

        if storage_type == StorageType.JSON:
            from hardpy.pytest_hardpy.db.json_file_store import JsonFileStore

            logger.debug(f"Creating JSON file storage for {store_name}")
            return JsonFileStore(store_name)

        if storage_type == StorageType.COUCHDB:
            try:
                from hardpy.pytest_hardpy.db.couchdb_store import CouchDBStore
            except ImportError as exc:
                msg = (
                    "CouchDB storage requires pycouchdb. "
                    "Install with: pip install hardpy[couchdb] or "
                    'pip install "pycouchdb>=1.14.2"'
                )
                raise ImportError(msg) from exc

            logger.debug(f"Creating CouchDB storage for {store_name}")
            return CouchDBStore(store_name)

        msg = (
            f"Unknown storage type: {storage_type}. "
            "Supported types: 'json', 'couchdb'"
        )
        raise ValueError(msg)
