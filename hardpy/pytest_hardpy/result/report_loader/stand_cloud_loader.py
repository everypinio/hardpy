# Copyright (c) 2024 Everypin
# GNU General Public License v3.0 (see LICENSE or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import annotations

from typing import TYPE_CHECKING

from oauthlib.oauth2.rfc6749.errors import OAuth2Error
from requests.exceptions import HTTPError

from hardpy.common.stand_cloud.connector import StandCloudConnector, StandCloudError
from hardpy.pytest_hardpy.utils import ConnectionData

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
        connection_data = ConnectionData()
        sc_addr = address if address else connection_data.sc_address
        self._sc_connector = StandCloudConnector(sc_addr)

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
        api = self._sc_connector.get_api("test_report")

        try:
            resp = api.post(
                verify=self._verify_ssl,
                json=report.model_dump(),
                timeout=timeout,
            )
        except RuntimeError as exc:
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
