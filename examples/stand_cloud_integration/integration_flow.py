import sys

import requests

SSL_VERIFY = True

########################################
# Change API_KEY to your api key
API_KEY = "your_api_key"
########################################

HEALTHCHECK_URL = "https://standcloud.io/integration/api/v1/healthcheck"
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

USER_INFO_URL = "https://standcloud.io/integration/api/v1/test_run"
response = requests.get(USER_INFO_URL, headers=header, verify=SSL_VERIFY)

if response.status_code != 200:
    print(response.text)
    sys.exit(1)
print("\nTest run list: ", response.text)
