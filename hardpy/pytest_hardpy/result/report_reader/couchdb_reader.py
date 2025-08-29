# Copyright (c) 2024 Everypin
# GNU General Public License v3.0 (see LICENSE or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import annotations

from dataclasses import dataclass
from logging import getLogger
from typing import TYPE_CHECKING

from pycouchdb import Server as DbServer
from pycouchdb.exceptions import NotFound

from hardpy.pytest_hardpy.db import DatabaseField as DF  # noqa: N817
from hardpy.pytest_hardpy.utils.const import TestStatus

if TYPE_CHECKING:
    from pycouchdb.client import Database

    from hardpy.pytest_hardpy.result.couchdb_config import CouchdbConfig


@dataclass
class ReportInfo:
    """CouchDB report info."""

    name: str
    status: str
    start_time: str
    end_time: str
    first_failed_test_name: str | None
    first_failed_test_id: str | None


class CouchdbReader:
    """CouchDB report info reader."""

    def __init__(self, config: CouchdbConfig) -> None:
        self._log = getLogger(__name__)
        self._config = config
        self._db_srv = DbServer(config.connection_string)
        self._db: Database = self._init_db()
        self._doc_id = "doc"

    def get_report_total_count(self) -> int:
        """Get the total number of reports in the database.

        Returns:
            int: total number of reports
        """
        return sum(1 for _ in self._db.all())

    def get_report_count_in_timeframe(self, start_time: int, end_time: int) -> int:
        """Get the number of reports in the database within the specified timeframe.

        Args:
            start_time (int): start time
            end_time (int): end time

        Raises:
            ValueError: if start time or end time is negative

        Returns:
            int: number of reports
        """
        if start_time < 0 or end_time < 0:
            msg = "Start time and end time must be positive values"
            raise ValueError(msg)
        return sum(
            1
            for report in self._db.all()
            if self._is_in_timeframe(
                self._get_start_time_from_db(report[self._doc_id]),  # type: ignore
                self._get_stop_time_from_db(report[self._doc_id]),  # type: ignore
                start_time,
                end_time,
            )
        )

    def get_report_status(self, report_name: str) -> str:
        """Get the status of a report by its name.

        Args:
            report_name (str): report name

        Raises:
            ValueError: if the report status is not valid

        Returns:
            str: report status
        """
        doc = self._db.get(report_name)
        return doc[DF.STATUS]

    def get_report_infos(self) -> list[ReportInfo]:
        """Get a list of information about all reports in the database.

        Returns:
            List[ReportInfo]: list of report information
        """
        reports_info = []
        reports = self._db.all()
        for report in reports:
            report_info = self._get_single_report_info(report)
            reports_info.append(report_info)
        return reports_info

    def get_report_infos_in_timeframe(
        self,
        start_time: int,
        end_time: int,
    ) -> list[ReportInfo]:
        """Get a list of information about reports in a timeframe in the database.

        Args:
            start_time (int): start time
            end_time (int): end time

        Raises:
            ValueError: if start time or end time is negative

        Returns:
            List[ReportInfo]: list of report information
        """
        if start_time < 0 or end_time < 0:
            msg = "Start time and end time must be positive values"
            raise ValueError(msg)

        reports_info = []
        reports = self._db.all()
        for report in reports:
            start_t_db = self._get_start_time_from_db(report[self._doc_id])
            stop_t_db = self._get_stop_time_from_db(report[self._doc_id])
            if self._is_in_timeframe(start_t_db, stop_t_db, start_time, end_time):  # type: ignore
                report_info = self._get_single_report_info(report)
                reports_info.append(report_info)
        return reports_info

    def _init_db(self) -> Database:
        try:
            return self._db_srv.database(self._config.db_name)
        except NotFound as exc:
            self._log.error(f"Error initializing database: {exc}")
            msg = "Error initializing database"
            raise RuntimeError(msg) from exc

    def _get_start_time_from_db(self, doc: dict) -> str:
        return doc[DF.START_TIME]

    def _get_stop_time_from_db(self, doc: dict) -> str:
        return doc[DF.STOP_TIME]

    def _get_single_report_info(self, report: dict) -> ReportInfo:
        first_failed_test_name = None
        first_failed_test_id = None
        report_doc = report[self._doc_id]
        for module_info in report_doc[DF.MODULES].values():
            for case_name, case_info in module_info[DF.CASES].items():
                if case_info[DF.STATUS] == TestStatus.FAILED:
                    first_failed_test_name = case_info[DF.NAME]
                    first_failed_test_id = case_name
        return ReportInfo(
            name=report_doc["_id"],
            status=report_doc[DF.STATUS],
            start_time=self._get_start_time_from_db(report_doc),
            end_time=self._get_stop_time_from_db(report_doc),
            first_failed_test_name=first_failed_test_name,
            first_failed_test_id=first_failed_test_id,
        )

    def _is_in_timeframe(
        self,
        start: int,
        end: int,
        timeframe_start: int,
        timeframe_end: int,
    ) -> bool:
        return timeframe_start <= start and end <= timeframe_end
