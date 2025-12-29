import hardpy
import pytest
from time import sleep


@pytest.mark.case_name("Check Power Supply Voltage")
@pytest.mark.module_name("Power Supply Tests")
def test_power_supply_voltage():
    """Test that power supply outputs correct voltage."""
    # Set test stand information
    hardpy.set_stand_name("Test Bench #1")
    hardpy.set_stand_location("Lab A")

    # Set device under test information
    hardpy.set_dut_serial_number("PSU-12345")
    hardpy.set_dut_name("Power Supply Unit")
    hardpy.set_dut_type("DC Power Supply")

    # Simulate voltage measurement
    expected_voltage = 5.0
    measured_voltage = 5.02  # Simulated measurement
    tolerance = 0.1

    # Record measurement
    hardpy.set_case_measurement(
        hardpy.NumericMeasurement(
            name="Output Voltage",
            value=measured_voltage,
            unit="V",
            lower_limit=expected_voltage - tolerance,
            upper_limit=expected_voltage + tolerance,
        )
    )

    # Add message
    hardpy.set_message(f"Measured voltage: {measured_voltage}V (expected: {expected_voltage}V)")

    # Verify voltage is within tolerance
    assert abs(measured_voltage - expected_voltage) <= tolerance, \
        f"Voltage out of tolerance: {measured_voltage}V"


@pytest.mark.case_name("Check Current Limit")
@pytest.mark.module_name("Power Supply Tests")
def test_current_limit():
    """Test that power supply has correct current limit."""
    # Simulate current limit test
    expected_limit = 3.0
    measured_limit = 3.05  # Simulated measurement
    tolerance = 0.2

    # Record measurement
    hardpy.set_case_measurement(
        hardpy.NumericMeasurement(
            name="Current Limit",
            value=measured_limit,
            unit="A",
            lower_limit=expected_limit - tolerance,
            upper_limit=expected_limit + tolerance,
        )
    )

    hardpy.set_message(f"Current limit: {measured_limit}A")

    assert abs(measured_limit - expected_limit) <= tolerance


@pytest.mark.case_name("Voltage Stability Test")
@pytest.mark.module_name("Power Supply Tests")
@pytest.mark.attempt(2)  # Retry once if fails
def test_voltage_stability():
    """Test voltage stability over time."""
    hardpy.set_message("Testing voltage stability over 5 seconds...")

    voltage_readings = []
    for i in range(5):
        # Simulate reading voltage
        voltage = 5.0 + (i * 0.01)  # Slight increase
        voltage_readings.append(voltage)
        sleep(0.1)  # Simulate measurement delay

    max_variation = max(voltage_readings) - min(voltage_readings)

    # Record measurement
    hardpy.set_case_measurement(
        hardpy.NumericMeasurement(
            name="Voltage Variation",
            value=max_variation,
            unit="V",
            upper_limit=0.1,
        )
    )

    hardpy.set_message(f"Max voltage variation: {max_variation:.3f}V")

    assert max_variation < 0.1, f"Voltage not stable: {max_variation}V variation"
