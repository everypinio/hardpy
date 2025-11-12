# Copyright (c) 2024 Everypin
# GNU General Public License v3.0 (see LICENSE or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import annotations

from typing import TYPE_CHECKING

from oauthlib.oauth2.rfc6749.errors import OAuth2Error
from requests.exceptions import ConnectionError, HTTPError  # noqa: A004

from hardpy.common.config import ConfigManager
from hardpy.common.stand_cloud.connector import StandCloudConnector, StandCloudError

if TYPE_CHECKING:
    from requests import Response

    from hardpy.pytest_hardpy.db.schema import ResultRunStore


class StandCloudLoader:
    """StandCloud report generator."""

    def __init__(self, address: str | None = None) -> None:
        """Create StandCLoud loader.

        Args:
            address (str | None, optional): StandCloud address.
                     Defaults to None (the value is taken from the.toml).
                     Can be used outside of HardPy applications.
        """
        self._verify_ssl = not __debug__
        config_manager = ConfigManager()
        sc_addr = address if address else config_manager.config.stand_cloud.address
        api_key = config_manager.config.stand_cloud.api_key
        self._sc_connector = StandCloudConnector(sc_addr, api_key=api_key)

    def load(self, report: ResultRunStore, timeout: int = 20) -> Response:
        """Load report to the StandCloud.

        Args:
            report (ResultRunStore): report
            timeout (int, optional): post timeout in seconds. Defaults to 20.
                                    High timeout value on poor network connections.

        Returns:
            Response: StandCloud load response, must be 201

        Raises:
            StandCloudError: if report not uploaded to StandCloud
        """
        try:
            api = self._sc_connector.get_api("test_report")
        except ConnectionError as exc:
            raise StandCloudError(str(exc)) from exc
        sc_report = self._convert_to_sc_format(report)

        try:
            resp = api.post(
                verify=self._verify_ssl,
                json=sc_report.model_dump(),
                timeout=timeout,
            )
        except (RuntimeError, ConnectionError) as exc:
            raise StandCloudError(str(exc)) from exc
        except OAuth2Error as exc:
            raise StandCloudError(exc.description) from exc
        except HTTPError as exc:
            return exc.response  # type: ignore

        return resp

    def healthcheck(self) -> Response:
        """Healthcheck of StandCloud API.

        Returns:
            Response: StandCloud healthcheck response, must be 200

        Raises:
            StandCloudError: if StandCloud is unavailable
        """
        return self._sc_connector.healthcheck()

    def _convert_to_sc_format(self, report: ResultRunStore) -> ResultRunStore:
        """Convert report to StandCloud format.

        StandCloud expects parameters to be not empty.
        If a parameter is None, it will be replaced with "unknown".
        """
        unknown_param = "unknown"
        # test stand name
        if not report.test_stand.name:
            report.test_stand.name = unknown_param
        # DUT part number
        if not report.dut.part_number:
            report.dut.part_number = unknown_param
        # DUT name
        if not report.dut.name:
            report.dut.name = report.dut.part_number
        # sub unit part number and name
        for sub_unit in report.dut.sub_units:
            if not sub_unit.part_number:
                sub_unit.part_number = unknown_param
            if not sub_unit.name:
                sub_unit.name = sub_unit.part_number
        # instrument part number and name
        for instrument in report.test_stand.instruments:
            if not instrument.part_number:
                instrument.part_number = unknown_param
            if not instrument.name:
                instrument.name = instrument.part_number
        return report
