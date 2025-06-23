# Copyright (c) 2025 Everypin
# GNU General Public License v3.0 (see LICENSE or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import annotations

from datetime import timedelta
from typing import TYPE_CHECKING

from requests.auth import AuthBase
from requests_oauth2client import BearerToken
from requests_oauthlib import OAuth2Session

if TYPE_CHECKING:
    from requests import PreparedRequest
    from requests_oauth2client import ApiClient

    from hardpy.common.stand_cloud.token_manager import TokenManager
    from hardpy.common.stand_cloud.utils import StandCloudAddr


class OAuth2(AuthBase):
    """Authorize HardPy using the device flow of OAuth 2.0."""

    def __init__(
        self,
        sc_addr: StandCloudAddr,
        client_id: str,
        token: BearerToken,
        token_manager: TokenManager,
        verify_ssl: bool = True,
    ) -> None:
        self._sc_addr = sc_addr
        self._client_id = client_id
        self._verify_ssl = verify_ssl
        self._token_manager = token_manager

        self._token = self._check_token(token)

    def __call__(self, req: PreparedRequest) -> PreparedRequest:
        """Append an OAuth 2 token to the request.

        Note that currently HTTPS is required for all requests. There may be
        a token type that allows for plain HTTP in the future and then this
        should be updated to allow plain HTTP on a white list basis.
        """
        req.headers[self._token.AUTHORIZATION_HEADER] = (  # type: ignore
            self._token.authorization_header()
        )
        return req

    def _check_token(self, token: BearerToken) -> ApiClient:
        """Check token in OAuth2 session and refresh it if needed.

        Args:
            token (BearerToken): bearer token to check

        Returns:
            ApiClient: refreshed token
        """
        refresh_url = self._sc_addr.token

        self.session = OAuth2Session(
            client_id=self._client_id,
            token=token.as_dict(),
            token_updater=self._token_manager.save_token_info,
        )

        is_need_refresh = False
        early_refresh = timedelta(seconds=60)

        if token.expires_in and token.expires_in < early_refresh.seconds:
            is_need_refresh = True
        if token.access_token is None:
            is_need_refresh = True

        if is_need_refresh:
            extra = {"client_id": self._client_id, "audience": self._sc_addr.api}
            ret = self.session.refresh_token(
                token_url=refresh_url,
                refresh_token=self._token_manager.read_refresh_token(),
                verify=self._verify_ssl,
                **extra,
            )

            self._token_manager.save_token_info(ret)
            return BearerToken(**ret)

        return token
