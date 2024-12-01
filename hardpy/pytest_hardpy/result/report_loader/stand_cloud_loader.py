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

    def __init__(self, verify_ssl: bool = False) -> None:
        """Create StandCLoud loader.

        Args:
            verify_ssl (bool, optional): Skips SSL checks.
            The option only for development and debug. Defaults to False.
        """
        connection_data = ConnectionData()
        self._verify_ssl = verify_ssl
        self._sc_connector = StandCloudConnector(
            connection_data.stand_cloud_api,
            connection_data.stand_cloud_auth,
            verify_ssl,
        )

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
            raise StandCloudError(exc.description)  # type: ignore
        except TokenExpiredError as exc:
            raise StandCloudError(exc.description)
        except InvalidGrantError as exc:
            raise StandCloudError(exc.description)
        except HTTPError as exc:
            raise StandCloudError(exc.description)

        if resp.status_code != HTTPStatus.CREATED:
            msg = f"Report not uploaded to StandCloud, response code {resp.status_code}"
            raise StandCloudError(msg)

    def healthcheck(self) -> None:
        """Healthcheck of StandCloud API.

        Raises:
            StandCloudError: if StandCloud is unavailable
        """
        self._sc_connector.healthcheck()
