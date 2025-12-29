# Copyright (c) 2024 Everypin
# GNU General Public License v3.0 (see LICENSE or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import annotations

import json
from abc import ABC, abstractmethod
from json import dumps
from logging import getLogger
from pathlib import Path
from typing import TYPE_CHECKING, Any

from glom import PathAccessError, assign, glom

from hardpy.common.config import ConfigManager, StorageType
from hardpy.common.singleton import SingletonMeta
from hardpy.pytest_hardpy.db.const import DatabaseField as DF  # noqa: N817
from hardpy.pytest_hardpy.db.schema import ResultRunStore

if TYPE_CHECKING:
    from pycouchdb.client import Database  # type: ignore[import-untyped]
    from pydantic import BaseModel


def _create_default_doc_structure(doc_id: str, doc_id_for_rev: str) -> dict:
    """Create default document structure with standard fields.

    Args:
        doc_id (str): Document ID to use
        doc_id_for_rev (str): Document ID for _rev field (for JSON compatibility)

    Returns:
        dict: Default document structure
    """
    return {
        "_id": doc_id,
        "_rev": doc_id_for_rev,
        DF.MODULES: {},
        DF.DUT: {
            DF.TYPE: None,
            DF.NAME: None,
            DF.REVISION: None,
            DF.SERIAL_NUMBER: None,
            DF.PART_NUMBER: None,
            DF.SUB_UNITS: [],
            DF.INFO: {},
        },
        DF.TEST_STAND: {
            DF.HW_ID: None,
            DF.NAME: None,
            DF.REVISION: None,
            DF.TIMEZONE: None,
            DF.LOCATION: None,
            DF.NUMBER: None,
            DF.INSTRUMENTS: [],
            DF.DRIVERS: {},
            DF.INFO: {},
        },
        DF.PROCESS: {
            DF.NAME: None,
            DF.NUMBER: None,
            DF.INFO: {},
        },
    }


class RunStoreInterface(ABC):
    """Interface for run storage implementations."""

    @abstractmethod
    def get_field(self, key: str) -> Any:  # noqa: ANN401
        """Get field from the run store.

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


class JsonRunStore(RunStoreInterface):
    """JSON file-based run storage implementation.

    Stores test run data using JSON files.
    """

    def __init__(self) -> None:
        config_manager = ConfigManager()
        self._store_name = "runstore"
        config_storage_path = Path(config_manager.config.database.storage_path)
        if config_storage_path.is_absolute():
            self._storage_dir = config_storage_path / "storage" / self._store_name
        else:
            self._storage_dir = Path(
                config_manager.tests_path
                / config_manager.config.database.storage_path
                / "storage"
                / self._store_name,
            )
        self._storage_dir.mkdir(parents=True, exist_ok=True)
        self._doc_id = config_manager.config.database.doc_id
        self._file_path = self._storage_dir / f"{self._doc_id}.json"
        self._log = getLogger(__name__)
        self._schema: type[BaseModel] = ResultRunStore
        self._doc: dict = self._init_doc()

    def get_field(self, key: str) -> Any:  # noqa: ANN401
        """Get field value from document using dot notation.

        Args:
            key (str): Field key, supports nested access with dots

        Returns:
            Any: Field value, or None if path does not exist
        """
        try:
            return glom(self._doc, key)
        except PathAccessError:
            return None

    def update_doc_value(self, key: str, value: Any) -> None:  # noqa: ANN401
        """Update document value in memory (does not persist).

        Args:
            key (str): Field key, supports nested access with dots
            value (Any): Value to set
        """
        try:
            dumps(value)
        except Exception:  # noqa: BLE001
            value = dumps(value, default=str)

        if "." in key:
            assign(self._doc, key, value, missing=dict)
        else:
            self._doc[key] = value

    def update_db(self) -> None:
        """Persist in-memory document to JSON file with atomic write."""
        self._storage_dir.mkdir(parents=True, exist_ok=True)
        temp_file = self._file_path.with_suffix(".tmp")

        try:
            with temp_file.open("w") as f:
                json.dump(self._doc, f, indent=2, default=str)
            temp_file.replace(self._file_path)
        except Exception as exc:
            self._log.error(f"Error writing to storage file: {exc}")
            if temp_file.exists():
                temp_file.unlink()
            raise

    def update_doc(self) -> None:
        """Reload document from JSON file to memory."""
        if self._file_path.exists():
            try:
                with self._file_path.open("r") as f:
                    self._doc = json.load(f)
            except json.JSONDecodeError as exc:
                self._log.error(f"Error reading storage file: {exc}")
            except Exception as exc:
                self._log.error(f"Error reading storage file: {exc}")
                raise

    def get_document(self) -> BaseModel:
        """Get full document with schema validation.

        Returns:
            BaseModel: Validated document model
        """
        self.update_doc()
        return self._schema(**self._doc)

    def clear(self) -> None:
        """Clear storage by resetting to initial state (in-memory only)."""
        self._doc = _create_default_doc_structure(self._doc_id, self._doc_id)

    def compact(self) -> None:
        """Optimize storage (no-op for JSON file storage)."""

    def _init_doc(self) -> dict:
        """Initialize or load document structure."""
        if self._file_path.exists():
            try:
                with self._file_path.open("r") as f:
                    doc = json.load(f)

                    if DF.MODULES not in doc:
                        doc[DF.MODULES] = {}

                    return doc
            except json.JSONDecodeError:
                self._log.warning(f"Corrupted storage file {self._file_path},"
                                  f" creating new")
            except Exception as exc:  # noqa: BLE001
                self._log.warning(f"Error loading storage file: {exc}, creating new")

        return _create_default_doc_structure(self._doc_id, self._doc_id)


class CouchDBRunStore(RunStoreInterface):
    """CouchDB-based run storage implementation.

    Stores test run data using CouchDB.
    Clears the storage on initialization to start fresh.
    """

    def __init__(self) -> None:
        from pycouchdb import Server as DbServer  # type: ignore[import-untyped]
        from pycouchdb.exceptions import (  # type: ignore[import-untyped]
            Conflict,
            GenericError,
        )
        from requests.exceptions import ConnectionError  # noqa: A004

        config_manager = ConfigManager()
        config = config_manager.config
        self._db_srv = DbServer(config.database.url)
        self._db_name = "runstore"
        self._doc_id = config.database.doc_id
        self._log = getLogger(__name__)
        self._schema: type[BaseModel] = ResultRunStore

        # Initialize database
        try:
            self._db: Database = self._db_srv.create(self._db_name)  # type: ignore[name-defined]
        except Conflict:
            self._db = self._db_srv.database(self._db_name)
        except GenericError as exc:
            msg = f"Error initializing database {exc}"
            raise RuntimeError(msg) from exc
        except ConnectionError as exc:
            msg = f"Error initializing database: {exc}"
            raise RuntimeError(msg) from exc

        self._doc: dict = self._init_doc()

        # Clear the runstore on initialization for CouchDB
        try:
            self.clear()
        except Exception:  # noqa: BLE001
            self._log.debug("Runstore storage will be created for the first time")

    def get_field(self, key: str) -> Any:  # noqa: ANN401
        """Get field from the run store.

        Args:
            key (str): Field key, supports nested access with dots

        Returns:
            Any: Field value, or None if path does not exist
        """
        try:
            return glom(self._doc, key)
        except PathAccessError:
            return None

    def update_doc_value(self, key: str, value: Any) -> None:  # noqa: ANN401
        """Update document value in memory (does not persist).

        Args:
            key (str): Field key, supports nested access with dots
            value (Any): Value to set
        """
        try:
            dumps(value)
        except Exception:  # noqa: BLE001
            value = dumps(value, default=str)

        if "." in key:
            assign(self._doc, key, value, missing=dict)
        else:
            self._doc[key] = value

    def update_db(self) -> None:
        """Persist in-memory document to storage backend."""
        from pycouchdb.exceptions import Conflict  # type: ignore[import-untyped]

        try:
            self._doc = self._db.save(self._doc)
        except Conflict:
            self._doc["_rev"] = self._db.get(self._doc_id)["_rev"]
            self._doc = self._db.save(self._doc)

    def update_doc(self) -> None:
        """Reload document from storage backend to memory."""
        self._doc["_rev"] = self._db.get(self._doc_id)["_rev"]
        self._doc = self._db.get(self._doc_id)

    def get_document(self) -> BaseModel:
        """Get full document with schema validation.

        Returns:
            BaseModel: Validated document model
        """
        self._doc = self._db.get(self._doc_id)
        return self._schema(**self._doc)

    def clear(self) -> None:
        """Clear storage and reset to initial state."""
        from pycouchdb.exceptions import (  # type: ignore[import-untyped]
            Conflict,
            NotFound,
        )

        try:
            self._db.delete(self._doc_id)
        except (Conflict, NotFound):
            self._log.debug("Database will be created for the first time")
        self._doc = self._init_doc()

    def compact(self) -> None:
        """Optimize storage (implementation-specific, may be no-op)."""
        self._db.compact()

    def _init_doc(self) -> dict:
        """Initialize or load document structure."""
        from pycouchdb.exceptions import NotFound  # type: ignore[import-untyped]

        try:
            doc = self._db.get(self._doc_id)
        except NotFound:
            # CouchDB doesn't need _rev field in the default structure
            default = _create_default_doc_structure(self._doc_id, self._doc_id)
            del default["_rev"]  # CouchDB manages _rev automatically
            return default

        if DF.MODULES not in doc:
            doc[DF.MODULES] = {}

        return doc


class RunStore(metaclass=SingletonMeta):
    """HardPy run storage factory for test run data.

    Creates appropriate storage backend based on configuration:
    - JSON file storage when storage_type is "json"
    - CouchDB storage when storage_type is "couchdb"

    Save state and case artifact. Supports multiple storage backends
    through the factory pattern.

    Note: This class acts as a factory. When instantiated, it returns
    the appropriate concrete implementation (JsonRunStore or CouchDBRunStore).
    """

    def __new__(cls) -> RunStoreInterface:  # type: ignore[misc]
        """Create and return the appropriate storage implementation.

        Returns:
            RunStoreInterface: Concrete storage implementation based on config
        """
        config = ConfigManager()
        storage_type = config.config.database.storage_type

        if storage_type == StorageType.JSON:
            return JsonRunStore()
        if storage_type == StorageType.COUCHDB:
            return CouchDBRunStore()
        msg = f"Unknown storage type: {storage_type}"
        raise ValueError(msg)
