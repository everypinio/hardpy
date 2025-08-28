import hardpy
import pytest
import time

pytestmark = pytest.mark.module_name("Logging Demonstration Module")


@pytest.mark.case_name("Debug Messages Demonstration")
def test_debug_messages():
    """Test generates various debug messages"""
    hardpy.set_message("Starting debug messages demonstration")

    for i in range(1, 6):
        hardpy.set_message(f"Iteration {i}/5: Checking subsystem {i}")

        # Simulate different log levels
        if i == 2:
            hardpy.set_message("WARN: Temporary performance delays detected")
        elif i == 4:
            hardpy.set_message("ERROR: Sensor malfunction detected")

    hardpy.set_message("Demonstration completed successfully")
    hardpy.set_case_artifact({"iterations": 5, "status": "completed"})


@pytest.mark.critical
@pytest.mark.case_name("Detailed System Verification")
def test_detailed_logs():
    """Test with detailed system operation logging"""
    hardpy.set_message("Initializing system verification")
    time.sleep(0.5)

    # Simulate working with different components
    components = ["CPU", "Memory", "Network Interface", "Storage Subsystem"]

    for component in components:
        hardpy.set_message(f"Testing component: {component}")
        time.sleep(0.3)

        # Simulate sensor readings
        if component == "CPU":
            hardpy.set_message("Processor temperature: 65°C")
        elif component == "Memory":
            hardpy.set_message("Memory usage: 3.2/8.0 GB")

    hardpy.set_message("All components operating within normal parameters")
    hardpy.set_case_artifact(
        {"checked_components": components, "result": "PASS", "timestamp": time.time()}
    )


@pytest.mark.case_name("Long Operation Simulation")
def test_long_operation():
    """Test with long-running operation and periodic logging"""
    total_steps = 10
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
    hardpy.set_message("Initializing hardware test")

    # Simulate sensor readings
    sensors = {"temperature": 45.6, "voltage": 12.3, "current": 0.25, "fan_speed": 2400}

    for sensor_name, value in sensors.items():
        hardpy.set_message(f"{sensor_name}: {value}")
        time.sleep(0.2)

    hardpy.set_message("All readings within normal range")
    hardpy.set_case_artifact(sensors)
