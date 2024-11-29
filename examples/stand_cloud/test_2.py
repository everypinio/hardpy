import pytest
from driver_example import DriverExample

import hardpy

pytestmark = [
    pytest.mark.module_name("Main tests"),
]


@pytest.mark.case_name("Minute check")
def test_minute_parity(driver_example: DriverExample):
    minute = driver_example.current_minute
    hardpy.set_message(f"Current minute {minute}")
    result = minute % 2
    data = {
        "minute": minute,
    }
    hardpy.set_case_artifact(data)
    assert result == 0, f"The test failed because {minute} is odd! Try again!"
