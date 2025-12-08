# Copyright (c) 2025 Demo
# Test module for communication tests

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
