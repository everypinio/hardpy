# Copyright (c) 2024 Everypin
# GNU General Public License v3.0 (see LICENSE or https://www.gnu.org/licenses/gpl-3.0.txt)

from logging import getLogger
from uuid import uuid4

from pycouchdb import Server as DbServer
from pycouchdb.client import Database
from pycouchdb.exceptions import Conflict

from hardpy.pytest_hardpy.db.schema import ResultRunStore
from hardpy.pytest_hardpy.result.couchdb_config import CouchdbConfig


class CouchdbLoader:
    """CouchDB report generator."""

    def __init__(self, config: CouchdbConfig) -> None:
        self._log = getLogger(__name__)
        self._config: CouchdbConfig = config
        self._db_srv = DbServer(config.connection_string)
        self._db: Database = self._init_db()

    def load(self, report: ResultRunStore) -> bool:
        """Load report to the report database.

        Args:
            report (ResultRunStore): report

        Returns:
            bool: True if success, else False
        """
        report_id = self._get_report_id(report)
        report_dict = self._schema_to_dict(report, report_id)
        try:
            self._db.save(report_dict)
        except Conflict as exc:
            self._log.error(f"Error while saving report {report_id}: {exc}")
            return False
        self._log.debug(f"Report saved with id: {report_id}")
        return True

    def _init_db(self) -> Database:
        try:
            return self._db_srv.create(self._config.db_name)  # type: ignore
        except Conflict:
            # database is already created
            return self._db_srv.database(self._config.db_name)

    def _get_report_id(self, report: ResultRunStore) -> str:
        timestamp = report.stop_time
        device_serial_number = report.dut.serial_number
        if not device_serial_number:
            self._log.warning("Device serial number is not provided in the report.")
            return f"report_{timestamp}_no_serial_{str(uuid4())[:6]}"
        return f"report_{timestamp}_{device_serial_number}"

    def _schema_to_dict(self, report: ResultRunStore, report_id: str) -> dict:
        report_dict = report.model_dump()
        report_dict.pop("rev")
        report_dict.pop("id")
        report_dict["_id"] = report_id
        return report_dict
