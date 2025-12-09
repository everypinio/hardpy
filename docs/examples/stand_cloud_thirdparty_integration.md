# StandCloud third party integration

This documentation explains how to use the StandCloud integration service via an API key.
Information on integration options with StandCloud can be found at 
https://standcloud.io/integration/api/v1/docs.

## Code example

The code samples are in Python, but they use simple constructs that are available in
most programming languages.

## Integration example

**integration_flow.py** is an example of a simple integration script written in Python.
The script requires the installation of the `requests` package.
The only thing that needs to be changed to make it work is the
**API key** in the `API_KEY` variable.
This script first checks access to the integration service, 
and then requests a list of completed test runs by sending a request to `test_run`.


```python
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
```
