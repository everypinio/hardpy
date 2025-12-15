# Copyright (c) 2024 Everypin
# GNU General Public License v3.0 (see LICENSE or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import annotations

from abc import ABC, abstractmethod
from logging import getLogger
from typing import TYPE_CHECKING, Any

from hardpy.common.config import ConfigManager, StorageType
from hardpy.common.singleton import SingletonMeta
from hardpy.pytest_hardpy.db.schema import ResultStateStore
from hardpy.pytest_hardpy.db.storage_factory import StorageFactory

if TYPE_CHECKING:
    from pydantic import BaseModel

    from hardpy.pytest_hardpy.db.storage_interface import Storage


class StateStoreInterface(ABC):
    """Interface for state storage implementations."""

    @abstractmethod
    def get_field(self, key: str) -> Any:  # noqa: ANN401
        """Get field from the state store.

        Args:
            key (str): Field key, supports nested access with dots

        Returns:
            Any: Field value
        """

    @abstractmethod
    def update_doc_value(self, key: str, value: Any) -> None:  # noqa: ANN401
        """Update document value in memory (does not persist).

        Args:
            key (str): Field key, supports nested access with dots
            value (Any): Value to set
        """

    @abstractmethod
    def update_db(self) -> None:
        """Persist in-memory document to storage backend."""

    @abstractmethod
    def update_doc(self) -> None:
        """Reload document from storage backend to memory."""

    @abstractmethod
    def get_document(self) -> BaseModel:
        """Get full document with schema validation.

        Returns:
            BaseModel: Validated document model
        """

    @abstractmethod
    def clear(self) -> None:
        """Clear storage and reset to initial state."""

    @abstractmethod
    def compact(self) -> None:
        """Optimize storage (implementation-specific, may be no-op)."""


class JsonStateStore(StateStoreInterface):
    """JSON file-based state storage implementation.

    Stores test execution state using JSON files.
    """

    def __init__(self) -> None:
        self._log = getLogger(__name__)
        self._storage: Storage = StorageFactory.create_storage(
            "statestore", ResultStateStore,
        )

    def get_field(self, key: str) -> Any:  # noqa: ANN401
        """Get field from the state store.

        Args:
            key (str): Field key, supports nested access with dots

        Returns:
            Any: Field value
        """
        return self._storage.get_field(key)

    def update_doc_value(self, key: str, value: Any) -> None:  # noqa: ANN401
        """Update document value in memory (does not persist).

        Args:
            key (str): Field key, supports nested access with dots
            value (Any): Value to set
        """
        self._storage.update_doc_value(key, value)

    def update_db(self) -> None:
        """Persist in-memory document to storage backend."""
        self._storage.update_db()

    def update_doc(self) -> None:
        """Reload document from storage backend to memory."""
        self._storage.update_doc()

    def get_document(self) -> BaseModel:
        """Get full document with schema validation.

        Returns:
            BaseModel: Validated document model
        """
        return self._storage.get_document()

    def clear(self) -> None:
        """Clear storage and reset to initial state."""
        self._storage.clear()

    def compact(self) -> None:
        """Optimize storage (implementation-specific, may be no-op)."""
        self._storage.compact()


class CouchDBStateStore(StateStoreInterface):
    """CouchDB-based state storage implementation.

    Stores test execution state using CouchDB.
    """

    def __init__(self) -> None:
        self._log = getLogger(__name__)
        self._storage: Storage = StorageFactory.create_storage(
            "statestore", ResultStateStore,
        )

    def get_field(self, key: str) -> Any:  # noqa: ANN401
        """Get field from the state store.

        Args:
            key (str): Field key, supports nested access with dots

        Returns:
            Any: Field value
        """
        return self._storage.get_field(key)

    def update_doc_value(self, key: str, value: Any) -> None:  # noqa: ANN401
        """Update document value in memory (does not persist).

        Args:
            key (str): Field key, supports nested access with dots
            value (Any): Value to set
        """
        self._storage.update_doc_value(key, value)

    def update_db(self) -> None:
        """Persist in-memory document to storage backend."""
        self._storage.update_db()

    def update_doc(self) -> None:
        """Reload document from storage backend to memory."""
        self._storage.update_doc()

    def get_document(self) -> BaseModel:
        """Get full document with schema validation.

        Returns:
            BaseModel: Validated document model
        """
        return self._storage.get_document()

    def clear(self) -> None:
        """Clear storage and reset to initial state."""
        self._storage.clear()

    def compact(self) -> None:
        """Optimize storage (implementation-specific, may be no-op)."""
        self._storage.compact()


class StateStore(metaclass=SingletonMeta):
    """HardPy state storage factory for test execution state.

    Creates appropriate storage backend based on configuration:
    - JSON file storage when storage_type is "json"
    - CouchDB storage when storage_type is "couchdb"

    This ensures state data is stored in the same backend as the main data.
    """

    def __init__(self) -> None:
        config = ConfigManager()
        storage_type = config.config.database.storage_type

        self._impl: StateStoreInterface
        if storage_type == StorageType.JSON:
            self._impl = JsonStateStore()
        elif storage_type == StorageType.COUCHDB:
            self._impl = CouchDBStateStore()
        else:
            msg = f"Unknown storage type: {storage_type}"
            raise ValueError(msg)

    def get_field(self, key: str) -> Any:  # noqa: ANN401
        """Get field from the state store.

        Args:
            key (str): Field key, supports nested access with dots

        Returns:
            Any: Field value
        """
        return self._impl.get_field(key)

    def update_doc_value(self, key: str, value: Any) -> None:  # noqa: ANN401
        """Update document value in memory (does not persist).

        Args:
            key (str): Field key, supports nested access with dots
            value (Any): Value to set
        """
        self._impl.update_doc_value(key, value)

    def update_db(self) -> None:
        """Persist in-memory document to storage backend."""
        self._impl.update_db()

    def update_doc(self) -> None:
        """Reload document from storage backend to memory."""
        self._impl.update_doc()

    def get_document(self) -> BaseModel:
        """Get full document with schema validation.

        Returns:
            BaseModel: Validated document model
        """
        return self._impl.get_document()

    def clear(self) -> None:
        """Clear storage and reset to initial state."""
        self._impl.clear()

    def compact(self) -> None:
        """Optimize storage (implementation-specific, may be no-op)."""
        self._impl.compact()
