# Copyright (c) 2025 Everypin
# GNU General Public License v3.0 (see LICENSE or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import annotations

import json
from abc import ABC, abstractmethod
from logging import getLogger
from pathlib import Path
from typing import TYPE_CHECKING

from uuid6 import uuid7

from hardpy.common.config import ConfigManager, StorageType
from hardpy.common.singleton import SingletonMeta
from hardpy.pytest_hardpy.db.schema import ResultRunStore

if TYPE_CHECKING:
    from collections.abc import Generator


class TempStoreInterface(ABC):
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


class JsonTempStore(TempStoreInterface):
    """JSON file-based temporary storage implementation.

    Stores reports temporarily when StandCloud sync fails using JSON files.
    """

    def __init__(self) -> None:
        self._log = getLogger(__name__)
        config = ConfigManager()
        config_storage_path = Path(config.config.database.storage_path)
        if config_storage_path.is_absolute():
            self._storage_dir = config_storage_path / "storage" / "tempstore"
        else:
            self._storage_dir = Path(
                config.tests_path
                / config.config.database.storage_path
                / "storage"
                / "tempstore",
            )
        self._storage_dir.mkdir(parents=True, exist_ok=True)
        self._schema = ResultRunStore

    def push_report(self, report: ResultRunStore) -> bool:
        """Push report to the temporary storage.

        Args:
            report (ResultRunStore): report to store

        Returns:
            bool: True if successful, False otherwise
        """
        report_dict = report.model_dump()
        report_dict.pop("id", None)
        report_id = str(uuid7())
        report_dict["_id"] = report_id
        report_dict["_rev"] = report_id
        report_file = self._storage_dir / f"{report_id}.json"

        try:
            with report_file.open("w") as f:
                json.dump(report_dict, f, indent=2, default=str)
        except Exception as exc:  # noqa: BLE001
            self._log.error(f"Error while saving report {report_id}: {exc}")
            return False
        else:
            self._log.debug(f"Report saved with id: {report_id}")
            return True

    def reports(self) -> Generator[dict]:
        """Get all reports from the temporary storage.

        Yields:
            dict: report from temporary storage
        """
        for report_file in self._storage_dir.glob("*.json"):
            try:
                with report_file.open("r") as f:
                    report_dict = json.load(f)
                yield report_dict
            except Exception as exc:  # noqa: BLE001, PERF203
                self._log.error(f"Error loading report from {report_file}: {exc}")
                continue

    def delete(self, report_id: str) -> bool:
        """Delete report from the temporary storage.

        Args:
            report_id (str): report ID to delete

        Returns:
            bool: True if successful, False otherwise
        """
        report_file = self._storage_dir / f"{report_id}.json"
        try:
            report_file.unlink()
        except FileNotFoundError:
            self._log.warning(f"Report {report_id} not found in temporary storage")
            return False
        except Exception as exc:  # noqa: BLE001
            self._log.error(f"Error deleting report {report_id}: {exc}")
            return False
        else:
            return True


class CouchDBTempStore(TempStoreInterface):
    """CouchDB-based temporary storage implementation.

    Stores reports temporarily when StandCloud sync fails using CouchDB.
    """

    def __init__(self) -> None:
        from pycouchdb import Server as DbServer  # type: ignore[import-untyped]
        from pycouchdb.exceptions import Conflict  # type: ignore[import-untyped]

        self._log = getLogger(__name__)
        config = ConfigManager()
        self._db_srv = DbServer(config.config.database.url)
        self._db_name = "tempstore"
        self._schema = ResultRunStore

        try:
            self._db = self._db_srv.create(self._db_name)
        except Conflict:
            # database already exists
            self._db = self._db_srv.database(self._db_name)

    def push_report(self, report: ResultRunStore) -> bool:
        """Push report to the temporary storage.

        Args:
            report (ResultRunStore): report to store

        Returns:
            bool: True if successful, False otherwise
        """
        from pycouchdb.exceptions import Conflict  # type: ignore[import-untyped]

        report_dict = report.model_dump()
        report_id = report_dict.pop("id", None)
        if not report_id:
            self._log.error("Report missing required 'id' field")
            return False
        try:
            self._db.save(report_dict)
        except Conflict as exc:
            self._log.error(f"Error while saving report {report_id}: {exc}")
            return False
        else:
            self._log.debug(f"Report saved with id: {report_id}")
            return True

    def reports(self) -> Generator[dict]:
        """Get all reports from the temporary storage.

        Yields:
            dict: report from temporary storage
        """
        yield from self._db.all()

    def delete(self, report_id: str) -> bool:
        """Delete report from the temporary storage.

        Args:
            report_id (str): report ID to delete

        Returns:
            bool: True if successful, False otherwise
        """
        from pycouchdb.exceptions import (  # type: ignore[import-untyped]
            Conflict,
            NotFound,
        )

        try:
            self._db.delete(report_id)
        except (NotFound, Conflict):
            return False
        else:
            return True


class TempStore(metaclass=SingletonMeta):
    """HardPy temporary storage factory for data synchronization.

    Creates appropriate storage backend based on configuration:
    - JSON file storage when storage_type is "json"
    - CouchDB storage when storage_type is "couchdb"

    This ensures temporary reports are stored in the same backend as the main data.

    Note: This class acts as a factory. When instantiated, it returns
    the appropriate concrete implementation (JsonTempStore or CouchDBTempStore).
    """

    def __new__(cls) -> TempStoreInterface:  # type: ignore[misc]
        """Create and return the appropriate storage implementation.

        Returns:
            TempStoreInterface: Concrete storage implementation based on config
        """
        config = ConfigManager()
        storage_type = config.config.database.storage_type

        if storage_type == StorageType.JSON:
            return JsonTempStore()
        if storage_type == StorageType.COUCHDB:
            return CouchDBTempStore()
        msg = f"Unknown storage type: {storage_type}"
        raise ValueError(msg)
