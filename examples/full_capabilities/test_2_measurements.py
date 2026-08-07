"""Numeric and string measurements, with and without limits."""

import pytest
from simulated_device import SimulatedDevice  # type: ignore[import-not-found]

from hardpy import (
    ComparisonOperation as CompOp,
    NumericMeasurement,
    StringMeasurement,
    set_case_artifact,
    set_case_measurement,
    set_message,
    set_module_artifact,
)

pytestmark = pytest.mark.module_name("Measurements")

SUPPLY_VOLTAGE_LIMITS_V = (3.2, 3.4)
IDLE_CURRENT_LIMIT_MA = 20.0


@pytest.mark.case_name("Supply voltage")
def test_supply_voltage(device: SimulatedDevice):
    """Check a value against a lower and an upper limit."""
    lower_limit, upper_limit = SUPPLY_VOLTAGE_LIMITS_V
    voltage = device.measure_supply_voltage()

    measurement = NumericMeasurement(
        name="Supply voltage",
        value=voltage,
        unit="V",
        operation=CompOp.GELE,
        lower_limit=lower_limit,
        upper_limit=upper_limit,
    )
    set_case_measurement(measurement)
    set_case_artifact({"supply_voltage_v": voltage})

    assert measurement.result, f"Voltage {voltage} V is outside the limits"


@pytest.mark.case_name("Idle current")
def test_idle_current(device: SimulatedDevice):
    """Check a value against a single comparison value."""
    current = device.measure_idle_current()

    measurement = NumericMeasurement(
        name="Idle current",
        value=current,
        unit="mA",
        operation=CompOp.LE,
        comparison_value=IDLE_CURRENT_LIMIT_MA,
    )
    set_case_measurement(measurement)

    assert measurement.result, f"Current {current} mA is above the limit"


@pytest.mark.case_name("Recorded values")
def test_recorded_values(device: SimulatedDevice):
    """Record values that are stored but not judged.

    A measurement without an operation has no result, it only documents the run.
    """
    power = device.measure_supply_voltage() * device.measure_idle_current()
    set_case_measurement(NumericMeasurement(name="Idle power", value=power, unit="mW"))
    set_case_measurement(
        StringMeasurement(name="Firmware", value=device.read_firmware_version()),
    )
    set_message(f"Idle power is {power:.1f} mW")


@pytest.mark.case_name("Labels")
def test_labels(device: SimulatedDevice):
    """Compare strings, optionally ignoring the case."""
    label = f"JIG-{device.serial_number}"

    measurement = StringMeasurement(
        name="Label",
        value=label.lower(),
        operation=CompOp.EQ,
        comparison_value=label,
        casesensitive=False,
    )
    set_case_measurement(measurement)
    set_module_artifact({"printed_label": label})

    assert measurement.result, f"Label {label} was not recognized"
