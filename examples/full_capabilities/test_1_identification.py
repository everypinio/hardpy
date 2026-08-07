"""Identification of the stand, the device under test and the production process."""

import pytest
from simulated_device import SimulatedDevice  # type: ignore[import-not-found]

from hardpy import (
    ComparisonOperation as CompOp,
    Group,
    Instrument,
    StringMeasurement,
    SubUnit,
    set_batch_serial_number,
    set_case_measurement,
    set_dut_info,
    set_dut_name,
    set_dut_part_number,
    set_dut_revision,
    set_dut_serial_number,
    set_dut_sub_unit,
    set_dut_type,
    set_instrument,
    set_message,
    set_process_info,
    set_process_name,
    set_process_number,
    set_stand_info,
    set_stand_location,
    set_stand_name,
    set_stand_number,
    set_stand_revision,
    set_user_name,
)

pytestmark = [
    pytest.mark.module_name("Identification"),
    pytest.mark.module_group(Group.SETUP),
]

EXPECTED_FIRMWARE_VERSION = "1.4.2"


@pytest.mark.case_name("Test stand")
def test_stand_identification():
    set_stand_name("Full capabilities bench")
    set_stand_number(1)
    set_stand_revision("rev_2")
    set_stand_location("Quebec, lab 2")
    set_stand_info({"maintainer": "test engineering", "shift": 1})

    set_instrument(
        Instrument(
            name="Power supply",
            part_number="PSU-3010",
            serial_number="PSU-000045",
            revision="rev_1",
            number=1,
            comment="Feeds the device under test",
            info={"channels": 2, "max_voltage": 30},
        ),
    )
    set_instrument(
        Instrument(
            name="Multimeter",
            part_number="DMM-7510",
            serial_number="DMM-000198",
            number=2,
        ),
    )


@pytest.mark.case_name("Device under test")
def test_dut_identification(device: SimulatedDevice):
    set_dut_name("Sensor board")
    set_dut_type("sensor_board")
    set_dut_serial_number(device.serial_number)
    set_dut_part_number("PN-4471")
    set_dut_revision("rev_3")
    set_dut_info({"assembly_line": "A", "hardware_variant": "wide range"})

    set_dut_sub_unit(
        SubUnit(
            name="Radio module",
            type="radio",
            serial_number="RM-000771",
            part_number="PN-1120",
            revision="rev_1",
        ),
    )
    set_dut_sub_unit(SubUnit(name="Sensor head", type="sensor", revision="rev_4"))


@pytest.mark.critical
@pytest.mark.case_name("Firmware version")
def test_firmware_version(device: SimulatedDevice):
    """Read the firmware version.

    The `critical` marker skips every remaining test when this one fails,
    since nothing can be trusted on an unknown firmware.
    """
    version = device.read_firmware_version()
    set_message(f"Device reports firmware {version}")

    measurement = StringMeasurement(
        name="Firmware version",
        value=version,
        operation=CompOp.EQ,
        comparison_value=EXPECTED_FIRMWARE_VERSION,
    )
    set_case_measurement(measurement)

    assert measurement.result, f"Expected firmware {EXPECTED_FIRMWARE_VERSION}"


@pytest.mark.case_name("Production process")
def test_process_identification():
    set_user_name("operator_1")
    set_batch_serial_number("BATCH-2026-07")
    set_process_name("Final test")
    set_process_number(3)
    set_process_info({"work_order": "WO-88213", "station": "FT-02"})
