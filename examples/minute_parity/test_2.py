import pytest
from driver_example import DriverExample

import hardpy

pytestmark = pytest.mark.module_name("Main tests")


@pytest.mark.case_name("Minute check")
def test_minute_parity(driver_example: DriverExample):
    minute = driver_example.current_minute
    result = minute % 2
    hardpy.set_case_measurement(
        hardpy.NumericMeasurement(value=minute, name="Current minute"),
    )
    error_code = 1
    error_msg = f"The test failed because {minute} is odd! Try again!"
    assert result == 0, hardpy.ErrorCode(error_code, error_msg)
