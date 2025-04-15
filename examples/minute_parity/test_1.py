import logging
from uuid import uuid4

import pytest

import hardpy

pytestmark = pytest.mark.module_name("Testing preparation")


@pytest.mark.case_name("DUT info")
def test_dut_info(module_log: logging.Logger):
    serial_number = str(uuid4())[:6]
    module_log.info(f"DUT serial number {serial_number}")
    hardpy.set_dut_serial_number(serial_number)
    hardpy.set_dut_part_number("part_number_1")
    info = {
        "batch": "test_batch",
        "board_rev": "rev_1",
    }
    hardpy.set_dut_info(info)
    assert True


@pytest.mark.case_name("Test stand info")
def test_stand_info(module_log: logging.Logger):
    test_stand_name = "Stand 1"
    module_log.info(f"Stand name: {test_stand_name}")
    hardpy.set_stand_name(test_stand_name)
    hardpy.set_stand_location("Moon")
    info = {
        "some_info": "123",
        "stand_id": "ST-001",
        "operator": "John Doe",
        "temperature": "23.5°C",
        "humidity": "45% RH",
        "pressure": "101.3 kPa",
        "voltage": "220 VAC",
        "current": "5 A",
        "firmware_version": "1.2.3",
        "serial_number": "SN-123456",
        "test_duration": "2 hours",
        "power_rating": "1.1 kW",
        "manufacturer": "SpaceTech Inc.",
        "model": "X-2000",
        "ip_address": "192.168.1.100",
        "mac_address": "00:1A:2B:3C:4D:5E",
        "last_calibration": "2023-11-15",
        "next_calibration": "2024-11-15",
        "safety_class": "Class A",
        "operating_mode": "Automatic",
        "battery_status": "85%",
        "connection_type": "Ethernet"
    }
    hardpy.set_stand_info(info)
    assert True
