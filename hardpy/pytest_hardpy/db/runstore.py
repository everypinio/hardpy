# Copyright (c) 2024 Everypin
# GNU General Public License v3.0 (see LICENSE or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import annotations

from logging import getLogger
from typing import TYPE_CHECKING, Any

from hardpy.common.singleton import SingletonMeta
from hardpy.pytest_hardpy.db.schema import ResultRunStore
from hardpy.pytest_hardpy.db.storage_factory import StorageFactory

if TYPE_CHECKING:
    from pydantic._internal._model_construction import ModelMetaclass

    from hardpy.pytest_hardpy.db.storage_interface import IStorage


class RunStore(metaclass=SingletonMeta):
    """HardPy run storage interface.

    Save state and case artifact. Supports multiple storage backends
    (JSON files, CouchDB) through the storage factory pattern.
    """

    def __init__(self) -> None:
        self._log = getLogger(__name__)
        self._storage: IStorage = StorageFactory.create_storage("runstore")

        # For CouchDB: Clear the runstore on initialization
        # For JSON: The JsonFileStore __init__ already loads existing data
        # Only clear if explicitly requested via clear() method
        from hardpy.pytest_hardpy.db.base_store import CouchDBStore
        if isinstance(self._storage, CouchDBStore):
            try:
                self._storage.clear()
            except Exception:  # noqa: BLE001
                self._log.debug("Runstore storage will be created for the first time")

        self._storage._schema = ResultRunStore  # type: ignore  # noqa: SLF001

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

    def get_document(self) -> ModelMetaclass:
        """Get document by schema.

        Returns:
            ModelMetaclass: document by schema
        """
        return self._storage.get_document()

    def clear(self) -> None:
        """Clear database."""
        self._storage.clear()

    def compact(self) -> None:
        """Compact database."""
        self._storage.compact()
