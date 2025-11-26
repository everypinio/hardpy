import pytest
import hardpy
import datetime
from uuid import uuid4
import time

pytestmark = pytest.mark.module_name("HardPy template")


@pytest.mark.case_name("Test 1")
def test_message():
    serial_number = str(uuid4())[:6]
    hardpy.set_dut_serial_number(serial_number)
    hardpy.set_message(f"Serial number: {serial_number}")


@pytest.mark.case_name("Test 2")
def test_seconds():
    for _ in range(10):
        current_time = datetime.datetime.now()
        current_second = int(current_time.strftime("%S"))
        hardpy.set_message(f"Second now {str(current_second)}", "Currect second")
        time.sleep(1)
