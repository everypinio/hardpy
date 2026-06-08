"""Setup module — slow (~2s/case), all-pass. Lets the operator scroll freely."""

import time
import pytest

from hardpy import set_message

pytestmark = pytest.mark.module_name("Setup")


@pytest.mark.case_name("Power on")
def test_setup_power_on():
    time.sleep(2.0)
    set_message("Power supply nominal: 5.00V")


@pytest.mark.case_name("Communication check")
def test_setup_comm():
    time.sleep(2.0)
    set_message("Serial comms established at 115200 baud")


@pytest.mark.case_name("Firmware version")
def test_setup_fw():
    time.sleep(2.0)
    set_message("Firmware: 1.2.3-build.20260512")
