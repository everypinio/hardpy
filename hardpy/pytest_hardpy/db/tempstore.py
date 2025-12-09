# Copyright (c) 2025 Everypin
# GNU General Public License v3.0 (see LICENSE or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import annotations

import json
from logging import getLogger
from pathlib import Path
from typing import TYPE_CHECKING
from uuid import uuid4

from hardpy.common.config import ConfigManager
from hardpy.common.singleton import SingletonMeta
from hardpy.pytest_hardpy.db.schema import ResultRunStore

if TYPE_CHECKING:
    from collections.abc import Generator


class TempStore(metaclass=SingletonMeta):
    """HardPy temporary storage for data syncronization.

    Stores reports temporarily when StandCloud sync fails. Uses JSON files
    regardless of the configured storage type to ensure reports are not lost
    even if the main storage backend is unavailable.
    """

    def __init__(self) -> None:
        self._log = getLogger(__name__)
        config = ConfigManager()
        self._storage_dir = Path(config.config.database.storage_path) / "tempstore"

        # Only create directory for JSON storage
        # CouchDB stores data directly in the database, no local .hardpy needed
        # JSON storage needs .hardpy/tempstore for StandCloud sync failures
        if config.config.database.storage_type == "json":
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
        report_id = report_dict.get("id", str(uuid4()))
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

    def reports(self) -> Generator[ResultRunStore]:
        """Get all reports from the temporary storage.

        Yields:
            ResultRunStore: report from temporary storage
        """
        for report_file in self._storage_dir.glob("*.json"):
            try:
                with report_file.open("r") as f:
                    report_dict = json.load(f)
                yield self._schema(**report_dict)
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

    def dict_to_schema(self, report: dict) -> ResultRunStore:
        """Convert report dict to report schema.

        Args:
            report (dict): report dictionary

        Returns:
            ResultRunStore: validated report schema
        """
        return self._schema(**report)
