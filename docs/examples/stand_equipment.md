# Stand equipment example

This example demonstrates how to document test bench equipment using the `set_instrument()` function in pytest-hardpy.
The example shows how to record instruments that are part of the test setup.

### How to start

1. Launch `hardpy init test_stand_equipment`.
2. Launch [CouchDH instance](../documentation/database.md#couchdb-instance).
3. Launch `hardpy run test_stand_equipment`.

### Description

The `set_instrument()` function allows documenting all equipment that forms part of the test bench setup.
This information is stored in the database.
Information about using of the function [set_instrument](https://github.com/everypinio/hardpy/tree/main/documentation/pytest_hadpy#set_instrument)

### Example implementation

```python
import pytest
import hardpy
from datetime import datetime

pytestmark = pytest.mark.module_name("Stand equipment")

@pytest.mark.case_name("Power Supply Setup")
def test_power_supply():
    """Document the power supply used in testing"""
    hardpy.set_instrument(
        name="DC Power Supply",
        revision="2.1",
        number=1,
        comment="Main system power source",
        info={
            "model": "PSU-3000",
            "voltage_range": "0-30V",
            "current_range": "0-5A",
            "calibration_date": datetime(2023, 6, 15).isoformat()
        }
    )
    assert True

@pytest.mark.case_name("Measurement Equipment")
def test_measurement_devices():
    """Document measurement equipment on the test bench"""
    # Multimeter
    hardpy.set_instrument(
        name="Digital Multimeter",
        revision="1.3",
        number=2,
        info={
            "model": "DMM-4040",
            "accuracy": "0.1%",
            "channels": 4
        }
    )
    
    # Oscilloscope
    hardpy.set_instrument(
        name="Oscilloscope",
        revision="3.2",
        number=3,
        info={
            "model": "DSO-X 2024A",
            "bandwidth": "200MHz",
            "sample_rate": "2GSa/s"
        }
    )
    assert True

@pytest.mark.case_name("Environmental Controls")
def test_environmental_controls():
    """Document environmental control equipment"""
    hardpy.set_instrument(
        name="Temperature Chamber",
        revision="4.0",
        number=4,
        comment="Used for thermal testing",
        info={
            "temperature_range": "-40°C to +150°C",
            "humidity_range": "10% to 98% RH"
        }
    )
    assert True
```
