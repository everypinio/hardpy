# Copyright (c) 2025 Demo
# Pytest configuration and fixtures for HardPy tests

import pytest


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
