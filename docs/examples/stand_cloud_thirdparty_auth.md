# StandCloud third party authorization

This documentation describes how to authorize a **HardPy** application on a
**StandCloud** system using the OAuth 2.0 Device Authorization Flow process.

## Authorization process

1. The application requests the device code from the authorization server.
2. The server returns:
    * `device_code`
    * `user_code`
    * `verification_uri` (authorization URL)
    * `verification_uri_complete` (the URL with the pre-filled code).
    * `expires_in` (code lifetime)
    * `interval` (status polling interval)
3. The user follows the link and confirms authorization.
4. The application periodically polls the token server.
5. After confirmation, the server returns an access token and a refresh token.

## Code example

The code samples are in Python, but they use simple constructs that are available in
most programming languages. To implement the authorization process for a third-party
application in a different language, use the general approach demonstrated in these scripts.
Reading [RFC6749](https://datatracker.ietf.org/doc/html/rfc8628),
which describes the OAuth 2.0 device flow, is also recommended.
The above examples do not display the QR code to the user; rather, they display a link for authorization.

### Authorization example

**auth_flow.py** is an example of a simple authorization script written in Python.
The script requires the installation of the `requests` package.
The only thing that needs to be changed to make it work is the
**StandCloud** address in the `BASE_URL` variable.

```python
# This script demonstrates the StandCloud authentication process.
# Change the URL to your StandCloud address, nothing else needs to be changed.

import json
import sys
import time

import requests

########################################
# Change URL to your StandCloud address
BASE_URL = "https://demo.standcloud.io"
########################################

# Confugirable parameters, False if the server is self-signed
SSL_VERIFY = True

# OAuth client configuration
# client_id must be "hardpy-report-uploader"
CLIENT_ID = "hardpy-report-uploader"

# API endpoints
API_URL = BASE_URL + "/hardpy/api/v1"
DEVICE_AUTHORIZATION_URL = BASE_URL + "/auth/api/oidc/device-authorization"
TOKEN_URL = BASE_URL + "/auth/api/oidc/token"


# Device Authorization Request
data = {
    "client_id": CLIENT_ID,
    "scope": "offline_access authelia.bearer.authz",
    "audience": API_URL,
}

req = requests.post(DEVICE_AUTHORIZATION_URL, data=data, verify=SSL_VERIFY, timeout=10)
response = json.loads(req.content)
verification_uri_complete = response["verification_uri_complete"]
interval = response["interval"]

# Token Request
if "error" in response:
    error = response["error"]
    error_description = response["error_description"]
    print(f"{error}: {error_description}")
    sys.exit(1)

print(f"\nVerification URI: {verification_uri_complete}")

# Token request
data = {
    "client_id": CLIENT_ID,
    "grant_type": "urn:ietf:params:oauth:grant-type:device_code",
    "device_code": response["device_code"],
}

# Token Response
while True:
    req = requests.post(TOKEN_URL, data=data, verify=SSL_VERIFY, timeout=10)
    response = json.loads(req.content)
    print(".", end="")
    if "access_token" in response:
        print("\nToken info:", response)
        break
    time.sleep(interval)

# Test API call
header = {
    "Authorization": "Bearer {}".format(response["access_token"]),
    "Content-type": "application/json",
    "Accept": "text/plain",
}
print("\nheader: ", header)

USER_INFO_URL = API_URL + "/healthcheck"
response = requests.get(USER_INFO_URL, headers=header, verify=SSL_VERIFY, timeout=10)

if response.status_code != 200:
    print(response.text)
    sys.exit(1)
print("\nOAuth Authenticated and Authorized API access")
```

### Authorization example with token update

**token_update.py** is a more complex version of the **auth_flow.py** script,
which rotates access and refresh tokens.
This script stores these tokens in a file.
However, this simplified token storage model should not be used in a production
environment for security reasons.
The only thing that needs to be changed to make it work is the
**StandCloud** address in the `BASE_URL` variable.

```python
# This script demonstrates the StandCloud authentication process with
# token updating. Don't use the save as file option, it's insecure.
# Change the URL to your StandCloud address, nothing else needs to be changed.

import json
import sys
import time
from pathlib import Path

import requests

########################################
# Change URL to your StandCloud address
BASE_URL = "https://demo.standcloud.io"
########################################

# Configurable parameters, False if the server is self-signed
SSL_VERIFY = True

# OAuth client configuration
# client_id must be "hardpy-report-uploader"
CLIENT_ID = "hardpy-report-uploader"

# API endpoints
API_URL = BASE_URL + "/hardpy/api/v1"
DEVICE_AUTHORIZATION_URL = BASE_URL + "/auth/api/oidc/device-authorization"
TOKEN_URL = BASE_URL + "/auth/api/oidc/token"
HEALTHCHECK_URL = API_URL + "/healthcheck"
TOKEN_FILE = Path(__file__).parent / "token_info.json"


def authenticate():
    data = {
        "client_id": CLIENT_ID,
        "scope": "offline_access authelia.bearer.authz",
        "audience": API_URL,
    }

    req = requests.post(
        DEVICE_AUTHORIZATION_URL, data=data, verify=SSL_VERIFY, timeout=10
    )
    response = req.json()

    if "error" in response:
        error = response["error"]
        error_description = response["error_description"]
        print(f"{error}: {error_description}")
        sys.exit(1)

    verification_uri_complete = response["verification_uri_complete"]
    interval = response["interval"]

    print(f"\nVerification URI: {verification_uri_complete}")

    data = {
        "client_id": CLIENT_ID,
        "grant_type": "urn:ietf:params:oauth:grant-type:device_code",
        "device_code": response["device_code"],
    }

    while True:
        req = requests.post(TOKEN_URL, data=data, verify=SSL_VERIFY, timeout=10)
        response = req.json()
        if "access_token" in response:
            print("\nAuthentication successful")
            break
        time.sleep(interval)

    # Calculate expiration time
    expires_at = time.time() + response["expires_in"]
    token_info = {
        "access_token": response["access_token"],
        "refresh_token": response["refresh_token"],
        "expires_at": expires_at,
    }
    return token_info


def refresh_tokens(refresh_token_value):
    data = {
        "client_id": CLIENT_ID,
        "grant_type": "refresh_token",
        "refresh_token": refresh_token_value,
    }

    try:
        req = requests.post(TOKEN_URL, data=data, verify=SSL_VERIFY, timeout=10)
        response = req.json()

        if "access_token" not in response:
            print(
                "Token refresh failed. Error:", response.get("error", "unknown error")
            )
            return None

        expires_at = time.time() + response["expires_in"]
        token_info = {
            "access_token": response["access_token"],
            "expires_at": expires_at,
        }

        # Update refresh token if new one is provided
        if "refresh_token" in response:
            token_info["refresh_token"] = response["refresh_token"]
            print("Access and refresh tokens updated")
        else:
            print("Access token updated")

        return token_info

    except Exception as e:
        print("Token refresh failed:", str(e))
        return None


def healthcheck(access_token):
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-type": "application/json",
        "Accept": "text/plain",
    }

    try:
        response = requests.get(
            HEALTHCHECK_URL, headers=headers, verify=SSL_VERIFY, timeout=10
        )
        if response.status_code == 200:
            print("Healthcheck successful")
            return True
        print(f"Healthcheck failed: HTTP {response.status_code}")
        return False
    except Exception as e:
        print("Healthcheck error:", str(e))
        return False


def save_token_info(token_info):
    with Path.open(TOKEN_FILE, "w") as f:
        json.dump(token_info, f, indent=4)


def load_token_info():
    try:
        with Path.open(TOKEN_FILE, "r") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return None


def main():
    token_info = load_token_info()

    # If no tokens exist or file is corrupted
    if (
        not token_info
        or "access_token" not in token_info
        or "refresh_token" not in token_info
    ):
        print("No valid tokens found. Starting authentication...")
        token_info = authenticate()
        save_token_info(token_info)
        healthcheck(token_info["access_token"])
        return

    # Check access token expiration with 10-second buffer
    current_time = time.time()
    if current_time < token_info["expires_at"] - 10:
        print("Access token is valid")
        healthcheck(token_info["access_token"])
        return

    print("Access token expired. Refreshing tokens...")
    new_token_info = refresh_tokens(token_info["refresh_token"])

    if new_token_info:
        # Preserve existing refresh token if not updated
        if "refresh_token" not in new_token_info:
            new_token_info["refresh_token"] = token_info["refresh_token"]

        save_token_info(new_token_info)
        healthcheck(new_token_info["access_token"])
    else:
        print("Refresh token invalid. Starting re-authentication...")
        token_info = authenticate()
        save_token_info(token_info)
        healthcheck(token_info["access_token"])


if __name__ == "__main__":
    main()
```
