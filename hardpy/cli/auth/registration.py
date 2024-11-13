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
from urllib.parse import urlencode

import requests
from keyring.core import load_keyring
from oauthlib.common import urldecode
from oauthlib.oauth2 import WebApplicationClient
from oauthlib.oauth2.rfc6749.errors import InvalidClientIdError


def register(ssl_verify: bool):
    """Register HardPy in StandCloud."""
    # OAuth client configuration

    client_id = "hardpy-report-uploader"
    client = WebApplicationClient(client_id)

    # URLs

    authorization_url = "https://auth.standcloud.localhost/api/oidc/authorization"
    par_url = "https://auth.standcloud.localhost/api/oidc/pushed-authorization-request"
    token_url = "https://auth.standcloud.localhost/api/oidc/token"
    demo_api_url = "https://demo-api.standcloud.localhost"

    # Code Challange Data

    code_verifier = base64.urlsafe_b64encode(os.urandom(40)).decode("utf-8")
    code_verifier = re.sub("[^a-zA-Z0-9]+", "", code_verifier)

    code_challenge = hashlib.sha256(code_verifier.encode("utf-8")).digest()
    code_challenge = base64.urlsafe_b64encode(code_challenge).decode("utf-8")
    code_challenge = code_challenge.replace("=", "")

    # Auth requests

    response = ""
    port = _reserve_socket_port()

    args = [
        sys.executable,
        "-m",
        "uvicorn",
        "hardpy.cli.auth.oauth_callback:app",
        "--host=127.0.0.1",
        f"--port={port}",
        "--log-level=error",
    ]

    callback_process = subprocess.Popen(
        args,
        stdout=subprocess.PIPE,
        bufsize=1,
        universal_newlines=True,
        env=dict(PYTHONUNBUFFERED="1"),
    )

    state = secrets.token_urlsafe(16)

    # pushed authorization request
    data = {
        "scope": "authelia.bearer.authz offline_access",
        "response_type": "code",
        "client_id": client_id,
        "redirect_uri": _redirect_uri(port),
        "code_challenge": code_challenge,
        "code_challenge_method": "S256",
        "state": state,
        "audience": demo_api_url,
    }

    # pushed authorization response
    response = json.loads(
        requests.post(
            par_url,
            data=data,
            verify=False,
        ).content
    )

    url = (
        authorization_url
        + "?"
        + urlencode({"client_id": client_id, "request_uri": response["request_uri"]})
    )

    # OAuth authorization code request
    print("\nOpen the provided URL and authorize HardPy to use StandCloud")
    print(f"{url}\n")

    # use subprocess
    first_line = next(callback_process.stdout)
    sleep(1)

    # OAuth authorization code grant
    response = json.loads(first_line)
    callback_process.kill()

    if response["state"] != state:
        print("Wrong state in response")
        sys.exit(1)

    if "error" in response:
        error = response["error"]
        error_description = response["error_description"]
        print(f"{error}: {error_description}")
        sys.exit(1)

    data = client.prepare_request_body(
        code=response["code"],
        client_id=client_id,
        redirect_uri=_redirect_uri(port),
        code_verifier=code_verifier,
    )

    # OAuth access token request
    data = dict(urldecode(data))
    response = requests.post(token_url, data=data, verify=ssl_verify)

    try:
        # OAuth access token grant
        response = client.parse_request_body_response(response.text)
    except InvalidClientIdError as e:
        print(e)
        sys.exit(1)

    with open("token_info.json", "w", encoding="utf-8") as f:  # noqa: PTH123
        storage_keyring = load_keyring("keyring.backends.SecretService.Keyring")
        mem_keyring = storage_keyring

        storage_keyring.set_password(
            "HardPy",
            "refresh_token",
            client.token["refresh_token"],
        )
        mem_keyring.set_password("HardPy", "access_token", client.token["access_token"])

        token = client.token
        token.pop("expires_in")
        token.pop("access_token")
        token.pop("refresh_token")
        json.dump(token, f, ensure_ascii=False, indent=4)

    print()
    print("Registration completed")


def _redirect_uri(port: str) -> str:
    return f"http://127.0.0.1:{port}/oauth2/callback"


def _reserve_socket_port() -> str:
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind(("127.0.0.1", 0))
    port = sock.getsockname()[1]
    sock.close()

    return str(port)
