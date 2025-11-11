import pytest

from hardpy import (
    ComparisonOperation as CompOp,
    NumericMeasurement,
    set_case_measurement,
)

pytestmark = pytest.mark.module_name("All comparison operations test")


@pytest.mark.case_name("Operation types with brackets")
def test_all_operation_types_with_brackets():
    meas_lt = NumericMeasurement(value=4, operation=CompOp.LT, comparison_value=5)
    set_case_measurement(meas_lt)

    meas_gelt = NumericMeasurement(
        value=3,
        operation=CompOp.GELT,
        lower_limit=2,
        upper_limit=4,
    )
    set_case_measurement(meas_gelt)

    meas_legt = NumericMeasurement(
        value=1,
        operation=CompOp.LEGT,
        lower_limit=2,
        upper_limit=4,
    )
    set_case_measurement(meas_legt)

    assert meas_lt.result
    assert meas_gelt.result
    assert meas_legt.result


@pytest.mark.case_name("Edge cases with units")
def test_edge_cases_with_units():
    meas_percent = NumericMeasurement(
        name="Efficiency",
        value=95.5,
        unit="%",
        operation=CompOp.GELE,
        lower_limit=90,
        upper_limit=100,
    )
    set_case_measurement(meas_percent)

    meas_degrees = NumericMeasurement(
        name="Angle",
        value=45,
        unit="°",
        operation=CompOp.GTLT,
        lower_limit=0,
        upper_limit=90,
    )
    set_case_measurement(meas_degrees)

    meas_minutes = NumericMeasurement(
        name="Duration",
        value=30,
        unit="′",
        operation=CompOp.LE,
        comparison_value=60,
    )
    set_case_measurement(meas_minutes)

    meas_voltage = NumericMeasurement(
        name="Voltage",
        value=3.3,
        unit="V",
        operation=CompOp.GELT,
        lower_limit=3.0,
        upper_limit=3.6,
    )
    set_case_measurement(meas_voltage)

    assert meas_percent.result
    assert meas_degrees.result
    assert meas_minutes.result
    assert meas_voltage.result


@pytest.mark.case_name("Boundary value tests")
def test_boundary_value_tests():
    meas_gt_boundary = NumericMeasurement(
        value=2.1,
        operation=CompOp.GTLT,
        lower_limit=2,
        upper_limit=4,
    )
    set_case_measurement(meas_gt_boundary)

    meas_ge_boundary = NumericMeasurement(
        value=2,
        operation=CompOp.GELE,
        lower_limit=2,
        upper_limit=4,
    )
    set_case_measurement(meas_ge_boundary)

    meas_mixed_boundary = NumericMeasurement(
        value=4,
        operation=CompOp.GTLE,
        lower_limit=2,
        upper_limit=4,
    )
    set_case_measurement(meas_mixed_boundary)

    assert meas_gt_boundary.result
    assert meas_ge_boundary.result
    assert meas_mixed_boundary.result
