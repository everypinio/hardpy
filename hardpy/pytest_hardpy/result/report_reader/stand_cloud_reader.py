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
    """StandCloud data reader."""

    def __init__(self, sc_connector: StandCloudConnector) -> None:
        """Create StandCloud reader.

        Args:
            sc_connector (StandCloudConnector): StandCloud connector
        """
        self._verify_ssl = not __debug__
        self._sc_connector = sc_connector

    def raw_request(self, endpoint: str, params: dict[str, Any] | None = None) -> Response:  # noqa: E501
        """Raw request to StandCloud API.

        The user defines the endpoint himself.
        Not recommended for use, if there is a request for a specific endpoint.
        """
        api = self._build_api(endpoint=endpoint, params=params)
        return self._request(api)

    def tested_dut(self, params: dict[str, Any]) -> Response:
        """Get tested DUT data from '/tested_dut' endpoint.

        Args:
            params (dict[str, Any]): _description_

        Returns:
            Response: tested dut data.
        """
        api = self._build_api(endpoint="tested_dut", params=params)
        return self._request(api)

    def _build_api(self, endpoint: str, params: dict | None = None) -> ApiClient:
        if params is None:
            return self._sc_connector.get_api(f"{endpoint}")
        encoded_params = urlencode(params)
        return self._sc_connector.get_api(f"{endpoint}?{encoded_params}")

    def _request(self, api: ApiClient) -> Response:
        try:
            resp = api.get(verify=self._verify_ssl)
        except RuntimeError as exc:
            raise StandCloudError(str(exc)) from exc
        except OAuth2Error as exc:
            raise StandCloudError(exc.description) from exc
        except RequestException as exc:
            return exc.response  # type: ignore

        return resp
