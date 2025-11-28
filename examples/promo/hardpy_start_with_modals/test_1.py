import pytest
import hardpy


pytestmark = pytest.mark.module_name("Production Test - Power Supply Unit")


@pytest.mark.case_name("Input Voltage Verification")
def test_input_voltage_verification():
    assert True
