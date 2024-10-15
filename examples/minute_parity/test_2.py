import datetime
from time import sleep

import pytest
from driver_example import DriverExample

import hardpy

pytestmark = [
    pytest.mark.module_name("Main tests"),
]

count = 0


@pytest.mark.attempt(5)
def test_attempt():
    global count  # noqa: PLW0603
    count += 1
    sleep(0.5)
    if count <= 3:  # noqa: PLR2004
        msg = "Test failed intentionally"
        raise Exception(msg)  # noqa: TRY002
    assert True


@pytest.mark.attempt(5)
def test_attempt_minute_parity():
    current_time = datetime.datetime.now()  # noqa: DTZ005
    minute = int(current_time.strftime("%M"))
    hardpy.set_message(f"Current minute {minute}", "msg_upd")
    result = minute % 2
    sleep(10)
    data = {
        "minute": minute,
    }
    hardpy.set_case_artifact(data)
    assert result == 0, f"The test failed because {minute} is odd! Try again!"


@pytest.mark.attempt(5)
@pytest.mark.case_name("Minute check")
def test_minute_parity(driver_example: DriverExample):
    minute = driver_example.current_minute
    hardpy.set_message(f"Current minute {minute}", "msg_upd")
    result = minute % 2
    data = {
        "minute": minute,
    }
    hardpy.set_case_artifact(data)
    assert result == 0, f"The test failed because {minute} is odd! Try again!"
