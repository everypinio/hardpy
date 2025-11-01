import pytest

from hardpy import (
    ComparisonOperation as CompOp,
    StringMeasurement,
    set_case_measurement,
)

pytestmark = pytest.mark.module_name("String measurement")


@pytest.mark.case_name("String comparisons")
def test_string_comparisons():
    meas1 = StringMeasurement(
        value="1.2.1",
        operation=CompOp.EQ,
        comparison_value="1.2.1",
    )
    set_case_measurement(meas1)

    meas2 = StringMeasurement(
        value="ABC",
        operation=CompOp.EQ,
        comparison_value="abc",
    )
    set_case_measurement(meas2)

    meas3 = StringMeasurement(
        value="ABC",
        operation=CompOp.EQ,
        casesensitive=False,
        comparison_value="abc",
    )
    set_case_measurement(meas3)

    meas4 = StringMeasurement(
        name="Version", value="v2.0.1", operation=CompOp.EQ, comparison_value="v2.0.1"
    )
    set_case_measurement(meas4)

    assert meas1.result
    assert not meas2.result
    assert meas3.result
    assert meas4.result
