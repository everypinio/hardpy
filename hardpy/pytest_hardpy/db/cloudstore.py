# Copyright (c) 2025 Everypin
# GNU General Public License v3.0 (see LICENSE or https://www.gnu.org/licenses/gpl-3.0.txt)

from logging import getLogger

from pycouchdb.exceptions import Conflict

from hardpy.common.singleton import SingletonMeta
from hardpy.pytest_hardpy.db.base_store import BaseStore
from hardpy.pytest_hardpy.db.schema import ResultRunStore


class CloudStore(BaseStore, metaclass=SingletonMeta):
    """HardPy temporary storage for data syncronization."""

    def __init__(self) -> None:
        super().__init__("cloudstore")
        self._log = getLogger(__name__)
        self._doc: dict = self._init_doc()
        self._schema = ResultRunStore

    def push_report(self, report: ResultRunStore) -> bool:
        """Push report to the report database."""
        report_dict = report.model_dump()
        report_id = report_dict.pop("id")
        report_dict["_id"] = report_id
        try:
            self._db.save(report_dict)
        except Conflict as exc:
            self._log.error(f"Error while saving report {report_id}: {exc}")
            return False
        self._log.debug(f"Report saved with id: {report_id}")
        return True
