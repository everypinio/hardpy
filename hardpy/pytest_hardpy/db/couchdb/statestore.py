# Copyright (c) 2026 Everypin
# GNU General Public License v3.0 (see LICENSE or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import annotations

from logging import getLogger
from typing import TYPE_CHECKING, Any

from pycouchdb import Server as DbServer
from pycouchdb.exceptions import (
    Conflict,
    GenericError,
    NotFound,
)
from requests.exceptions import ConnectionError  # noqa: A004

from hardpy.common.config import ConfigManager
from hardpy.pytest_hardpy.db.common import (
    StorageInterface,
    clear_doc_value as _clear_doc_value,
    create_default_doc_structure,
    get_field as _get_field,
    update_doc_value as _update_doc_value,
)
from hardpy.pytest_hardpy.db.const import DatabaseField as DF  # noqa: N817
from hardpy.pytest_hardpy.db.couchdb.common import (
    update_db as _update_db,
    update_doc as _update_doc,
)
from hardpy.pytest_hardpy.db.schema import ResultStateStore

if TYPE_CHECKING:
    from pycouchdb.client import Database
    from pydantic import BaseModel


class CouchDBStateStore(StorageInterface):
    """CouchDB-based state storage implementation.

    Stores test execution state using CouchDB.
    """

    def __init__(self) -> None:
        config_manager = ConfigManager()
        config = config_manager.config
        self._db_srv = DbServer(config.database.url)
        self._db_name = "statestore"
        self._doc_id = config.database.doc_id
        self._log = getLogger(__name__)
        self._schema: type[BaseModel] = ResultStateStore

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

    def get_field(self, key: str) -> Any:  # noqa: ANN401
        """Get field from the state store.

        Args:
            key (str): Field key, supports nested access with dots

        Returns:
            Any: Field value, or None if path does not exist
        """
        return _get_field(self._doc, key)

    def update_doc_value(self, key: str, value: Any) -> None:  # noqa: ANN401
        """Update document value in memory (does not persist).

        Args:
            key (str): Field key, supports nested access with dots
            value (Any): Value to set
        """
        _update_doc_value(self._doc, key, value)

    def clear_doc_value(self, key: str) -> Any:  # noqa: ANN401
        """Clear field from the storage.

        Args:
            key (str): Field key, supports nested access with dots

        Returns:
            Any: Field value, or None if path does not exist
        """
        return _clear_doc_value(self._doc, key)

    def update_db(self) -> None:
        """Persist in-memory document to storage backend."""
        _update_db(self._doc, self._doc_id, self._db)

    def update_doc(self) -> None:
        """Reload document from storage backend to memory."""
        self._doc = _update_doc(self._doc, self._doc_id, self._db)

    def get_document(self) -> BaseModel:
        """Get full document with schema validation.

        Returns:
            BaseModel: Validated document model
        """
        self._doc = self._db.get(self._doc_id)
        return self._schema(**self._doc)

    def clear(self) -> None:
        """Clear storage and reset to initial state."""
        try:
            self._db.delete(self._doc_id)
        except (Conflict, NotFound):
            self._log.debug("Database will be created for the first time")
        self._doc = self._init_doc()

    def compact(self) -> None:
        """Optimize storage (implementation-specific, may be no-op)."""
        self._db.compact()

    def save_history(self, timestamp_id: str) -> None:
        """Save current document as a history entry."""
        doc = self._doc.copy()
        doc["_id"] = timestamp_id
        doc.pop("_rev", None)
        try:
            self._db.save(doc)
        except (Conflict, GenericError, ConnectionError) as e:
            self._log.warning(f"Failed to save history: {e}")

    def _init_doc(self) -> dict:
        """Initialize or load document structure."""
        try:
            doc = self._db.get(self._doc_id)
        except NotFound:
            # CouchDB doesn't need _rev field in the default structure
            default = create_default_doc_structure(self._doc_id, self._doc_id)
            del default["_rev"]  # CouchDB manages _rev automatically
            return default

        if DF.MODULES not in doc:
            doc[DF.MODULES] = {}

        # Reset volatile fields
        default_doc = create_default_doc_structure(doc["_id"], self._doc_id)
        doc[DF.DUT] = default_doc[DF.DUT]
        doc[DF.TEST_STAND] = default_doc[DF.TEST_STAND]
        doc[DF.PROCESS] = default_doc[DF.PROCESS]

        return doc
