# Copyright (c) 2024 Everypin
# GNU General Public License v3.0 (see LICENSE or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import annotations

from abc import ABC, abstractmethod
from logging import getLogger
from typing import TYPE_CHECKING, Any

from hardpy.common.config import ConfigManager
from hardpy.common.singleton import SingletonMeta
from hardpy.pytest_hardpy.db.schema import ResultRunStore

if TYPE_CHECKING:
    from pydantic import BaseModel


class RunStoreInterface(ABC):
    """Interface for run storage implementations."""

    @abstractmethod
    def get_field(self, key: str) -> Any:  # noqa: ANN401
        """Get field from the run store.

        Args:
            key (str): field name

        Returns:
            Any: field value
        """

    @abstractmethod
    def update_doc_value(self, key: str, value: Any) -> None:  # noqa: ANN401
        """Update document value.

        Args:
            key (str): document key
            value: document value
        """

    @abstractmethod
    def update_db(self) -> None:
        """Update database by current document."""

    @abstractmethod
    def update_doc(self) -> None:
        """Update current document by database."""

    @abstractmethod
    def get_document(self) -> BaseModel:
        """Get document by schema.

        Returns:
            BaseModel: document by schema
        """

    @abstractmethod
    def clear(self) -> None:
        """Clear database."""

    @abstractmethod
    def compact(self) -> None:
        """Compact database."""


class JsonRunStore(RunStoreInterface):
    """JSON file-based run storage implementation.

    Stores test run data using JSON files on the local filesystem.
    """

    def __init__(self) -> None:
        from hardpy.pytest_hardpy.db.json_file_store import JsonFileStore

        self._log = getLogger(__name__)
        self._storage = JsonFileStore("runstore")
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


class CouchDBRunStore(RunStoreInterface):
    """CouchDB-based run storage implementation.

    Stores test run data in CouchDB database.
    """

    def __init__(self) -> None:
        from hardpy.pytest_hardpy.db.couchdb_store import CouchDBStore

        self._log = getLogger(__name__)
        self._storage = CouchDBStore("runstore")

        # Clear the runstore on initialization for CouchDB
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


class RunStore(metaclass=SingletonMeta):
    """HardPy run storage factory for test run data.

    Creates appropriate storage backend based on configuration:
    - JSON file storage when storage_type is "json"
    - CouchDB storage when storage_type is "couchdb"

    Save state and case artifact. Supports multiple storage backends
    through the factory pattern.
    """

    def __init__(self) -> None:
        config = ConfigManager()
        storage_type = config.config.database.storage_type

        self._impl: RunStoreInterface
        if storage_type == "json":
            self._impl = JsonRunStore()
        elif storage_type == "couchdb":
            self._impl = CouchDBRunStore()
        else:
            msg = f"Unknown storage type: {storage_type}"
            raise ValueError(msg)

    def get_field(self, key: str) -> Any:  # noqa: ANN401
        """Get field from the run store.

        Args:
            key (str): field name

        Returns:
            Any: field value
        """
        return self._impl.get_field(key)

    def update_doc_value(self, key: str, value: Any) -> None:  # noqa: ANN401
        """Update document value.

        Args:
            key (str): document key
            value: document value
        """
        self._impl.update_doc_value(key, value)

    def update_db(self) -> None:
        """Update database by current document."""
        self._impl.update_db()

    def update_doc(self) -> None:
        """Update current document by database."""
        self._impl.update_doc()

    def get_document(self) -> BaseModel:
        """Get document by schema.

        Returns:
            BaseModel: document by schema
        """
        return self._impl.get_document()

    def clear(self) -> None:
        """Clear database."""
        self._impl.clear()

    def compact(self) -> None:
        """Compact database."""
        self._impl.compact()
