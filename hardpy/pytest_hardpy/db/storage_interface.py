# GNU General Public License v3.0 (see LICENSE or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from pydantic._internal._model_construction import ModelMetaclass


class IStorage(ABC):
    """Abstract storage interface for HardPy data persistence.

    This interface defines the contract for storage implementations,
    allowing HardPy to support multiple storage backends (CouchDB, JSON files, etc.).
    """

    @abstractmethod
    def get_field(self, key: str) -> Any:  # noqa: ANN401
        """Get field value from document using dot notation.

        Args:
            key (str): Field key, supports nested access with dots (e.g., "modules.test1.status")

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
    def get_document(self) -> ModelMetaclass:
        """Get full document with schema validation.

        Returns:
            ModelMetaclass: Validated document model
        """

    @abstractmethod
    def clear(self) -> None:
        """Clear storage and reset to initial state."""

    @abstractmethod
    def compact(self) -> None:
        """Optimize storage (implementation-specific, may be no-op)."""
