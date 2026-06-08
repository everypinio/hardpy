"""Measurements module — slow with a mid-run failure (triggers auto-expand)."""

import time
import pytest

from hardpy import (
    ComparisonOperation as CompOp,
    NumericMeasurement,
    set_case_measurement,
)

pytestmark = pytest.mark.module_name("Measurements")


@pytest.mark.case_name("Voltage rail 3V3")
def test_meas_3v3():
    time.sleep(2.0)
    meas = NumericMeasurement(
        value=3.31,
        unit="V",
        operation=CompOp.GELE,
        lower_limit=3.20,
        upper_limit=3.40,
    )
    set_case_measurement(meas)
    assert meas.result


@pytest.mark.case_name("Voltage rail 5V0")
def test_meas_5v0():
    time.sleep(2.0)
    meas = NumericMeasurement(
        value=5.02,
        unit="V",
        operation=CompOp.GELE,
        lower_limit=4.90,
        upper_limit=5.10,
    )
    set_case_measurement(meas)
    assert meas.result


@pytest.mark.case_name("Voltage rail 12V (fails)")
def test_meas_12v_fail():
    time.sleep(2.0)
    meas = NumericMeasurement(
        value=10.8,
        unit="V",
        operation=CompOp.GELE,
        lower_limit=11.5,
        upper_limit=12.5,
    )
    set_case_measurement(meas)
    assert meas.result, "12V rail out of spec - supply or load issue"


@pytest.mark.case_name("Current draw")
def test_meas_current():
    time.sleep(2.0)
    meas = NumericMeasurement(
        value=0.42,
        unit="A",
        operation=CompOp.LE,
        comparison_value=1.0,
    )
    set_case_measurement(meas)
    assert meas.result
