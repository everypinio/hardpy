import contextlib

import pytest

from hardpy import ComparisonOperation as CompOp, NumericMeasurement, set_measurement

pytestmark = pytest.mark.module_name("Measurement example")


@pytest.mark.case_name("Test 1")
def test_1():
    meas1 = NumericMeasurement(value=10, operation=CompOp.EQ, comparison_value=10)
    set_measurement(meas1)
    meas2 = NumericMeasurement(value=9, operation=CompOp.EQ, comparison_value=10)
    set_measurement(meas2)
    assert meas1.check_condition()
    assert meas2.check_condition(), "value is not equal to 10"


@pytest.mark.case_name("Test 1")
def test_2():
    meas = NumericMeasurement(value=5, operation=CompOp.GT, comparison_value=3)
    set_measurement(meas)
    assert meas.check_condition()


@pytest.mark.case_name("Test 1")
def test_3():
    meas = NumericMeasurement(
        value=7,
        operation=CompOp.GELE,
        lower_limit=5,
        upper_limit=10,
    )
    set_measurement(meas)
    assert meas.check_condition()

    with contextlib.suppress(ValueError):
        NumericMeasurement(value=7, operation=CompOp.EQ)
