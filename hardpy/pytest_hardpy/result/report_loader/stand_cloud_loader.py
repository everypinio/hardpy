# Copyright (c) 2024 Everypin
# GNU General Public License v3.0 (see LICENSE or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import annotations

from http import HTTPStatus
from typing import TYPE_CHECKING

from oauthlib.oauth2.rfc6749.errors import InvalidGrantError, TokenExpiredError
from requests.exceptions import HTTPError
from requests_oauth2client.tokens import ExpiredAccessToken

from hardpy.common.stand_cloud.connector import StandCloudConnector, StandCloudError
from hardpy.pytest_hardpy.utils import ConnectionData

if TYPE_CHECKING:
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

    def load(self, report: ResultRunStore) -> None:
        """Load report to the StandCloud.

        Args:
            report (ResultRunStore): report

        Raises:
            StandCloudError: if report not uploaded to StandCloud
        """
        api = self._sc_connector.get_api("api/test_run")

        try:
            resp = api.post(verify=self._verify_ssl, json=report.model_dump())
        except ExpiredAccessToken as exc:
            raise StandCloudError(str(exc))  # type: ignore
        except TokenExpiredError as exc:
            raise StandCloudError(exc.description)
        except InvalidGrantError as exc:
            raise StandCloudError(exc.description)
        except HTTPError as exc:
            raise StandCloudError(exc.args)  # type: ignore

        if resp.status_code != HTTPStatus.CREATED:
            msg = f"Report not uploaded to StandCloud, response code {resp.status_code}"
            raise StandCloudError(msg)

    def healthcheck(self) -> None:
        """Healthcheck of StandCloud API.

        Raises:
            StandCloudError: if StandCloud is unavailable
        """
        self._sc_connector.healthcheck()
