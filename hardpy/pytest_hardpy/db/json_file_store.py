# GNU General Public License v3.0 (see LICENSE or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import annotations

import json
from json import dumps
from logging import getLogger
from pathlib import Path
from typing import TYPE_CHECKING, Any

from glom import assign, glom

from hardpy.common.config import ConfigManager
from hardpy.pytest_hardpy.db.const import DatabaseField as DF  # noqa: N817
from hardpy.pytest_hardpy.db.storage_interface import IStorage

if TYPE_CHECKING:
    from pydantic._internal._model_construction import ModelMetaclass


class JsonFileStore(IStorage):
    """JSON file-based storage implementation.

    Stores data in JSON files within the .hardpy/storage directory of the test project.
    Provides atomic writes and file locking for concurrent access safety.
    """

    def __init__(self, store_name: str) -> None:
        """Initialize JSON file storage.

        Args:
            store_name (str): Name of the storage (e.g., "runstore", "statestore")
        """
        config_manager = ConfigManager()
        self._store_name = store_name
        self._storage_dir = Path(config_manager.config.database.storage_path) / "storage"
        self._storage_dir.mkdir(parents=True, exist_ok=True)
        self._file_path = self._storage_dir / f"{store_name}.json"
        self._doc_id = config_manager.config.database.doc_id
        self._log = getLogger(__name__)
        self._doc: dict = self._init_doc()
        self._schema: ModelMetaclass

    def get_field(self, key: str) -> Any:  # noqa: ANN401
        """Get field value from document using dot notation.

        Args:
            key (str): Field key, supports nested access with dots

        Returns:
            Any: Field value, or None if path does not exist
        """
        from glom import PathAccessError

        try:
            return glom(self._doc, key)
        except PathAccessError:
            # Return None for missing paths (matches CouchDB behavior)
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
            # serialize non-serializable objects as string
            value = dumps(value, default=str)

        if "." in key:
            # Use glom's Assign with missing=dict to create intermediate paths
            assign(self._doc, key, value, missing=dict)
        else:
            self._doc[key] = value

    def update_db(self) -> None:
        """Persist in-memory document to JSON file with atomic write."""
        temp_file = self._file_path.with_suffix(".tmp")

        try:
            # Write to temporary file first
            with temp_file.open("w") as f:
                json.dump(self._doc, f, indent=2, default=str)

            # Atomic rename (on most systems)
            temp_file.replace(self._file_path)

        except Exception as exc:
            self._log.error(f"Error writing to storage file: {exc}")
            # Clean up temp file if it exists
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
                # Keep existing in-memory document if file is corrupted
            except Exception as exc:
                self._log.error(f"Error reading storage file: {exc}")
                raise

    def get_document(self) -> ModelMetaclass:
        """Get full document with schema validation.

        Returns:
            ModelMetaclass: Validated document model
        """
        self.update_doc()
        return self._schema(**self._doc)

    def clear(self) -> None:
        """Clear storage by resetting to initial state (in-memory only).

        Note: For JSON storage, clear() only resets the in-memory document.
        Call update_db() explicitly to persist the cleared state.
        This differs from CouchDB where clear() immediately affects the database.
        """
        # Reset document to initial state (in-memory only)
        self._doc = {
            "_id": self._doc_id,
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
        # NOTE: We do NOT call update_db() here to avoid persisting cleared state
        # The caller should call update_db() when they want to persist changes

    def compact(self) -> None:
        """Optimize storage (no-op for JSON file storage)."""

    def _init_doc(self) -> dict:
        """Initialize or load document structure.

        Returns:
            dict: Document structure
        """
        if self._file_path.exists():
            try:
                with self._file_path.open("r") as f:
                    doc = json.load(f)

                    # Ensure required fields exist (for backward compatibility)
                    if DF.MODULES not in doc:
                        doc[DF.MODULES] = {}

                    # Reset volatile fields for state-like stores
                    if self._store_name == "statestore":
                        doc[DF.DUT] = {
                            DF.TYPE: None,
                            DF.NAME: None,
                            DF.REVISION: None,
                            DF.SERIAL_NUMBER: None,
                            DF.PART_NUMBER: None,
                            DF.SUB_UNITS: [],
                            DF.INFO: {},
                        }
                        doc[DF.TEST_STAND] = {
                            DF.HW_ID: None,
                            DF.NAME: None,
                            DF.REVISION: None,
                            DF.TIMEZONE: None,
                            DF.LOCATION: None,
                            DF.NUMBER: None,
                            DF.INSTRUMENTS: [],
                            DF.DRIVERS: {},
                            DF.INFO: {},
                        }
                        doc[DF.PROCESS] = {
                            DF.NAME: None,
                            DF.NUMBER: None,
                            DF.INFO: {},
                        }

                    return doc
            except json.JSONDecodeError:
                self._log.warning(
                    f"Corrupted storage file {self._file_path}, creating new",
                )
            except Exception as exc:  # noqa: BLE001
                self._log.warning(f"Error loading storage file: {exc}, creating new")

        # Return default document structure
        return {
            "_id": self._doc_id,
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
