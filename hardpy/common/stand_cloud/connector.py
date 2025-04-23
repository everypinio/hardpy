# Copyright (c) 2024 Everypin
# GNU General Public License v3.0 (see LICENSE or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import annotations

import json
from datetime import datetime, timedelta, timezone
from enum import Enum
from logging import getLogger
from typing import TYPE_CHECKING, NamedTuple

from oauthlib.oauth2.rfc6749.errors import OAuth2Error
from requests.exceptions import RequestException
from requests_oauth2client import ApiClient, BearerToken
from requests_oauth2client.tokens import ExpiredAccessToken
from requests_oauthlib import OAuth2Session

from hardpy.common.stand_cloud.exception import StandCloudError
from hardpy.common.stand_cloud.token_storage import get_token_store

if TYPE_CHECKING:
    from requests import Response


class StandCloudURL(NamedTuple):
    """URL.

    api: API address
    token: token address
    par: pushed-authorization-request address
    auth: auth address
    """

    api: str
    token: str
    par: str
    auth: str


class StandCloudAPIMode(str, Enum):
    """StandCloud API mode.

    HARDPY for test stand, integration for third-party service.
    """

    HARDPY = "hardpy"
    INTEGRATION = "integration"


class StandCloudConnector:
    """StandCloud API connector."""

    def __init__(
        self,
        addr: str,
        api_mode: StandCloudAPIMode = StandCloudAPIMode.HARDPY,
        api_version: int = 1,
    ) -> None:
        """Create StandCLoud loader.

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

        self._url: StandCloudURL = StandCloudURL(
            api=https_prefix + addr + f"/{api_mode.value}/api/v{api_version}",
            token=https_prefix + auth_addr + "/api/oidc/token",
            par=https_prefix + auth_addr + "/api/oidc/pushed-authorization-request",
            auth=https_prefix + auth_addr + "/api/oidc/authorization",
        )

        self._verify_ssl = not __debug__
        self._log = getLogger(__name__)

    @property
    def url(self) -> StandCloudURL:
        """Get StandCloud URL."""
        return self._url

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
        except OAuth2Error as exc:
            raise StandCloudError(exc.description) from exc
        except RequestException as exc:
            raise StandCloudError(exc.strerror) from exc # type: ignore

        return resp

    def _token_update(self, token: BearerToken) -> None:
        storage_keyring, mem_keyring = get_token_store()

        _access_token = "access_token"  # noqa: S105
        _expires_at = "expires_at"
        _refresh_token = "refresh_token"  # noqa: S105
        _hardpy = "HardPy"

        storage_keyring.set_password(_hardpy, _refresh_token, token[_refresh_token])
        mem_keyring.set_password(_hardpy, _access_token, token[_access_token])

        token_data = {
            _access_token: token[_access_token],
            _expires_at: token[_expires_at],
        }

        mem_keyring.set_password(_hardpy, _access_token, json.dumps(token_data))

    def _get_expires_in(self, expires_at: float | None) -> int:
        if expires_at is None:
            return -1
        expires_at_datetime = datetime.fromtimestamp(expires_at, timezone.utc)

        now_datetime = datetime.now(timezone.utc)

        expires_in_datetime = expires_at_datetime - now_datetime
        return int(expires_in_datetime.total_seconds())

    def _get_access_token_info(self) -> tuple[str | None, float | None]:
        _, mem_keyring = get_token_store()

        _access_token = "access_token"  # noqa: S105
        _expires_at = "expires_at"

        token_info = mem_keyring.get_password("HardPy", _access_token)
        if token_info is None:
            return None, None
        token_dict = json.loads(token_info)
        access_token = token_dict[_access_token]
        expired_at = token_dict[_expires_at]

        return access_token, expired_at

    def _get_refresh_token(self) -> str | None:
        (storage_keyring, _) = get_token_store()

        refresh_token = storage_keyring.get_password("HardPy", "refresh_token")
        self._log.debug("Got refresh token from the storage keyring")
        return refresh_token

    def _get_api(self, endpoint: str) -> ApiClient:
        token = self._get_token()
        client_id = "hardpy-report-uploader"

        extra = {
            "client_id": client_id,
            "audience": self._url.api,
            "redirect_uri": "http://localhost/oauth2/callback",
        }

        session = OAuth2Session(
            client_id,
            token=token.as_dict(),
            token_updater=self._token_update,
        )

        is_need_refresh = False
        early_refresh = timedelta(seconds=30)

        if token.expires_in and token.expires_in < early_refresh.seconds:
            is_need_refresh = True

        if token.access_token is None:
            self._log.debug("Want to refresh token since don't have access token")
            is_need_refresh = True

        if is_need_refresh:
            try:
                ret = session.refresh_token(
                    token_url=self._url.token,
                    refresh_token=self._get_refresh_token(),
                    verify=False,
                    **extra,
                )
            except OAuth2Error as exc:
                raise StandCloudError(exc.description) from exc
            except RequestException as exc:
                raise StandCloudError(exc.strerror) from exc  # type: ignore
            self._token_update(ret)  # type: ignore

        return ApiClient(self._url.api + "/" + endpoint, session=session, timeout=10)

    def _get_token(self) -> BearerToken:
        access_token, expires_at = self._get_access_token_info()
        expires_in = self._get_expires_in(expires_at)

        return BearerToken(
            scope=["authelia.bearer.authz", "offline_access"],
            token_type="bearer",  # noqa: S106
            access_token=access_token,
            expires_at=expires_at,
            expires_in=expires_in,
        )
