# Copyright (c) 2025 Everypin
# GNU General Public License v3.0 (see LICENSE or https://www.gnu.org/licenses/gpl-3.0.txt)

from http import HTTPStatus

from pydantic import ValidationError

from hardpy.common.stand_cloud.exception import StandCloudError
from hardpy.pytest_hardpy.db.schema import ResultRunStore
from hardpy.pytest_hardpy.db.tempstore import TempStore
from hardpy.pytest_hardpy.result.report_loader.stand_cloud_loader import (
    StandCloudLoader,
)


class StandCloudSynchronizer:
    """Synchronize reports with StandCloud."""

    def __init__(self) -> None:
        self._tempstore = TempStore()

    def sync(self) -> str:
        """Sync reports with StandCloud.

        Returns:
            str: Synchronization message
        """
        invalid_reports = []
        success_report_counter = 0
        try:
            loader = StandCloudLoader()
            response = loader.healthcheck()
        except StandCloudError as exc:
            return f"StandCloud service is not available: {exc}"
        for _report in self._tempstore.reports():
            try:
                report_id = _report.get("id")
                document: dict = _report.get("doc")
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
                schema_report = self._tempstore.dict_to_schema(document)
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
            if not self._tempstore.delete(report_id):
                reason = f"Report {report_id} not deleted from the temporary storage"
                invalid_reports.append({report_id: reason})
            success_report_counter += 1
        if success_report_counter:
            msg = (
                f"Reports successfully uploaded to StandCloud: {success_report_counter}"
            )
        if invalid_reports:
            msg += "\nInvalid reports:\n\n"
            for _report in invalid_reports:
                report_id, reason = next(iter(_report.items()))
                msg += f"{report_id}: {reason}\n"
        return msg

    def push_to_tempstore(self, report: ResultRunStore) -> bool:
        """Push report to the report database.

        Args:
            report (ResultRunStore): report

        Returns:
            bool: True if success, else False
        """
        return self._tempstore.push_report(report)
