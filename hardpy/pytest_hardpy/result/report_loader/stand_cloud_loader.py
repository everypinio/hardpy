# Copyright (c) 2024 Everypin
# GNU General Public License v3.0 (see LICENSE or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import annotations

import json
from datetime import datetime, timedelta, timezone
from logging import getLogger
from typing import TYPE_CHECKING

from keyring.core import load_keyring
from oauthlib.oauth2.rfc6749.errors import InvalidGrantError, TokenExpiredError
from requests.exceptions import HTTPError
from requests_oauth2client import ApiClient, BearerToken
from requests_oauth2client.tokens import ExpiredAccessToken
from requests_oauthlib import OAuth2Session

if TYPE_CHECKING:
    from keyring.backend import KeyringBackend

    from hardpy.pytest_hardpy.db.schema import ResultRunStore



class StandCloudLoader:
    """StandCloud report generator."""

    def __init__(self, is_debug: bool = False) -> None:
        self._api_url = "https://api.standcloud.localhost/healthcheck"
        self._is_debug = is_debug
        self._is_resp_verify = not is_debug
        self._log = getLogger(__name__)
        self.healthcheck()

    def load(self, report: ResultRunStore) -> int:
        """Load report to the StandCloud.

        Args:
            report (ResultRunStore): report

        Returns:
            int: response status code
        """
        api = self._get_api()
        error_code = 500

        try:
            resp = api.post(verify=self._is_resp_verify, data=report.model_dump())
            self._log.debug(f"Got new content from API: {resp}")
        except ExpiredAccessToken as e:
            self._log.error(
                "API access error: token is expired for ",
                f"{timedelta(seconds = abs(e.args[0].expires_in))}",
            )
            return error_code
        except TokenExpiredError as e:
            self._log.error(f"API access error: {e.description}")
            return error_code
        except InvalidGrantError as e:
            self._log.error(f"Refresh token error: {e.description}")
            return error_code
        except HTTPError as e:
            self._log.error(e)
            return resp.status_code

        return resp.status_code

    def healthcheck(self) -> int:
        """Healthcheck of StandCloud API.

        Returns:
            int: response status code
        """
        api = self._get_api()
        error_code = 500

        try:
            resp = api.get(verify=self._is_resp_verify)
            self._log.debug(f"Got new content from API: {resp}")
        except ExpiredAccessToken as e:
            self._log.error(
                "API access error: token is expired for ",
                f"{timedelta(seconds = abs(e.args[0].expires_in))}",
            )
            return error_code
        except TokenExpiredError as e:
            self._log.error(f"API access error: {e.description}")
            return error_code
        except InvalidGrantError as e:
            self._log.error(f"Refresh token error: {e.description}")
            return error_code
        except HTTPError as e:
            self._log.error(e)
            return resp.status_code

        return resp.status_code

    def _get_keyrings(self) -> tuple[KeyringBackend, KeyringBackend]:
        storage_keyring = load_keyring("keyring.backends.SecretService.Keyring")
        mem_keyring = storage_keyring

        return storage_keyring, mem_keyring

    def _token_update(self, token: BearerToken) -> None:
        storage_keyring, mem_keyring = self._get_keyrings()

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
        _, mem_keyring = self._get_keyrings()

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
        (storage_keyring, _) = self._get_keyrings()

        refresh_token = storage_keyring.get_password("HardPy", "refresh_token")
        self._log.debug("Got refresh token from the storage keyring")
        return refresh_token

    def _get_api(self) -> ApiClient:
        token = self._get_token()
        client_id = "hardpy-report-uploader"

        extra = {
            "client_id": client_id,
            "audience": "https://demo-api.standcloud.localhost",
            "redirect_uri": "http://localhost:8088/oauth2/callback",
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
            ret = session.refresh_token(
                token_url="https://auth.standcloud.localhost/api/oidc/token",  # noqa: S106
                refresh_token=self._get_refresh_token(),
                verify=False,
                **extra,
            )
            self._token_update(ret)  # type: ignore

        return ApiClient(self._api_url, session=session, timeout=10)

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
