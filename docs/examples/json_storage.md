# JSON storage

This is an example of using **pytest-hardpy** functions, storing
the result to JSON file.
The code for this example can be seen inside the hardpy package
[JSON storage](https://github.com/everypinio/hardpy/tree/main/examples/json_storage).

### how to start

1. Launch `hardpy init --no-create-database --storage-type json json_storage`.
2. Modify the files described below.
3. Launch `hardpy run json_storage`.

### hardpy.toml

Replace the settings in the `[frontend]` and `[frontend.modal_result]` sections 
with those shown in the **hardpy.toml** example file below.

```toml
title = "HardPy JSON Storage Demo"
tests_name = "Device Test Suite"

[database]
storage_type = "json"
storage_path = "result"

[frontend]
host = "localhost"
port = 8000
language = "en"
sound_on = false
full_size_button = false
manual_collect = false
measurement_display = true

[frontend.modal_result]
enable = true
auto_dismiss_pass = true
auto_dismiss_timeout = 5
```

### conftest.py

```python
from pathlib import Path
import pytest

from hardpy import JsonLoader, get_current_report


@pytest.fixture(scope="session")
def setup_test_environment():
    """Set up test environment before all tests."""
    print("\n=== Setting up test environment ===")
    # Add any global setup here
    yield
    print("\n=== Tearing down test environment ===")
    # Add any global cleanup here


@pytest.fixture(scope="function")
def test_device():
    """Fixture providing simulated test device."""

    class TestDevice:
        def __init__(self):
            self.connected = False
            self.voltage = 5.0
            self.current = 0.0

        def connect(self):
            self.connected = True
            return True

        def disconnect(self):
            self.connected = False

        def measure_voltage(self):
            return self.voltage

        def measure_current(self):
            return self.current

    device = TestDevice()
    device.connect()

    yield device

    device.disconnect()


def save_report_to_dir():
    report = get_current_report()
    if report:
        loader = JsonLoader(Path.cwd() / "reports")
        loader.load(report)


@pytest.fixture(scope="session", autouse=True)
def fill_actions_after_test(post_run_functions: list):
    post_run_functions.append(save_report_to_dir)
    yield
```

### test_chart_demo.py

```python
import hardpy
import pytest
import math

@pytest.mark.case_name("Sine Wave Analysis")
@pytest.mark.module_name("Chart Demonstrations")
def test_sine_wave():
    """Test generating and analyzing a sine wave."""
    hardpy.set_message("Generating sine wave data...")

    # Generate sine wave data
    x_data = []
    y_data = []

    for i in range(100):
        x = i / 10.0  # 0 to 10
        y = math.sin(x)
        x_data.append(x)
        y_data.append(y)

    # Create chart
    chart = hardpy.Chart(
        title="Sine Wave",
        x_label="Time",
        y_label="Amplitude",
        type=hardpy.ChartType.LINE,
    )
    chart.add_series(x_data, y_data, "Sine Wave")

    hardpy.set_case_chart(chart)

    # Verify amplitude
    max_amplitude = max(y_data)
    min_amplitude = min(y_data)
    peak_to_peak = max_amplitude - min_amplitude

    hardpy.set_case_measurement(
        hardpy.NumericMeasurement(
            name="Peak-to-Peak Amplitude",
            value=peak_to_peak,
            unit="V",
            lower_limit=1.9,
            upper_limit=2.1,
        )
    )

    hardpy.set_message(f"Peak-to-peak amplitude: {peak_to_peak:.3f}V")

    assert 1.9 <= peak_to_peak <= 2.1, "Amplitude out of range"

@pytest.mark.case_name("Temperature Curve")
@pytest.mark.module_name("Chart Demonstrations")
def test_temperature_curve():
    """Test temperature rise curve."""
    hardpy.set_message("Recording temperature curve...")

    # Simulate temperature rise
    time_data = []
    temp_data = []

    for i in range(50):
        time = i * 2  # seconds
        # Exponential rise to 80°C
        temp = 25 + 55 * (1 - math.exp(-i / 20))
        time_data.append(time)
        temp_data.append(temp)

    # Create chart
    chart = hardpy.Chart(
        title="Temperature Rise Curve",
        x_label="Time (seconds)",
        y_label="Temperature (°C)",
        type=hardpy.ChartType.LINE,
    )
    chart.add_series(time_data, temp_data, "Temperature")

    hardpy.set_case_chart(chart)

    # Check final temperature
    final_temp = temp_data[-1]

    hardpy.set_case_measurement(
        hardpy.NumericMeasurement(
            name="Final Temperature",
            value=final_temp,
            unit="°C",
            upper_limit=85,
        )
    )

    hardpy.set_message(f"Final temperature: {final_temp:.1f}°C")

    assert final_temp < 85, f"Temperature too high: {final_temp}°C"
```

### test_communication.py

```python
import hardpy
import pytest
from time import sleep

@pytest.mark.case_name("Serial Port Connection")
@pytest.mark.module_name("Communication Tests")
def test_serial_connection():
    """Test serial port connection."""
    hardpy.set_message("Testing serial port connection...")

    # Simulate connection
    port = "/dev/ttyUSB0"
    baudrate = 115200

    hardpy.set_instrument(
        hardpy.Instrument(
            name="Serial Port",
            comment=f"{port} @ {baudrate} baud"
        )
    )

    # Simulate successful connection
    connection_ok = True

    hardpy.set_message(f"Connected to {port} at {baudrate} baud")

    assert connection_ok, "Failed to establish serial connection"

@pytest.mark.case_name("Data Transfer Test")
@pytest.mark.module_name("Communication Tests")
@pytest.mark.attempt(3)  # Allow 2 retries
def test_data_transfer():
    """Test data transfer over serial."""
    hardpy.set_message("Testing data transfer...")

    # Simulate sending and receiving data
    sent_bytes = 1024
    received_bytes = 1024
    transfer_time = 0.5  # seconds

    # Calculate transfer rate
    transfer_rate = (sent_bytes + received_bytes) / transfer_time

    hardpy.set_case_measurement(
        hardpy.NumericMeasurement(
            name="Transfer Rate",
            value=transfer_rate,
            unit="bytes/s",
            lower_limit=1000,
        )
    )

    hardpy.set_message(f"Transfer rate: {transfer_rate:.0f} bytes/s")

    assert received_bytes == sent_bytes, "Data integrity error"
    assert transfer_rate > 1000, "Transfer rate too slow"

@pytest.mark.case_name("Protocol Validation")
@pytest.mark.module_name("Communication Tests")
@pytest.mark.critical  # Critical test - stops all if fails
def test_protocol_validation():
    """Test communication protocol validation."""
    hardpy.set_message("Validating communication protocol...")

    # Simulate protocol check
    protocol_version = "v2.1"
    expected_version = "v2.1"

    hardpy.set_case_measurement(
        hardpy.StringMeasurement(
            name="Protocol Version",
            value=protocol_version,
            comparison_value=expected_version,
        )
    )

    hardpy.set_message(f"Protocol version: {protocol_version}")

    assert protocol_version == expected_version, \
        f"Protocol mismatch: got {protocol_version}, expected {expected_version}"

@pytest.mark.case_name("Error Handling Test")
@pytest.mark.module_name("Communication Tests")
@pytest.mark.dependency("test_communication::test_protocol_validation")
def test_error_handling():
    """Test error handling (depends on protocol validation)."""
    hardpy.set_message("Testing error handling...")

    # Simulate error injection and recovery
    errors_injected = 5
    errors_handled = 5

    hardpy.set_case_measurement(
        hardpy.NumericMeasurement(
            name="Errors Handled",
            value=errors_handled,
            unit="count",
            comparison_value=errors_injected,
        )
    )

    hardpy.set_message(f"Handled {errors_handled}/{errors_injected} errors")

    assert errors_handled == errors_injected, "Some errors not handled correctly"
```

### test_voltage.py

```python
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
```
