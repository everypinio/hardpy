# Copyright (c) 2026 Everypin
# GNU General Public License v3.0 (see LICENSE or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import annotations

import json
from logging import getLogger
from pathlib import Path
from typing import TYPE_CHECKING, Any

from hardpy.common.config import ConfigManager
from hardpy.pytest_hardpy.db.common import (
    StorageInterface,
    clear_doc_value as _clear_doc_value,
    create_default_doc_structure,
    get_field as _get_field,
    update_doc_value as _update_doc_value,
)
from hardpy.pytest_hardpy.db.const import DatabaseField as DF  # noqa: N817
from hardpy.pytest_hardpy.db.json.common import (
    update_db as _update_db,
    update_doc as _udpate_doc,
)
from hardpy.pytest_hardpy.db.schema import ResultStateStore

if TYPE_CHECKING:
    from pydantic import BaseModel


class JsonStateStore(StorageInterface):
    """JSON file-based state storage implementation.

    Stores test execution state using JSON files.
    """

    def __init__(self) -> None:
        config_manager = ConfigManager()
        self._store_name = "statestore"
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
        self._schema: type[BaseModel] = ResultStateStore
        self._doc: dict = self._init_doc()

    def get_field(self, key: str) -> Any:  # noqa: ANN401
        """Get field value from document using dot notation.

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
        """Persist in-memory document to JSON file with atomic write."""
        _update_db(self._storage_dir, self._file_path, self._doc)

    def update_doc(self) -> None:
        """Reload document from JSON file to memory."""
        self._doc = _udpate_doc(self._file_path, self._doc)

    def get_document(self) -> BaseModel:
        """Get full document with schema validation.

        Returns:
            BaseModel: Validated document model
        """
        self.update_doc()
        return self._schema(**self._doc)

    def clear(self) -> None:
        """Clear storage by resetting to initial state (in-memory only)."""
        self._doc = create_default_doc_structure(self._doc_id, self._doc_id)

    def compact(self) -> None:
        """Optimize storage (no-op for JSON file storage)."""

    def save_history(self, timestamp_id: str) -> None:
        """Save current document as a history entry."""
        doc = self._doc.copy()
        doc["_id"] = timestamp_id
        doc.pop("_rev", None)
        history_file = self._storage_dir / f"{timestamp_id}.json"
        try:
            with history_file.open("w") as f:
                json.dump(doc, f)
        except OSError as e:
            self._log.warning(f"Failed to save history: {e}")

    def _init_doc(self) -> dict:
        """Initialize or load document structure."""
        if self._file_path.exists():
            try:
                with self._file_path.open("r") as f:
                    doc = json.load(f)

                    if DF.MODULES not in doc:
                        doc[DF.MODULES] = {}

                    # Reset volatile fields for statestore
                    default_doc = create_default_doc_structure(doc["_id"], self._doc_id)
                    doc[DF.DUT] = default_doc[DF.DUT]
                    doc[DF.TEST_STAND] = default_doc[DF.TEST_STAND]
                    doc[DF.PROCESS] = default_doc[DF.PROCESS]

                    return doc
            except json.JSONDecodeError:
                self._log.warning(
                    f"Corrupted storage file {self._file_path}, creating new",
                )
            except Exception as exc:  # noqa: BLE001
                self._log.warning(f"Error loading storage file: {exc}, creating new")

        return create_default_doc_structure(self._doc_id, self._doc_id)
