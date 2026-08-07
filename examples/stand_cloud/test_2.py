import pytest
from driver_example import DriverExample

import jig

pytestmark = pytest.mark.module_name("Main tests")


@pytest.mark.case_name("Minute check")
def test_minute_parity(driver_example: DriverExample):
    minute = driver_example.current_minute
    jig.set_message(f"Current minute {minute}")
    result = minute % 2
    jig.set_case_measurement(
        jig.NumericMeasurement(value=minute, name="Current minute"),
    )
    error_code = 1
    error_msg = f"The test failed because {minute} is odd! Try again!"
    assert result == 0, jig.ErrorCode(error_code, error_msg)
