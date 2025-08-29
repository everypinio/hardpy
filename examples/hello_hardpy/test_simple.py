import hardpy
import pytest
import time
import random

pytestmark = pytest.mark.module_name("Logging Demonstration Module")


@pytest.mark.case_name("Debug Messages Demonstration")
def test_debug_messages():
    """Test generates various debug messages"""
    for i in range(50):
        hardpy.set_message(f"Iteration {i+1}/50: Checking subsystem {i+1}")

        # Simulate different log levels
        if i % 10 == 1:
            hardpy.set_message("WARN: Temporary performance delays detected")
        elif i % 10 == 3:
            hardpy.set_message("ERROR: Sensor malfunction detected")

    hardpy.set_message("Demonstration completed successfully")
    hardpy.set_case_artifact({"iterations": 50, "status": "completed"})


@pytest.mark.critical
@pytest.mark.case_name("Detailed System Verification")
def test_detailed_logs():
    """Test with detailed system operation logging"""
    components = ["CPU", "Memory", "Network Interface", "Storage Subsystem"] * 10

    for i, component in enumerate(components, 1):
        hardpy.set_message(f"Testing component {i}/{len(components)}: {component}")

        # Simulate sensor readings
        if "CPU" in component:
            hardpy.set_message(f"Processor temperature: {random.randint(50, 80)}°C")
        elif "Memory" in component:
            hardpy.set_message(f"Memory usage: {random.uniform(2.0, 8.0):.1f}/8.0 GB")

    hardpy.set_message("All components operating within normal parameters")
    hardpy.set_case_artifact(
        {"checked_components": components, "result": "PASS", "timestamp": time.time()}
    )


@pytest.mark.case_name("Long Operation Simulation")
def test_long_operation():
    """Test with long-running operation and periodic logging"""
    total_steps = 100  # было 10, стало 100
    hardpy.set_message(f"Starting long operation ({total_steps} steps)")

    for step in range(total_steps):
        progress = (step + 1) / total_steps * 100
        hardpy.set_message(f"Progress: {progress:.1f}%")

        # Periodic additional logging
        if step % 3 == 0:
            hardpy.set_message(f"Background task {step} completed")

    hardpy.set_message("Long operation completed")
    hardpy.set_case_artifact(
        {"total_steps": total_steps, "average_step_time": "2s", "result": "SUCCESS"}
    )


@pytest.mark.critical
@pytest.mark.case_name("Hardware Components Simulation")
def test_hardware_simulation():
    """Simulation of hardware components operation"""
    for i in range(100):
        sensor_value = random.uniform(40, 60)
        hardpy.set_message(f"temperature_{i}: {sensor_value:.1f}°C")

    sensors = {
        "temperature": [random.uniform(40, 60) for _ in range(100)],
        "voltage": [random.uniform(11.5, 12.5) for _ in range(100)],
        "current": [random.uniform(0.2, 0.3) for _ in range(100)],
        "fan_speed": [random.randint(2000, 2500) for _ in range(100)],
    }

    hardpy.set_message("All readings within normal range")
    hardpy.set_case_artifact(sensors)
