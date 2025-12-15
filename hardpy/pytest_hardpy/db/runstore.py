# Copyright (c) 2024 Everypin
# GNU General Public License v3.0 (see LICENSE or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import annotations

from logging import getLogger
from typing import TYPE_CHECKING, Any

from hardpy.common.config import ConfigManager, StorageType
from hardpy.common.singleton import SingletonMeta
from hardpy.pytest_hardpy.db.schema import ResultRunStore
from hardpy.pytest_hardpy.db.storage_factory import StorageFactory

if TYPE_CHECKING:
    from pydantic import BaseModel

    from hardpy.pytest_hardpy.db.storage_interface import Storage


class RunStore(metaclass=SingletonMeta):
    """HardPy run storage for test run data.

    Creates appropriate storage backend based on configuration:
    - JSON file storage when storage_type is "json"
    - CouchDB storage when storage_type is "couchdb"

    Save state and case artifact. Supports multiple storage backends
    through the factory pattern.
    """

    def __init__(self) -> None:
        self._log = getLogger(__name__)
        config = ConfigManager()

        self._storage: Storage = StorageFactory.create_storage(
            "runstore", ResultRunStore,
        )

        # Clear the runstore on initialization for CouchDB
        if config.config.database.storage_type == StorageType.COUCHDB:
            try:
                self._storage.clear()
            except Exception:  # noqa: BLE001
                self._log.debug("Runstore storage will be created for the first time")

    def get_field(self, key: str) -> Any:  # noqa: ANN401
        """Get field from the run store.

        Args:
            key (str): field name

        Returns:
            Any: field value
        """
        return self._storage.get_field(key)

    def update_doc_value(self, key: str, value: Any) -> None:  # noqa: ANN401
        """Update document value.

        Args:
            key (str): document key
            value: document value
        """
        self._storage.update_doc_value(key, value)

    def update_db(self) -> None:
        """Update database by current document."""
        self._storage.update_db()

    def update_doc(self) -> None:
        """Update current document by database."""
        self._storage.update_doc()

    def get_document(self) -> BaseModel:
        """Get document by schema.

        Returns:
            BaseModel: document by schema
        """
        return self._storage.get_document()

    def clear(self) -> None:
        """Clear database."""
        self._storage.clear()

    def compact(self) -> None:
        """Compact database."""
        self._storage.compact()
