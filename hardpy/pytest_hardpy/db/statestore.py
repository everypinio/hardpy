# Copyright (c) 2024 Everypin
# GNU General Public License v3.0 (see LICENSE or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import annotations

from logging import getLogger
from typing import TYPE_CHECKING, Any

from hardpy.common.singleton import SingletonMeta
from hardpy.pytest_hardpy.db.schema import ResultStateStore
from hardpy.pytest_hardpy.db.storage_factory import StorageFactory

if TYPE_CHECKING:
    from pydantic._internal._model_construction import ModelMetaclass

    from hardpy.pytest_hardpy.db.storage_interface import IStorage


class StateStore(metaclass=SingletonMeta):
    """HardPy state storage interface.

    Stores current test execution state. Supports multiple storage backends
    (JSON files, CouchDB) through the storage factory pattern.
    """

    def __init__(self) -> None:
        self._log = getLogger(__name__)
        self._storage: IStorage = StorageFactory.create_storage("statestore")
        self._storage._schema = ResultStateStore  # type: ignore  # noqa: SLF001

    def get_field(self, key: str) -> Any:  # noqa: ANN401
        """Get field from the state store.

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
