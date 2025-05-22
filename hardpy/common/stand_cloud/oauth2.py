# Copyright (c) 2025 Everypin
# GNU General Public License v3.0 (see LICENSE or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import annotations

import io
import json
import sys
from copy import deepcopy
from datetime import datetime, timedelta, timezone
from time import sleep
from typing import TYPE_CHECKING, Final

import qrcode
import requests
from keyring.errors import KeyringError
from requests.auth import AuthBase
from requests_oauth2client import BearerToken
from requests_oauthlib import OAuth2Session

from hardpy.common.stand_cloud.token_storage import get_token_store

if TYPE_CHECKING:
    from requests_oauth2client import ApiClient

    from hardpy.common.stand_cloud.connector import StandCloudConnector

SERVICE_NAME: Final = "HardPy"


class OAuth2(AuthBase):
    """Authorize HardPy using the device flow of OAuth 2.0."""

    def __init__(self, sc_connector: StandCloudConnector):
        self._sc_connector = sc_connector

        try:
            token = self._read_token_info()
        except Exception:  # noqa: BLE001
            token = self._get_new_token()

        self.token = self._check_token(token)

    def __call__(self, req: requests.PreparedRequest) -> requests.PreparedRequest:
        """Append an OAuth 2 token to the request.

        Note that currently HTTPS is required for all requests. There may be
        a token type that allows for plain HTTP in the future and then this
        should be updated to allow plain HTTP on a white list basis.
        """
        req.headers[self.token.AUTHORIZATION_HEADER] = self.token.authorization_header()  # type: ignore
        return req

    def _check_token(self, token: BearerToken) -> ApiClient:
        refresh_url = self._sc_connector.url.token

        session = OAuth2Session(
            self._sc_connector.client_id,
            token=token.as_dict(),
            token_updater=self._save_token_info,
        )

        is_need_refresh = False
        early_refresh = timedelta(seconds=30)

        if token.expires_in and token.expires_in < early_refresh.seconds:
            is_need_refresh = True
        if token.access_token is None:
            is_need_refresh = True

        if is_need_refresh:
            extra = {
                "client_id": self._sc_connector.client_id,
                "audience": self._sc_connector.url.api,
            }
            ret = session.refresh_token(
                token_url=refresh_url,
                refresh_token=self._get_refresh_token(),
                verify=False,
                **extra,
            )
            self._save_token_info(ret)
            return BearerToken(**ret)

        return token

    def _get_new_token(self) -> BearerToken:
        req = requests.post(
            self._sc_connector.url.device,
            data={
                "client_id": self._sc_connector.client_id,
                "scope": "offline_access authelia.bearer.authz",
                "audience": self._sc_connector.url.api,
            },
            verify=self._sc_connector.verify_ssl,
            timeout=10,
        )
        response = json.loads(req.content)
        self._print_user_action_request(response["verification_uri_complete"])

        interval = response["interval"]
        data = {
            "client_id": self._sc_connector.client_id,
            "grant_type": "urn:ietf:params:oauth:grant-type:device_code",
            "device_code": response["device_code"],
        }
        return self._wait_verification(auth_info=data, interval=interval)

    def _wait_verification(self, auth_info: dict, interval: int) -> BearerToken:
        start_time = datetime.now(tz=timezone.utc)
        while True:
            print(".", end="")
            sleep(interval)

            req = requests.post(
                self._sc_connector.url.token,
                data=auth_info,
                verify=self._sc_connector.verify_ssl,
                timeout=interval,
            )
            response = json.loads(req.content)

            if "error" in response:
                current_time = datetime.now(tz=timezone.utc)
                if current_time >= start_time + timedelta(minutes=3):
                    print("Verification time is out")
                    sys.exit(1)
                continue

            if "access_token" in response and "refresh_token" in response:
                print("Token received")
                new_token = BearerToken(**response)

                if "expires_at" not in response and new_token.expires_at:
                    response["expires_at"] = new_token.expires_at.timestamp()
                self._save_token_info(response)
                return new_token

    def _print_user_action_request(self, url_complete: str) -> None:
        qr = qrcode.QRCode()
        qr.add_data(url_complete)
        f = io.StringIO()
        qr.print_ascii(out=f)
        f.seek(0)

        print(f.read())
        print("Scan the QR code or, using a browser on another device, visit:")
        print(url_complete, end="\n\n")

    def _save_token_info(self, token: BearerToken | dict) -> None:
        storage_keyring, mem_keyring = get_token_store()
        storage_keyring.set_password(
            SERVICE_NAME,
            "refresh_token",
            token["refresh_token"],
        )

        token_info = deepcopy(token)
        token_info.pop("expires_in")
        token_info.pop("refresh_token")

        try:
            mem_keyring.set_password(
                SERVICE_NAME,
                "access_token",
                json.dumps(token_info),
            )
        except KeyringError as e:
            print(e)
            sys.exit(1)

    def _get_refresh_token(self) -> str | None:
        storage_keyring, _ = get_token_store()
        return storage_keyring.get_password(SERVICE_NAME, "refresh_token")

    def _read_token_info(self) -> BearerToken:
        _, mem_keyring = get_token_store()
        token_info = mem_keyring.get_password(SERVICE_NAME, "access_token")
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
