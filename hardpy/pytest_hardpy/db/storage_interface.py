# GNU General Public License v3.0 (see LICENSE or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Any

from hardpy.pytest_hardpy.db.const import DatabaseField as DF  # noqa: N817

if TYPE_CHECKING:
    from pydantic import BaseModel


class Storage(ABC):
    """Abstract storage interface for HardPy data persistence.

    This interface defines the contract for storage implementations,
    allowing HardPy to support multiple storage backends (CouchDB, JSON files, etc.).
    """

    @abstractmethod
    def get_field(self, key: str) -> Any:  # noqa: ANN401
        """Get field value from document using dot notation.

        Args:
            key (str): Field key, supports nested access with dots
                (e.g., "modules.test1.status")

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

    def _create_default_doc_structure(self, doc_id: str) -> dict:
        """Create default document structure with standard fields.

        Args:
            doc_id (str): Document ID to use

        Returns:
            dict: Default document structure with DUT, TEST_STAND, and PROCESS fields
        """
        return {
            "_id": doc_id,
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
