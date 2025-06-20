# Copyright (c) 2024 Everypin
# GNU General Public License v3.0 (see LICENSE or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import annotations

import json
from datetime import datetime, timedelta, timezone
from logging import getLogger
from time import sleep
from typing import TYPE_CHECKING

import requests
from oauthlib.oauth2.rfc6749.errors import OAuth2Error
from requests.exceptions import RequestException
from requests_oauth2client import ApiClient, BearerToken
from requests_oauth2client.tokens import ExpiredAccessToken

from hardpy.common.stand_cloud.exception import StandCloudError
from hardpy.common.stand_cloud.oauth2 import OAuth2
from hardpy.common.stand_cloud.token_manager import TokenManager
from hardpy.common.stand_cloud.utils import StandCloudAPIMode, StandCloudAddr

if TYPE_CHECKING:
    from requests import Response


class StandCloudConnector:
    """StandCloud API connector."""

    def __init__(
        self,
        addr: str,
        api_mode: StandCloudAPIMode = StandCloudAPIMode.HARDPY,
        api_version: int = 1,
    ) -> None:
        """Create StandCloud API connector.

        Args:
            addr (str): StandCloud service name.
            api_mode (StandCloudAPIMode): StandCloud API mode,
                hardpy for test stand, integration for third-party service.
                Default: StandCloudAPIMode.HARDPY.
            api_version (int): StandCloud API version.
                Default: 1.
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
        self.verify_ssl = not __debug__
        self._token_manager = TokenManager(self._addr.domain)
        self._token: BearerToken = self.read_access_token()
        self._log = getLogger(__name__)

    @property
    def addr(self) -> str:
        """Get StandCloud service name."""
        return self._addr.domain

    @property
    def api_url(self) -> str:
        """Get StandCloud API URL."""
        return self._addr.api

    def update_token(self, token: BearerToken) -> None:
        """Update access token.

        Args:
            token (BearerToken): access token.
        """
        self._token = token

    def read_access_token(self) -> BearerToken | None:
        """Read access token from token store.

        Returns:
            BearerToken: access token
        """
        try:
            return self._read_token_info()
        except Exception:  # noqa: BLE001
            return None

    def get_verification_url(self) -> dict:
        """Get StandCloud verification URL.

        Returns:
            dict: verification URL
        """
        req = requests.post(
            self._addr.device,
            data={
                "client_id": self._client_id,
                "scope": "offline_access authelia.bearer.authz",
                "audience": self._addr.api,
            },
            verify=self.verify_ssl,
            timeout=10,
        )
        return json.loads(req.content)

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
            resp = api.get(verify=self.verify_ssl)
        except ExpiredAccessToken as exc:
            raise StandCloudError(str(exc)) from exc
        except OAuth2Error as exc:
            raise StandCloudError(exc.description) from exc
        except RequestException as exc:
            raise StandCloudError(exc.strerror) from exc  # type: ignore

        return resp

    def wait_verification(
        self,
        response: dict,
        waiting_time_m: int = 5,
    ) -> BearerToken | None:
        """Wait StandCloud verification.

        Args:
            response (dict): verification response
            waiting_time_m (int): authorization waiting time in minutes

        Returns:
            BearerToken: access token
        """
        interval = response["interval"]
        start_time = datetime.now(tz=timezone.utc)
        device_code = response["device_code"]
        while True:
            sleep(interval)

            req = requests.post(
                self._addr.token,
                data={
                    "client_id": self._client_id,
                    "grant_type": "urn:ietf:params:oauth:grant-type:device_code",
                    "device_code": device_code,
                },
                verify=self.verify_ssl,
                timeout=interval,
            )
            response = json.loads(req.content)

            if "error" in response:
                current_time = datetime.now(tz=timezone.utc)
                if current_time >= start_time + timedelta(minutes=waiting_time_m):
                    return None
                continue

            if "access_token" in response and "refresh_token" in response:
                new_token = BearerToken(**response)

                if "expires_at" not in response and new_token.expires_at:
                    response["expires_at"] = new_token.expires_at.timestamp()
                self._token_manager.save_token_info(response)
                return new_token

    def _get_api(self, endpoint: str) -> ApiClient:
        if self._token is None:
            msg = (
                f"Access token to {self._addr.domain} is not set."
                f"Login to {self._addr.domain} first"
            )
            raise StandCloudError(msg)
        auth = OAuth2(
            sc_addr=self._addr,
            client_id=self._client_id,
            token=self._token,
            token_storer=self._token_manager,
            verify_ssl=self.verify_ssl,
        )
        session = auth.session
        return ApiClient(f"{self._addr.api}/{endpoint}", session=session, timeout=10)

    def _read_token_info(self) -> BearerToken:
        _, mem_keyring = self._token_manager.get_store()
        token_info = mem_keyring.get_password(
            self._token_manager.service_name,
            "access_token",
        )
        secret = self._add_expires_in(json.loads(token_info))  # type: ignore
        return BearerToken(**secret)

    def _add_expires_in(self, secret: dict) -> dict:
        if "expires_at" in secret:
            expires_at = secret["expires_at"]
        elif "id_token" in secret and "exp" in secret["id_token"]:
            expires_at = secret["id_token"]["exp"]
        expires_at_datetime = datetime.fromtimestamp(expires_at, timezone.utc)

        expires_in_datetime = expires_at_datetime - datetime.now(timezone.utc)
        expires_in = int(expires_in_datetime.total_seconds())

        secret["expires_in"] = expires_in

        return secret
