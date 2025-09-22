import pytest

from hardpy import (
    ComparisonOperation as CompOp,
    NumericMeasurement,
    set_case_measurement,
    set_message,
)

pytestmark = pytest.mark.module_name("Numeric measurement")


@pytest.mark.case_name("Test 1")
@pytest.mark.skip(reason="dont fail")
def test_1():
    meas0 = NumericMeasurement(value=1.0, name="Just a value")
    set_case_measurement(meas0)
    set_message(f"{meas0.value}")
    meas1 = NumericMeasurement(value=10, unit="cm", operation=CompOp.EQ, comparison_value=10)
    set_case_measurement(meas1)
    meas2 = NumericMeasurement(value=9, unit="cm", operation=CompOp.EQ, comparison_value=10)
    set_case_measurement(meas2)
    assert meas1.result
    assert meas2.result, "value is not equal to 10"


@pytest.mark.case_name("Test 2")
def test_2():
    meas = NumericMeasurement(value=5, operation=CompOp.NE, comparison_value=3)
    set_case_measurement(meas)
    assert meas.result


@pytest.mark.case_name("Test 3")
def test_3():
    meas = NumericMeasurement(
        value=7,
        operation=CompOp.GELE,
        lower_limit=5,
        upper_limit=10,
    )
    set_case_measurement(meas)
    assert meas.result
