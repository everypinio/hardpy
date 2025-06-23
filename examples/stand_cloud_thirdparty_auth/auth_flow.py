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
