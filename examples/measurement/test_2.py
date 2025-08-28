import pytest

from hardpy import (
    ComparisonOperation as CompOp,
    StringMeasurement,
    set_measurement,
)

pytestmark = pytest.mark.module_name("String measurement")


@pytest.mark.case_name("Test 1")
def test_1():
    meas1 = StringMeasurement(
        value="1.2.1",
        operation=CompOp.EQ,
        comparison_value="1.2.1",
    )
    set_measurement(meas1)
    assert meas1.result

    meas2 = StringMeasurement(
        value="ABC",
        operation=CompOp.EQ,
        comparison_value="abc",
    )
    meas3 = StringMeasurement(
        value="ABC",
        operation=CompOp.EQ,
        casesensitive=False,
        comparison_value="abc",
    )
    assert not meas2.result
    assert meas3.result
