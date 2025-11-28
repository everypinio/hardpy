import pytest
import hardpy
import datetime
from uuid import uuid4
import time

pytestmark = pytest.mark.module_name("Production Test - Device Commissioning")


@pytest.mark.case_name("Device Serial Number Registration")
def test_serial_number_registration():
    serial_number = str(uuid4())[:6]
    hardpy.set_dut_serial_number(serial_number)
    hardpy.set_message(f"Device serial number registered: {serial_number}")


@pytest.mark.case_name("System Time Synchronization Check")
def test_time_synchronization():
    for _ in range(10):
        current_time = datetime.datetime.now()
        current_second = int(current_time.strftime("%S"))
        hardpy.set_message(
            f"System time second: {str(current_second)}", "Time Synchronization"
        )
        time.sleep(1)
