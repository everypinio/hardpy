# Copyright (c) 2026 Everypin
# GNU General Public License v3.0 (see LICENSE or https://www.gnu.org/licenses/gpl-3.0.txt)

from collections.abc import Generator
from logging import getLogger

from pycouchdb import Server as DbServer
from pycouchdb.exceptions import (
    Conflict,
    NotFound,
)

from jig.common.config import ConfigManager
from jig.pytest_jig.db.common import TempStorageInterface
from jig.pytest_jig.db.schema import ResultRunStore


class CouchDBTempStore(TempStorageInterface):
    """CouchDB-based temporary storage implementation.

    Stores reports temporarily when StandCloud sync fails using CouchDB.
    """

    def __init__(self) -> None:
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
        try:
            self._db.delete(report_id)
        except (NotFound, Conflict):
            return False
        else:
            return True
