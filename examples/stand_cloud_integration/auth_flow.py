import sys

import requests

########################################
# Change API_KEY to your api key
API_KEY = "your_api_key"
########################################

SSL_VERIFY = True
BASE_URL = "https://standcloud.io"
API_URL = BASE_URL + "/integration/api/v1"  # API endpoints

HEALTHCHECK_URL = API_URL + "/healthcheck"
response = requests.get(HEALTHCHECK_URL, verify=SSL_VERIFY)

if response.status_code != 200:
    print(response.text)
    sys.exit(1)
print("StandCloud is up and running")

# Test API call
header = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-type": "application/json",
    "Accept": "text/plain",
}
print("\nheader: ", header)

USER_INFO_URL = API_URL + "/test_run"
response = requests.get(USER_INFO_URL, headers=header, verify=SSL_VERIFY)

if response.status_code != 200:
    print(response.text)
    sys.exit(1)
print("\nTest run list: ", response.text)
