# Copyright (c) 2024 Everypin
# GNU General Public License v3.0 (see LICENSE or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import annotations

import json
from logging import getLogger
from pathlib import Path
from typing import TYPE_CHECKING

from uuid6 import uuid7

if TYPE_CHECKING:
    from hardpy.pytest_hardpy.db.schema import ResultRunStore


class JsonLoader:
    """JSON report generator."""

    def __init__(self, storage_dir: Path | None = None) -> None:
        if not storage_dir:
            storage_dir = Path.cwd() / "reports"
        self._storage_dir = storage_dir
        self._storage_dir.mkdir(parents=True, exist_ok=True)
        self._log = getLogger(__name__)

    def load(self, report: ResultRunStore, new_report_id: str | None = None) -> bool:
        """Load report to the report database.

        Args:
            report (ResultRunStore): report
            new_report_id (str | None, optional): user's report ID. Defaults to uuid7.

        Returns:
            bool: True if success, else False
        """
        report_dict = report.model_dump()
        report_id = new_report_id if new_report_id else str(uuid7())
        report_dict["id"] = report_id
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
