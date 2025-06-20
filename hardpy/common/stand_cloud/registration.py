# Copyright (c) 2025 Everypin
# GNU General Public License v3.0 (see LICENSE or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import annotations

from datetime import timedelta
from io import StringIO
from typing import TYPE_CHECKING

from oauthlib.oauth2.rfc6749.errors import (
    InvalidGrantError,
    TokenExpiredError,
)
from qrcode import QRCode
from requests.exceptions import HTTPError
from requests_oauth2client.tokens import ExpiredAccessToken

from hardpy.common.stand_cloud.token_manager import TokenManager

if TYPE_CHECKING:
    from hardpy.common.stand_cloud.connector import StandCloudConnector


def login(sc_connector: StandCloudConnector) -> None:
    """Login HardPy in StandCloud.

    Args:
        sc_connector (StandCloudConnector): StandCloud connector
    """
    token = sc_connector.read_access_token()
    if token is None:
        response = sc_connector.get_verification_url()
        url = response["verification_uri_complete"]
        _print_user_action_request(url)
        token = sc_connector.wait_verification(response)

    sc_connector.update_token(token)

    try:
        sc_connector.healthcheck()
    except ExpiredAccessToken as e:
        time_diff = timedelta(seconds=abs(e.args[0].expires_in))
        print(f"API access error: token is expired for {time_diff}")
    except TokenExpiredError as e:
        print(f"API access error: {e.description}")
    except InvalidGrantError as e:
        print(f"Refresh token error: {e.description}")
    except HTTPError as e:
        print(e)

    print(f"HardPy login to {sc_connector.addr} success")


def logout(addr: str) -> bool:
    """Logout HardPy from StandCloud.

    Args:
        addr (str): StandCloud address

    Returns:
        bool: True if successful else False
    """
    token_manager = TokenManager(addr)
    return token_manager.remove_token()

def _print_user_action_request(url_complete: str) -> None:
    qr = QRCode()
    qr.add_data(url_complete)
    f = StringIO()
    qr.print_ascii(out=f)
    f.seek(0)

    print(f.read())
    print("Scan the QR code or, using a browser on another device, visit:")
    print(url_complete, end="\n\n")
