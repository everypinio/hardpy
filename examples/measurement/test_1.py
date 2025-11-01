import pytest

from hardpy import (
    ComparisonOperation as CompOp,
    NumericMeasurement,
    set_case_measurement,
    set_message,
)

pytestmark = pytest.mark.module_name("Numeric measurement")


@pytest.mark.case_name("Basic numeric measurements")
def test_basic_numeric():
    meas0 = NumericMeasurement(value=1.0)
    set_case_measurement(meas0)
    set_message(f"Simple value: {meas0.value}")

    meas1 = NumericMeasurement(
        name="Length", value=10, unit="cm", operation=CompOp.EQ, comparison_value=10
    )
    set_case_measurement(meas1)

    meas2 = NumericMeasurement(
        name="Width", value=9, unit="cm", operation=CompOp.EQ, comparison_value=10
    )
    set_case_measurement(meas2)

    assert meas1.result
    assert meas2.result, "Width is not equal to 10 cm"


@pytest.mark.case_name("Range measurements")
def test_range_measurements():
    meas = NumericMeasurement(
        name="Temperature",
        value=7,
        unit="°C",
        operation=CompOp.GELE,
        lower_limit=5,
        upper_limit=10,
    )
    set_case_measurement(meas)
    assert meas.result


@pytest.mark.case_name("Unit variations")
def test_unit_variations():
    meas1 = NumericMeasurement(name="Angle", value=90, unit="°")
    set_case_measurement(meas1)

    meas2 = NumericMeasurement(name="Efficiency", value=95.5, unit="%")
    set_case_measurement(meas2)

    meas3 = NumericMeasurement(name="Frequency", value=1000, unit="Hz")
    set_case_measurement(meas3)

    meas4 = NumericMeasurement(name="Count", value=42)
    set_case_measurement(meas4)

    assert all([meas1.result, meas2.result, meas3.result, meas4.result])
