# Copyright (c) 2025 Everypin
# GNU General Public License v3.0 (see LICENSE or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import annotations

from typing import TYPE_CHECKING
from urllib.parse import urlencode

from oauthlib.oauth2.rfc6749.errors import OAuth2Error
from requests.exceptions import RequestException

from hardpy.common.stand_cloud.connector import StandCloudConnector, StandCloudError

if TYPE_CHECKING:
    from typing import Any

    from requests import Response
    from requests_oauth2client import ApiClient


class StandCloudReader:
    """StandCloud data reader.

    The link to the documentation can be obtained by address:
    https://service_name/integration/api/v1/docs

    For example:
    https://demo.standcloud.io/integration/api/v1/docs
    """

    def __init__(self, sc_connector: StandCloudConnector) -> None:
        """Create StandCloud reader.

        Args:
            sc_connector (StandCloudConnector): StandCloud connector
        """
        self._verify_ssl = not __debug__
        self._sc_connector = sc_connector

    def request(self, endpoint: str, params: dict[str, Any] | None = None) -> Response:
        """Get data from endpoint.

        Args:
            endpoint (str): endpoint address.
            params (dict[str, Any] | None, optional): endpoint parameters.
                Defaults to None.

        Returns:
            Response: endpoint data.
        """
        return self._request(endpoint=endpoint, params=params)

    def test_run(
        self,
        run_id: str | None = None,
        params: dict[str, Any] | None = None,
    ) -> Response:
        """Get run data from '/test_run' endpoint.

        Args:
            run_id (str): UUIDv4 test run identifier.
                Example: "3fa85f64-5717-4562-b3fc-2c963f66afa6"
            params (dict[str, Any] | None, optional): test_run parameters.
                Defaults to None.

        Returns:
            Response: test run data.
        """
        if run_id is not None and params is not None:
            msg = "run_id and params are mutually exclusive"
            raise ValueError(msg)
        if run_id is not None:
            return self._request(endpoint=f"test_run/{run_id}")
        return self._request(endpoint="test_run", params=params)

    def tested_dut(self, params: dict[str, Any]) -> Response:
        """Get tested DUT's data from '/tested_dut' endpoint.

        Args:
            params (dict[str, Any]): tested DUT filters:
                Examples: {
                    "test_stand_name": "Stand 1",
                    "part_number": "part_number_1",
                    "firmware_version": "1.2.3",
                }

        Returns:
            Response: tested dut data.
        """
        return self._request(endpoint="tested_dut", params=params)

    def _request(self, endpoint: str, params: dict[str, Any] | None = None) -> Response:
        api = self._build_api(endpoint=endpoint, params=params)
        try:
            resp = api.get(verify=self._verify_ssl)
        except RuntimeError as exc:
            raise StandCloudError(str(exc)) from exc
        except OAuth2Error as exc:
            raise StandCloudError(exc.description) from exc
        except RequestException as exc:
            return exc.response  # type: ignore

        return resp

    def _build_api(self, endpoint: str, params: dict | None = None) -> ApiClient:
        if params is None:
            return self._sc_connector.get_api(f"{endpoint}")
        encoded_params = urlencode(params)
        return self._sc_connector.get_api(f"{endpoint}?{encoded_params}")
