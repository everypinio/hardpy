# Copyright (c) 2025 Everypin
# GNU General Public License v3.0 (see LICENSE or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import annotations

from http import HTTPStatus
from typing import TYPE_CHECKING

from pydantic import ValidationError

from hardpy.common.stand_cloud.exception import StandCloudError
from hardpy.pytest_hardpy.db.tempstore import CouchDBTempStore, TempStore
from hardpy.pytest_hardpy.result.report_loader.stand_cloud_loader import (
    StandCloudLoader,
)

if TYPE_CHECKING:
    from hardpy.pytest_hardpy.db.schema import ResultRunStore


class StandCloudSynchronizer:
    """Synchronize reports with StandCloud."""

    def __init__(self) -> None:
        self._tempstore: TempStore | None = None

    @property
    def _get_tempstore(self) -> TempStore:
        """Get TempStore instance lazily.

        Returns:
            TempStore: TempStore singleton instance
        """
        if self._tempstore is None:
            self._tempstore = TempStore()
        return self._tempstore

    def sync(self) -> str:
        """Sync reports with StandCloud.

        Returns:
            str: Synchronization message
        """
        _tempstore = self._get_tempstore
        if not self._get_tempstore.reports():
            return "All reports are synchronized with StandCloud"
        loader = self._create_sc_loader()

        invalid_reports = []
        success_report_counter = 0
        for _report in self._get_tempstore.reports():
            try:
                if isinstance(_tempstore, CouchDBTempStore):
                    document: dict = _report.get("doc")  # type: ignore[assignment]
                    report_id: str = _report.get("id")  # type: ignore[assignment]
                else:
                    document: dict = _report
                    report_id: str = _report.get("_id")
                document.pop("rev")
            except KeyError:
                try:
                    document.pop("_rev")
                except KeyError:
                    reason = (
                        "The rev (or _rev) field is missing from the original report."
                    )
                    invalid_reports.append({report_id: reason})
                    continue
            try:
                schema_report = self._get_tempstore.dict_to_schema(document)
            except ValidationError as exc:
                reason = f"Report has invalid format: {exc}"
                invalid_reports.append({report_id: reason})
                continue
            try:
                response = loader.load(schema_report)
            except StandCloudError as exc:
                reason = f"StandCloud service problem: {exc}"
                invalid_reports.append({report_id: reason})
                continue
            if response.status_code != HTTPStatus.CREATED:
                reason = f"Staus code: {response.status_code}, text: {response.text}"
                invalid_reports.append({report_id: reason})
                continue
            if not self._get_tempstore.delete(report_id):
                reason = f"Report {report_id} not deleted from the temporary storage"
                invalid_reports.append({report_id: reason})
            success_report_counter += 1
        return self._create_sync_message(success_report_counter, invalid_reports)

    def push_to_tempstore(self, report: ResultRunStore) -> bool:
        """Push report to the report database.

        Args:
            report (ResultRunStore): report

        Returns:
            bool: True if success, else False
        """
        return self._get_tempstore.push_report(report)

    def push_to_sc(self, report: ResultRunStore) -> bool:
        """Push report to the StandCloud.

        Args:
            report (ResultRunStore): report
        """
        try:
            loader = self._create_sc_loader()
        except StandCloudError:
            return False
        try:
            response = loader.load(report)
        except StandCloudError:
            return False
        return response.status_code == HTTPStatus.CREATED

    def _create_sync_message(self, success_report: int, invalid_reports: list) -> str:
        msg = ""
        if success_report:
            msg = f"Reports successfully uploaded to StandCloud: {success_report}"
        if invalid_reports:
            msg += "\nInvalid reports:\n\n"
            for _report in invalid_reports:
                report_id, reason = next(iter(_report.items()))
                msg += f"Report id: {report_id}: {reason}\n"
            raise StandCloudError(msg)
        if not msg:
            msg = "All reports are synchronized with StandCloud"
        return msg

    def _create_sc_loader(self) -> StandCloudLoader:
        loader = StandCloudLoader()
        response = loader.healthcheck()
        if response.status_code != HTTPStatus.OK:
            url = response.url
            code = response.status_code
            msg = f"StandCloud healthcheck at {url} is unavailable, status code: {code}"
            raise StandCloudError(msg)
        # if the response.text contains invalid page data but status code is 200:
        if response.status_code == HTTPStatus.OK and response.text != "{}":
            msg = f"StandCloud healthcheck at {response.url} is unavailable"
            raise StandCloudError(msg)
        return loader
