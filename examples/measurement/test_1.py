import pytest

from hardpy import (
    ComparisonOperation as CompOp,
    NumericMeasurement,
    set_case_measurement,
)

pytestmark = pytest.mark.module_name("Numeric measurement")


@pytest.mark.case_name("Basic numeric operations")
def test_basic_numeric_operations():
    meas0 = NumericMeasurement(value=1.0)
    set_case_measurement(meas0)

    meas1 = NumericMeasurement(value=10, operation=CompOp.EQ, comparison_value=10)
    set_case_measurement(meas1)

    meas2 = NumericMeasurement(value=9, operation=CompOp.EQ, comparison_value=10)
    set_case_measurement(meas2)

    meas3 = NumericMeasurement(value=5, operation=CompOp.NE, comparison_value=3)
    set_case_measurement(meas3)

    meas4 = NumericMeasurement(
        value=7,
        operation=CompOp.GELE,
        lower_limit=5,
        upper_limit=10,
    )
    set_case_measurement(meas4)

    assert meas1.result
    assert meas2.result, "value is not equal to 10"
    assert meas3.result
    assert meas4.result


@pytest.mark.case_name("Advanced numeric measurements")
def test_advanced_numeric_measurements():
    voltage_meas = NumericMeasurement(
        name="Voltage",
        value=1.2,
        unit="V",
        operation=CompOp.GELE,
        lower_limit=1.0,
        upper_limit=1.5,
    )
    set_case_measurement(voltage_meas)

    temperature_meas = NumericMeasurement(
        name="Temperature",
        value=23.5,
        unit="°C",
        operation=CompOp.GELE,
        lower_limit=20,
        upper_limit=25,
    )
    set_case_measurement(temperature_meas)

    percentage_meas = NumericMeasurement(
        value=98.6,
        unit="%",
        operation=CompOp.GE,
        comparison_value=95,
    )
    set_case_measurement(percentage_meas)

    minutes_meas = NumericMeasurement(
        name="Time",
        value=30,
        unit="′",
        operation=CompOp.EQ,
        comparison_value=30,
    )
    set_case_measurement(minutes_meas)

    assert all(
        [
            voltage_meas.result,
            temperature_meas.result,
            percentage_meas.result,
            minutes_meas.result,
        ],
    )


@pytest.mark.case_name("Failed numeric measurements")
def test_failed_numeric_measurements():
    high_voltage_meas = NumericMeasurement(
        name="High Voltage",
        value=15.0,
        unit="V",
        operation=CompOp.LE,
        comparison_value=12.0,
    )
    set_case_measurement(high_voltage_meas)

    low_temp_meas = NumericMeasurement(
        name="Low Temp",
        value=-10,
        unit="°C",
        operation=CompOp.GELE,
        lower_limit=0,
        upper_limit=50,
    )
    set_case_measurement(low_temp_meas)

    raw_meas = NumericMeasurement(name="Raw Value", value=42.0)
    set_case_measurement(raw_meas)

    rad_meas = NumericMeasurement(value=3.14, unit="rad")
    set_case_measurement(rad_meas)

    assert not high_voltage_meas.result, "Voltage too high"
    assert not low_temp_meas.result, "Temperature too low"
