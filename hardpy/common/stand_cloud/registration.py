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
from time import sleep
from typing import TYPE_CHECKING
from urllib.parse import urlencode

import requests
from keyring.errors import KeyringError
from oauthlib.common import urldecode
from oauthlib.oauth2 import WebApplicationClient
from oauthlib.oauth2.rfc6749.errors import InvalidClientIdError

from hardpy.common.stand_cloud.token_storage import get_token_store

if TYPE_CHECKING:
    from requests_oauth2client import BearerToken


def register(ssl_verify: bool, api_addr: str, auth_addr: str) -> None:
    """Register HardPy in StandCloud."""
    # TODO (xorialexandrov): Fix magic numbers
    # OAuth client configuration
    client_id = "hardpy-report-uploader"
    client = WebApplicationClient(client_id)

    # URLs
    authorization_url = f"https://{auth_addr}/api/oidc/authorization"
    par_url = f"https://{auth_addr}/api/oidc/pushed-authorization-request"
    token_url = f"https://{auth_addr}/api/oidc/token"
    api_url = f"https://{api_addr}/"

    # Auth requests
    port = _reserve_socket_port()
    callback_process = _create_callback_process(port)

    state = secrets.token_urlsafe(16)

    # Code Challange Data
    code_verifier = _code_verifier()
    code_challenge = _code_challenge(code_verifier)

    # # pushed authorization request
    data = {
        "scope": "authelia.bearer.authz offline_access",
        "response_type": "code",
        "client_id": client_id,
        "redirect_uri": _redirect_uri(port),
        "code_challenge": code_challenge,
        "code_challenge_method": "S256",
        "state": state,
        "audience": api_url,
    }

    timeout = 10

    # pushed authorization response
    response = json.loads(
        requests.post(par_url, data=data, verify=ssl_verify, timeout=timeout).content,
    )
    url = (
        authorization_url
        + "?"
        + urlencode({"client_id": client_id, "request_uri": response["request_uri"]})
    )

    # OAuth authorization code request
    print(f"\nOpen the provided URL and authorize HardPy to use StandCloud\n{url}\n")

    # use subprocess
    first_line = next(callback_process.stdout)  # type: ignore
    sleep(1)

    # OAuth authorization code grant
    response = json.loads(first_line)
    callback_process.kill()

    _check_incorrect_response(response, state)

    data = client.prepare_request_body(
        code=response["code"],
        client_id=client_id,
        redirect_uri=_redirect_uri(port),
        code_verifier=code_verifier,
    )

    # OAuth access token request
    data = dict(urldecode(data))
    response = requests.post(token_url, data=data, verify=ssl_verify, timeout=timeout)

    try:
        # OAuth access token grant
        response = client.parse_request_body_response(response.text)
    except InvalidClientIdError as e:
        print(e)
        sys.exit(1)

    _store_password(client.token)


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
    print("\nRegistration completed")


def _check_incorrect_response(response: dict, state: str) -> None:
    if response["state"] != state:
        print("Wrong state in response")
        sys.exit(1)

    if "error" in response:
        error = response["error"]
        error_description = response["error_description"]
        print(f"{error}: {error_description}")
        sys.exit(1)
