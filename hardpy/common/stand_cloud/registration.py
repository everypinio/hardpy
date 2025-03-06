# Copyright (c) 2024 Everypin
# GNU General Public License v3.0 (see LICENSE or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import annotations

import base64
import hashlib
import json
import os
import re
import secrets
import socket
import subprocess
import sys
from contextlib import suppress
from platform import system
from time import sleep
from typing import TYPE_CHECKING
from urllib.parse import urlencode

import requests
from keyring import delete_password, get_credential
from keyring.errors import KeyringError
from oauthlib.common import urldecode
from oauthlib.oauth2 import WebApplicationClient
from oauthlib.oauth2.rfc6749.errors import InvalidClientIdError

from hardpy.common.stand_cloud.connector import StandCloudConnector, StandCloudError
from hardpy.common.stand_cloud.token_storage import get_token_store

if TYPE_CHECKING:
    from requests_oauth2client import BearerToken


def login(addr: str) -> None:
    """Login HardPy in StandCloud.

    Args:
        addr (str): StandCloud address
    """
    # OAuth client configuration
    client_id = "hardpy-report-uploader"
    client = WebApplicationClient(client_id)
    try:
        sc_connector = StandCloudConnector(addr=addr)
    except StandCloudError as exc:
        print(str(exc))
        sys.exit(1)

    verify_ssl = not __debug__

    # Auth requests
    port = _reserve_socket_port()
    callback_process = _create_callback_process(port)
    state = secrets.token_urlsafe(16)
    code_verifier = _code_verifier()
    data = _par_data(code_verifier, client_id, port, state, sc_connector.url.api)
    timeout = 10

    # fmt: off
    # pushed authorization response
    try:
        response = json.loads(requests.post(sc_connector.url.par, data=data, verify=verify_ssl, timeout=timeout).content)
    except Exception as e:  # noqa: BLE001
        print(f"Authentication server is unavailable: {e}")
        sys.exit(1)
    url = (sc_connector.url.auth + "?" + urlencode({"client_id": client_id, "request_uri": response["request_uri"]}))

    # OAuth authorization code request
    print(f"\nOpen the provided URL and authorize HardPy to use StandCloud\n\n{url}")

    # use subprocess
    first_line = next(callback_process.stdout)  # type: ignore
    sleep(1)

    # OAuth authorization code grant
    response = json.loads(first_line)
    callback_process.kill()

    _check_incorrect_response(response, state)

    code = response["code"]
    uri = _redirect_uri(port)
    data = client.prepare_request_body(code=code, client_id=client_id, redirect_uri=uri, code_verifier=code_verifier)

    # OAuth access token request
    data = dict(urldecode(data))
    response = requests.post(sc_connector.url.token, data=data, verify=verify_ssl, timeout=timeout)
    # fmt: on

    try:
        # OAuth access token grant
        response = client.parse_request_body_response(response.text)
    except InvalidClientIdError as e:
        print(e)
        sys.exit(1)

    _store_password(client.token)


def logout() -> bool:
    """Logout HardPy from StandCloud.

    Returns:
        bool: True if successful else False
    """
    service_name = "HardPy"

    try:
        while cred := get_credential(service_name, None):
            delete_password(service_name, cred.username)
    except KeyringError:
        return False
    # TODO(xorialexandrov): fix keyring clearing
    # Windows does not clear refresh token by itself
    if system() == "Windows":
        storage_keyring, _ = get_token_store()
        with suppress(KeyringError):
            storage_keyring.delete_password(service_name, "refresh_token")
    return True


def _redirect_uri(port: str) -> str:
    return f"http://127.0.0.1:{port}/oauth2/callback"


def _reserve_socket_port() -> str:
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind(("127.0.0.1", 0))
    port = sock.getsockname()[1]
    sock.close()

    return str(port)


def _code_verifier() -> str:
    code_verifier = base64.urlsafe_b64encode(os.urandom(40)).decode("utf-8")
    return re.sub("[^a-zA-Z0-9]+", "", code_verifier)


def _code_challenge(code_verifier: str) -> str:
    code_challenge = hashlib.sha256(code_verifier.encode("utf-8")).digest()
    code_challenge = base64.urlsafe_b64encode(code_challenge).decode("utf-8")
    return code_challenge.replace("=", "")


def _create_callback_process(port: str) -> subprocess.Popen:
    args = [
        sys.executable,
        "-m",
        "uvicorn",
        "hardpy.common.stand_cloud.oauth_callback:app",
        "--host=127.0.0.1",
        f"--port={port}",
        "--log-level=error",
    ]

    if system() == "Windows":
        env = os.environ.copy()
        env["PYTHONUNBUFFERED"] = "1"

        return subprocess.Popen(  # noqa: S603
            args,
            stdout=subprocess.PIPE,
            bufsize=1,
            universal_newlines=True,
            env=env,
            creationflags=subprocess.CREATE_NEW_PROCESS_GROUP,  # type: ignore
        )
    return subprocess.Popen(  # noqa: S603
        args,
        stdout=subprocess.PIPE,
        bufsize=1,
        universal_newlines=True,
        env=dict(PYTHONUNBUFFERED="1"),  # noqa: C408
    )


def _store_password(token: BearerToken) -> None:
    storage_keyring, mem_keyring = get_token_store()

    storage_keyring.set_password(
        "HardPy",
        "refresh_token",
        token["refresh_token"],
    )
    token_data = {
        "access_token": token["access_token"],
        "expires_at": token["expires_at"],
    }
    try:
        mem_keyring.set_password("HardPy", "access_token", json.dumps(token_data))
    except KeyringError as e:
        print(e)
        return
    print("\nRegistration completed successfully")


def _check_incorrect_response(response: dict, state: str) -> None:
    if response["state"] != state:
        print("Wrong state in response")
        sys.exit(1)

    if "error" in response:
        error = response["error"]
        error_description = response["error_description"]
        print(f"{error}: {error_description}")
        sys.exit(1)


def _par_data(
    code_verifier: str,
    client_id: str,
    port: str,
    state: str,
    api_url: str,
) -> dict:
    """Create pushed authorization request data.

    Returns:
        dict: pushed authorization request data
    """
    # Code Challenge Data
    code_challenge = _code_challenge(code_verifier)

    # pushed authorization request
    return {
        "scope": "authelia.bearer.authz offline_access",
        "response_type": "code",
        "client_id": client_id,
        "redirect_uri": _redirect_uri(port),
        "code_challenge": code_challenge,
        "code_challenge_method": "S256",
        "state": state,
        "audience": api_url,
    }
