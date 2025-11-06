import pytest

from hardpy import (
    ComparisonOperation as CompOp,
    NumericMeasurement,
    StringMeasurement,
    set_case_measurement,
    set_message,
)

pytestmark = pytest.mark.module_name("String measurement")


@pytest.mark.case_name("Basic string operations")
def test_basic_string_operations():
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

    assert meas1.result
    assert not meas2.result
    assert meas3.result


@pytest.mark.case_name("Advanced string measurements")
def test_advanced_string_measurements():
    set_message("Starting string measurements...")

    simple_str_meas = StringMeasurement(
        value="abc", operation=CompOp.EQ, comparison_value="abc"
    )
    set_case_measurement(simple_str_meas)

    serial_meas = StringMeasurement(
        name="Serial Number",
        value="SN123456",
        operation=CompOp.NE,
        comparison_value="SN000000",
    )
    set_case_measurement(serial_meas)

    failed_str_meas = StringMeasurement(
        name="Wrong Code", value="FAIL", operation=CompOp.EQ, comparison_value="PASS"
    )
    set_case_measurement(failed_str_meas)

    info_meas = StringMeasurement(value="INFO")
    set_case_measurement(info_meas)

    set_message("String measurements completed")

    assert simple_str_meas.result
    assert serial_meas.result
    assert not failed_str_meas.result, "Wrong status code"


@pytest.mark.case_name("Mixed measurements with messages")
def test_mixed_measurements_with_messages():
    set_message("Starting mixed measurements...")

    voltage_meas = NumericMeasurement(name="Input Voltage", value=12.3, unit="V")
    set_case_measurement(voltage_meas)

    set_message("Voltage measurement completed")

    current_meas = NumericMeasurement(name="Current", value=0.5, unit="A")
    set_case_measurement(current_meas)

    status_meas = StringMeasurement(
        name="Status", value="OK", operation=CompOp.EQ, comparison_value="OK"
    )
    set_case_measurement(status_meas)

    set_message("All measurements done")

    assert voltage_meas.value > 10
    assert current_meas.value < 1.0
    assert status_meas.result
