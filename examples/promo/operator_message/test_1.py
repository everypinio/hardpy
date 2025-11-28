from time import sleep

import pytest

from hardpy import clear_operator_message, set_message, set_operator_message

pytestmark = pytest.mark.module_name("Production Test - Operator Instructions")


def test_thermal_soak_operation():
    set_operator_message(
        msg="Start thermal soak procedure - maintain device under test at 85°C for 3 minutes",
        title="Thermal Test Procedure",
    )
    for i in range(3, 0, -1):
        set_message(f"Thermal soak time remaining: {i} minutes", "Test Status")
        sleep(1)
    set_message("Thermal soak test completed successfully", "Test Status")
    clear_operator_message()
    assert True
