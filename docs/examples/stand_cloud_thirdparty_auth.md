# StandCloud third party authorization

This documentation describes how to authorize a **HardPy** application on a
**StandCloud** system using the OAuth 2.0 Device Authorization Flow process.

## Authorization process

1. The application requests the device code from the authorization server.
2. The server returns:
    * `device_code`
    * `user_code`
    * `verification_uri` (authorization URL)
    * `verification_uri_complete` (the URL with the pre-filled code)
    * `expires_in` (code lifetime)
    * `interval` (status polling interval)
3. The user follows the link and confirms authorization.
4. The application periodically polls the token server.
5. After confirmation, the server returns an access token and a refresh token.

## Code example

The code samples are in Python, but they use simple constructs that are available in
most programming languages.
To implement the authorization process for a third-party
application in a different language, use the general approach demonstrated in these scripts.
Reading [RFC6749](https://datatracker.ietf.org/doc/html/rfc8628),
which describes the OAuth 2.0 device flow, is also recommended.
The above examples do not display the QR code to the user; rather, they display a link for authorization.

## Authorization example

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


# Device authorization aequest
data = {
    "client_id": CLIENT_ID,
    "scope": "offline_access authelia.bearer.authz",
    "audience": API_URL,
}

req = requests.post(DEVICE_AUTHORIZATION_URL, data=data, verify=SSL_VERIFY, timeout=10)
response = json.loads(req.content)
verification_uri_complete = response["verification_uri_complete"]
interval = response["interval"]

# Token request
if "error" in response:
    error = response["error"]
    error_description = response["error_description"]
    print(f"{error}: {error_description}")
    sys.exit(1)

print(f"\nVerification URI: {verification_uri_complete}")

data = {
    "client_id": CLIENT_ID,
    "grant_type": "urn:ietf:params:oauth:grant-type:device_code",
    "device_code": response["device_code"],
}

# Token response
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

### 1. Introduction

The script facilitates a secure way for devices with limited input capabilities
(like command-line applications) to authenticate with **StandCloud**.
It leverages the OAuth 2.0 Device Flow, which allows a user to authorize a device
by visiting a URL on a separate, input-rich device (e.g., a web browser on a computer or smartphone).

### 2. Key concepts: OAuth 2.0 device authorization grant flow

The OAuth 2.0 Device Authorization Grant Flow is designed for devices that cannot easily
display a browser or accept direct user input (like typing a username and password).
The flow generally involves the following steps:

1. **Device Authorization Request**: The client (this script) requests a device code and a
   verification URI from the authorization server.
2. **User Interaction**: The user takes the verification URI and a user code
    (provided by the authorization server) and enters them into a browser on a
    separate device to authorize the client.
3. **Token Request Polling**: The client repeatedly polls the authorization server's
    token endpoint with the device code until the user completes the authorization.
4. **Token Response**: Once authorized, the client receives access tokens and (optionally) refresh tokens.
5. **API Access**: The client uses the obtained access token to make authenticated calls to the protected API resources.

For a deeper understanding of the OAuth 2.0 Device Authorization Grant, refer to the official specification:
[RFC 8628 - OAuth 2.0 Device Authorization Grant](https://datatracker.ietf.org/doc/html/rfc8628).

### 3. Script breakdown

The script performs the following sequence of operations:

#### 3.1. Configuration

* **`BASE_URL`**: This variable must be changed to your specific **StandCloud** instance URL.
    * **Example**: `https://company_name.standcloud.io`
* **`SSL_VERIFY`**: A boolean flag (`True` by default) indicating whether SSL certificate verification should be performed.
    Set to `False` if your server uses a self-signed certificate.
* **`CLIENT_ID`**: The OAuth client identifier, which is fixed as `hardpy-report-uploader`.
    This identifies the client application to the **StandCloud** authentication system.

#### 3.2. API endpoints

The script defines several critical API endpoints based on the `BASE_URL`:

* **`API_URL`**: The base URL for the **StandCloud** API (`/hardpy/api/v1`).
* **`DEVICE_AUTHORIZATION_URL`**: The endpoint for initiating the device authorization flow (`/auth/api/oidc/device-authorization`).
* **`TOKEN_URL`**: The endpoint for requesting tokens after device authorization (`/auth/api/oidc/token`).

#### 3.3. Device authorization request

The script first makes a `POST` request to the `DEVICE_AUTHORIZATION_URL` with the following parameters:

* **`client_id`**: The `CLIENT_ID` defined above.
* **`scope`**: Defines the permissions requested.
    * `offline_access`: Allows the client to request refresh tokens,
        enabling long-term access without re-authorization.
    * `authelia.bearer.authz`: A specific scope related to Authelia
        (an open-source authentication and authorization server often used with OpenID Connect)
        for bearer token authorization.
* **`audience`**: Specifies the intended recipient of the access token, which is the `API_URL`.

Upon a successful response, the script extracts:

* **`verification_uri_complete`**: The full URL the user needs to visit in their browser to authorize the device.
* **`interval`**: The recommended polling interval (in seconds) for subsequent token requests.
* **`device_code`**: A code representing the authorization request, used in subsequent token polling.

The script then prints the `verification_uri_complete` for the user to access.
It includes basic error handling for the device authorization request.

#### 3.4. Token request (polling)

After initiating the device authorization, the script enters a loop to poll
the `TOKEN_URL` until authorization is granted by the user.
Each `POST` request to the `TOKEN_URL` includes:

* **`client_id`**: The `CLIENT_ID`.
* **`grant_type`**: Set to `"urn:ietf:params:oauth:grant-type:device_code"`, indicating the Device Flow grant type.
* **`device_code`**: The `device_code` obtained from the initial device authorization request.

The script pauses for the `interval` period between each poll.
Once the `access_token` is present in the response, the polling loop breaks, and the script proceeds.

#### 3.5. Test API call

Finally, the script demonstrates how to use the obtained `access_token` to make an authenticated API call.

* An `Authorization` header is constructed with the format `"Bearer <access_token>"`.
* A `GET` request is made to the `API_URL` + `/healthcheck` endpoint.
    This is a simple endpoint to verify successful authentication and authorization.

If the API call returns a `200 OK` status, it confirms that the OAuth authentication and
authorization process was successful, and the client can now access protected resources.
Any other status code indicates an issue, and the response text is printed for debugging.

### 4. Replicating in other languages

To implement this authentication flow in a different programming language, you will need to:

1. **HTTP Client Library**: Use an HTTP client library available in your chosen language
    (e.g., `requests` for Python, `HttpClient` for C#, `fetch` for JavaScript, `OkHttp` for Java, `net/http` for Go).
2. **JSON Parsing**: Implement JSON parsing to handle the responses from the authorization and token endpoints.
3. **URL Construction**: Construct the `DEVICE_AUTHORIZATION_URL`, `TOKEN_URL`, and `API_URL`
    correctly based on your **StandCloud** instance.
4. **Request Parameters**: Ensure that the `client_id`, `scope`, `audience`, `grant_type`,
    and `device_code` parameters are correctly included in your `POST` request bodies, typically as form-urlencoded data.
5. **Polling Logic**: Implement a polling mechanism with appropriate delays to wait for user authorization.
6. **Bearer Token**: Correctly format the `Authorization: Bearer <access_token>` header for protected API calls.

## Authorization example with token update

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

### 1. Script breakdown

This script extends the previous basic authentication by adding functions for token management.

#### 1.1. Configuration and endpoints

Most configurations are similar to the previous script:

* **`BASE_URL`**: **StandCloud** instance URL.
* **`SSL_VERIFY`**: For SSL certificate validation.
* **`CLIENT_ID`**: Fixed as `"hardpy-report-uploader"`.
* **`API_URL`**: Base URL for API calls.
* **`DEVICE_AUTHORIZATION_URL`**: Endpoint for initiating device flow.
* **`TOKEN_URL`**: Endpoint for token requests (both initial and refresh).
* **`HEALTHCHECK_URL`**: A specific endpoint used to test API access.
* **`TOKEN_FILE`**: A `Path` object pointing to `token_info.json` in the same
    directory as the script. This file is used to store token information for persistence.
    **(Remember the security warning regarding file storage)**.

#### 1.2. `authenticate()` function

This function encapsulates the **initial OAuth 2.0 Device Authorization Grant Flow**,
identical to the previous script's main logic.

1. It initiates a `POST` request to `DEVICE_AUTHORIZATION_URL` with `client_id`,
    `scope` (`offline_access` is crucial here for getting a refresh token), and `audience`.
2. It handles the user interaction step, printing the `verification_uri_complete`.
3. It polls the `TOKEN_URL` using the `device_code` until an `access_token`
    (and importantly, a `refresh_token`) is received.
4. It calculates the `expires_at` timestamp based on `expires_in` and the current time,
    then returns a dictionary (`token_info`) containing `access_token`, `refresh_token`, and `expires_at`.

#### 1.3. `refresh_tokens()` function

This new function handles the **refresh token grant type**.

1. It constructs a `POST` request to the `TOKEN_URL` with:
    * **`client_id`**: Your client identifier.
    * **`grant_type`**: Set to `"refresh_token"`.
    * **`refresh_token`**: The `refresh_token_value` obtained from a previous authentication or refresh.
2. Upon a successful response, it extracts the `access_token` and its new `expires_at` timestamp.
3. Crucially, it checks if a *new* `refresh_token` is provided in the response.
    If so, it updates the stored refresh token. Some authorization servers issue new
    refresh tokens with each refresh; others do not.
    Best practice is to use the newest one if provided.
4. It returns the `token_info` dictionary.
    If the refresh fails, it prints an error and returns `None`.

#### 1.4. `healthcheck()` function

This helper function tests the validity of an `access_token` by making a `GET` request to the `HEALTHCHECK_URL`.

1. It sets the `Authorization` header with the `Bearer` token.
2. It returns `True` if the response status is `200 OK`,
    indicating successful API access, and `False` otherwise.

#### 1.5. `save_token_info()` and `load_token_info()` functions

These functions handle the **persistence of token information** to and from a local JSON file (`token_info.json`).

* **`save_token_info`**: Writes the `token_info` dictionary to the `TOKEN_FILE`.
* **`load_token_info`**: Reads the `token_info` from the `TOKEN_FILE`.
    It includes error handling for `FileNotFoundError` or `json.JSONDecodeError`
    if the file doesn't exist or is corrupted, returning `None` in such cases.

#### 1.6. `main()`

This function orchestrates the script's logic.

1. **Load Existing Tokens**: It first attempts to `load_token_info()` from the file.
2. **Initial Authentication**: If no valid tokens are found (file doesn't exist,
    is corrupted, or essential keys are missing), it calls `authenticate()`
    to start a new device flow, then `save_token_info()` and performs a `healthcheck`.
3. **Check Token Expiration**: If tokens are loaded, it checks if the `access_token`
    is still valid (with a 10-second buffer before actual expiration).
      * If valid, it performs a `healthcheck` directly.
4. **Token Refresh**: If the `access_token` has expired or is about to expire,
    it calls `refresh_tokens()` using the stored `refresh_token`.
       * If the refresh is successful, it updates the `token_info`
       (preserving the refresh token if a new one wasn't issued), `save_token_info()`, and performs a `healthcheck`.
       * If the refresh fails (e.g., refresh token is revoked or expired),
       it falls back to starting a new full `authenticate()` flow.

### 2. Replicating in other languages

To implement this robust authentication and token refresh logic in another programming language, you'll need to:

1. **HTTP Client**: Utilize your language's HTTP client for making `POST` and `GET` requests.
2. **JSON Handling**: Parse JSON responses for token information and API results.
3. **Time Management**: Accurately calculate token expiration times using timestamps.
4. **Token Storage**: Implement a **secure** method to store `access_token` and especially
    `refresh_token` between application runs. Avoid plain text files in production. Consider:
    * Environment variables (for secrets, typically during deployment).
    * Operating system's credential manager (e.g., macOS Keychain, Windows Credential Manager).
    * Encrypted database or file storage.
    * Secure vaults (e.g., HashiCorp Vault, AWS Secrets Manager).
5. **Flow Logic**:
    * **Initial Authentication**: Implement the Device Flow as described in the previous documentation.
    * **Token Expiration Check**: Before making an API call, always check if the access token is near expiration.
    * **Token Refresh Logic**: If expired, make a `POST` request to the `TOKEN_URL` with `grant_type=refresh_token` and the `refresh_token`.
    * **Fallback to Re-authentication**: If the refresh token fails, initiate the full Device Flow again.
6. **Error Handling**: Implement robust error handling for network issues,
    invalid responses, and authentication failures at each step.
