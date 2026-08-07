# Copyright (c) 2026 Everypin
# GNU General Public License v3.0 (see LICENSE or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import annotations

from abc import ABC, abstractmethod
from json import dumps
from typing import TYPE_CHECKING, Any

from glom import PathAccessError, assign, glom

from jig.pytest_jig.db.const import (
    DatabaseField as DF,  # noqa: N817  # noqa: N817
)
from jig.pytest_jig.db.schema import ResultRunStore

if TYPE_CHECKING:
    from collections.abc import Generator

    from pydantic import BaseModel


class StorageInterface(ABC):
    """Interface for storage implementations."""

    @abstractmethod
    def get_field(self, key: str) -> Any:  # noqa: ANN401
        """Get field from the storage.

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
    def clear_doc_value(self) -> None:
        """Clear field from the storage."""

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


class TempStorageInterface(ABC):
    """Interface for temporary storage implementations."""

    @abstractmethod
    def push_report(self, report: ResultRunStore) -> bool:
        """Push report to the temporary storage.

        Args:
            report (ResultRunStore): report to store

        Returns:
            bool: True if successful, False otherwise
        """

    @abstractmethod
    def reports(self) -> Generator[dict]:
        """Get all reports from the temporary storage.

        Yields:
            dict: report from temporary storage
        """

    @abstractmethod
    def delete(self, report_id: str) -> bool:
        """Delete report from the temporary storage.

        Args:
            report_id (str): report ID to delete

        Returns:
            bool: True if successful, False otherwise
        """

    def dict_to_schema(self, report: dict) -> ResultRunStore:
        """Convert report dict to report schema.

        Args:
            report (dict): report dictionary

        Returns:
            ResultRunStore: validated report schema
        """
        return ResultRunStore(**report)


def create_default_doc_structure(doc_id: str, doc_id_for_rev: str) -> dict:
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
        DF.DUT: {},
        DF.TEST_STAND: {},
        DF.PROCESS: {},
    }


def update_doc_value(doc: dict, key: str, value: Any) -> None:  # noqa: ANN401
    """Update document value in memory (does not persist).

    Args:
        doc (dict): Storage document
        key (str): Field key, supports nested access with dots
        value (Any): Value to set
    """
    try:
        dumps(value)
    except Exception:  # noqa: BLE001
        value = dumps(value, default=str)

    if "." in key:
        assign(doc, key, value, missing=dict)
    else:
        doc[key] = value


def clear_doc_value(doc: dict, key: str) -> Any:  # noqa: ANN401
    """Clear field from the storage.

    Args:
        doc (dict): Storage document
        key (str): Field key, supports nested access with dots

    Returns:
        Any: Field value, or None if path does not exist
    """
    return doc.pop(key, None)


def get_field(doc: dict, key: str) -> Any:  # noqa: ANN401
    """Get field from the storage.

    Args:
        doc (dict): Storage document
        key (str): Field key, supports nested access with dots

    Returns:
        Any: Field value, or None if path does not exist
    """
    try:
        return glom(doc, key)
    except PathAccessError:
        return None
