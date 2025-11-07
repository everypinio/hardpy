import pytest

from hardpy import (
    ComparisonOperation as CompOp,
    StringMeasurement,
    set_case_measurement,
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

    assert simple_str_meas.result
    assert serial_meas.result
    assert not failed_str_meas.result, "Wrong status code"
