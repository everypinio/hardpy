# Copyright (c) 2026 Everypin
# GNU General Public License v3.0 (see LICENSE or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import annotations

from logging import getLogger
from typing import TYPE_CHECKING

import requests
from requests.exceptions import RequestException
from requests_oauth2client import ApiClient
from requests_oauth2client.tokens import ExpiredAccessToken

from hardpy.common.stand_cloud.exception import StandCloudError
from hardpy.common.stand_cloud.utils import StandCloudAPIMode, StandCloudAddr

if TYPE_CHECKING:
    from requests import Response


class StandCloudConnector:
    """StandCloud API connector."""

    def __init__(
        self,
        addr: str = "standcloud.everypin.io",
        api_mode: StandCloudAPIMode = StandCloudAPIMode.HARDPY,
        api_version: int = 1,
        api_key: str | None = None,
    ) -> None:
        """Create StandCloud API connector.

        Args:
            addr (str): StandCloud service name.
            api_mode (StandCloudAPIMode): StandCloud API mode,
                hardpy for test stand, integration for third-party service.
                Default: StandCloudAPIMode.HARDPY.
            api_version (int): StandCloud API version.
                Default: 1.
            api_key (str | None): StandCloud API key.
                Default: None.
        """
        https_prefix = "https://"
        auth_addr = addr + "/auth"

        self._addr: StandCloudAddr = StandCloudAddr(
            domain=addr,
            api=https_prefix + addr + f"/{api_mode.value}/api/v{api_version}",
            token=https_prefix + auth_addr + "/api/oidc/token",
            auth=https_prefix + auth_addr + "/api/oidc/authorization",
            device=https_prefix + auth_addr + "/api/oidc/device-authorization",
        )

        self._client_id = "hardpy-report-uploader"
        self._verify_ssl = not __debug__
        self._api_key = api_key
        self._log = getLogger(__name__)

    @property
    def addr(self) -> str:
        """Get StandCloud service name."""
        return self._addr.domain

    @property
    def api_url(self) -> str:
        """Get StandCloud API URL."""
        return self._addr.api

    def get_api(self, endpoint: str) -> ApiClient:
        """Get StandCloud API client.

        Args:
            endpoint (str): endpoint address.

        Returns:
            ApiClient: API clinet
        """
        return self._get_api(endpoint)

    def healthcheck(self) -> Response:
        """Healthcheck of StandCloud API.

        Returns:
            Response: healthcheck response

        Raises:
            StandCloudError: if StandCloud is unavailable
        """
        api = self._get_api("healthcheck")

        try:
            resp = api.get(verify=self._verify_ssl)
        except ExpiredAccessToken as exc:
            raise StandCloudError(str(exc)) from exc
        except RequestException as exc:
            raise StandCloudError(exc.strerror or str(exc)) from exc  # type: ignore
        except Exception as exc:
            raise StandCloudError(exc) from exc

        return resp

    def _get_api(self, endpoint: str) -> ApiClient:
        if self._api_key:
            session = requests.Session()
            session.headers["Authorization"] = f"Bearer {self._api_key}"
            return ApiClient(
                f"{self._addr.api}/{endpoint}",
                session=session,
                timeout=10,
            )

        msg = f"API key for {self._addr.domain} is not set."
        raise StandCloudError(msg)
