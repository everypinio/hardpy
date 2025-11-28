import pytest

from hardpy import (
    ComparisonOperation as CompOp,
    NumericMeasurement,
    set_case_measurement,
)

pytestmark = pytest.mark.module_name("Production Test - Electrical Parameters")


@pytest.mark.case_name("Basic Electrical Measurements")
def test_basic_electrical_measurements():
    # Test basic voltage measurement without limits
    voltage_raw = NumericMeasurement(value=12.0, unit="V")
    set_case_measurement(voltage_raw)

    # Test exact voltage match (nominal voltage)
    voltage_nominal = NumericMeasurement(
        value=12.0, operation=CompOp.EQ, comparison_value=12.0, unit="V"
    )
    set_case_measurement(voltage_nominal)

    # Test voltage tolerance failure
    voltage_tolerance = NumericMeasurement(
        value=11.8, operation=CompOp.EQ, comparison_value=12.0, unit="V"
    )
    set_case_measurement(voltage_tolerance)

    # Test current not equal to zero (system active)
    current_active = NumericMeasurement(
        value=0.5, operation=CompOp.NE, comparison_value=0, unit="A"
    )
    set_case_measurement(current_active)

    # Test voltage within operating range
    voltage_range = NumericMeasurement(
        value=12.2, operation=CompOp.GELE, lower_limit=11.5, upper_limit=12.5, unit="V"
    )
    set_case_measurement(voltage_range)

    assert voltage_nominal.result
    assert voltage_tolerance.result, "Voltage out of tolerance"
    assert current_active.result
    assert voltage_range.result


@pytest.mark.case_name("Critical Parameter Verification")
def test_critical_parameter_verification():
    # Power supply voltage verification
    main_voltage = NumericMeasurement(
        name="Main Supply Voltage",
        value=24.0,
        unit="V",
        operation=CompOp.GELE,
        lower_limit=23.0,
        upper_limit=25.0,
    )
    set_case_measurement(main_voltage)

    # Operating temperature check
    board_temperature = NumericMeasurement(
        name="PCB Temperature",
        value=45.2,
        unit="°C",
        operation=CompOp.GELE,
        lower_limit=0,
        upper_limit=85,
    )
    set_case_measurement(board_temperature)

    # Efficiency measurement
    power_efficiency = NumericMeasurement(
        value=94.8,
        unit="%",
        operation=CompOp.GE,
        comparison_value=90,
    )
    set_case_measurement(power_efficiency)

    # Frequency stability test
    clock_frequency = NumericMeasurement(
        name="Crystal Frequency",
        value=16.0,
        unit="MHz",
        operation=CompOp.EQ,
        comparison_value=16.0,
    )
    set_case_measurement(clock_frequency)

    assert all(
        [
            main_voltage.result,
            board_temperature.result,
            power_efficiency.result,
            clock_frequency.result,
        ],
    )


@pytest.mark.case_name("Out-of-Spec Measurements")
def test_out_of_spec_measurements():
    # Over-voltage protection test
    over_voltage = NumericMeasurement(
        name="Over-voltage Protection",
        value=15.5,
        unit="V",
        operation=CompOp.LE,
        comparison_value=13.8,
    )
    set_case_measurement(over_voltage)

    # Under-temperature shutdown test
    low_temperature = NumericMeasurement(
        name="Low Temperature Operation",
        value=-15,
        unit="°C",
        operation=CompOp.GELE,
        lower_limit=-10,
        upper_limit=60,
    )
    set_case_measurement(low_temperature)

    # Raw resistance measurement
    shunt_resistance = NumericMeasurement(name="Shunt Resistor", value=0.1, unit="Ω")
    set_case_measurement(shunt_resistance)

    # Phase measurement
    phase_angle = NumericMeasurement(value=0.78, unit="rad")
    set_case_measurement(phase_angle)

    assert not over_voltage.result, "Over-voltage protection failed"
    assert not low_temperature.result, "Temperature below operating limit"
