import pytest
from hardpy import (
    ComparisonOperation as CompOp,
    NumericMeasurement,
    StringMeasurement,
    set_case_measurement,
    set_message,
)

pytestmark = pytest.mark.module_name("Measurement Demonstration")


@pytest.mark.case_name("All measurement types")
def test_all_measurement_types():
    meas1 = NumericMeasurement(
        name="Voltage",
        value=1.2,
        unit="V",
        operation=CompOp.GELE,
        lower_limit=1.0,
        upper_limit=1.5,
    )
    set_case_measurement(meas1)

    meas2 = NumericMeasurement(
        value=5, unit="°", operation=CompOp.EQ, comparison_value=5
    )
    set_case_measurement(meas2)

    meas3 = StringMeasurement(value="abc", operation=CompOp.EQ, comparison_value="abc")
    set_case_measurement(meas3)

    meas4 = NumericMeasurement(
        name="Banana", value=15, operation=CompOp.GT, comparison_value=10
    )
    set_case_measurement(meas4)

    meas5 = NumericMeasurement(
        name="Temperature",
        value=23.5,
        unit="°C",
        operation=CompOp.GELE,
        lower_limit=20,
        upper_limit=25,
    )
    set_case_measurement(meas5)

    meas6 = NumericMeasurement(
        value=98.6, unit="%", operation=CompOp.GE, comparison_value=95
    )
    set_case_measurement(meas6)

    meas7 = StringMeasurement(
        name="Serial Number",
        value="SN123456",
        operation=CompOp.NE,
        comparison_value="SN000000",
    )
    set_case_measurement(meas7)

    assert all(
        [
            meas1.result,
            meas2.result,
            meas3.result,
            meas4.result,
            meas5.result,
            meas6.result,
            meas7.result,
        ]
    )


@pytest.mark.case_name("Failed measurements")
def test_failed_measurements():
    meas1 = NumericMeasurement(
        name="High Voltage",
        value=15.0,
        unit="V",
        operation=CompOp.LE,
        comparison_value=12.0,
    )
    set_case_measurement(meas1)

    meas2 = NumericMeasurement(
        name="Low Temp",
        value=-10,
        unit="°C",
        operation=CompOp.GELE,
        lower_limit=0,
        upper_limit=50,
    )
    set_case_measurement(meas2)

    meas3 = StringMeasurement(
        name="Wrong Code", value="FAIL", operation=CompOp.EQ, comparison_value="PASS"
    )
    set_case_measurement(meas3)

    assert not meas1.result, "Voltage too high"
    assert not meas2.result, "Temperature too low"
    assert not meas3.result, "Wrong status code"


@pytest.mark.case_name("Mixed with messages")
def test_mixed_with_messages():
    set_message("Starting voltage measurement...")

    meas1 = NumericMeasurement(name="Input Voltage", value=12.3, unit="V")
    set_case_measurement(meas1)

    set_message("Voltage measurement completed")

    meas2 = NumericMeasurement(name="Current", value=0.5, unit="A")
    set_case_measurement(meas2)

    set_message("All measurements done")

    assert meas1.value > 10
    assert meas2.value < 1.0


@pytest.mark.case_name("Measurement without result")
def test_measurement_without_result():
    meas1 = NumericMeasurement(name="Raw Value", value=42.0)
    set_case_measurement(meas1)

    meas2 = StringMeasurement(value="INFO")
    set_case_measurement(meas2)

    meas3 = NumericMeasurement(value=3.14, unit="rad")
    set_case_measurement(meas3)
