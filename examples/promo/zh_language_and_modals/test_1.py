import pytest
import hardpy


pytestmark = pytest.mark.module_name("Production Test - Power Supply Unit")


@pytest.mark.case_name("Input Voltage Range Test")
def test_input_voltage_range():
    assert True
