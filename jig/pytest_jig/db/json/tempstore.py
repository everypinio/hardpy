# Copyright (c) 2026 Everypin
# GNU General Public License v3.0 (see LICENSE or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import annotations

import json
from logging import getLogger
from pathlib import Path
from typing import TYPE_CHECKING

from uuid6 import uuid7

from jig.common.config import ConfigManager
from jig.pytest_jig.db.common import TempStorageInterface
from jig.pytest_jig.db.schema import ResultRunStore

if TYPE_CHECKING:
    from collections.abc import Generator


class JsonTempStore(TempStorageInterface):
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
