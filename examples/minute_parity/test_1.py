from uuid import uuid4

import pytest

import hardpy

pytestmark = pytest.mark.module_name("Testing preparation")


@pytest.mark.case_name("Process info")
def test_process_info():
    hardpy.set_process_name("Acceptance Test")
    hardpy.set_process_number(1)

    process_info = {"stage": "production", "version": "1.0"}
    hardpy.set_process_info(process_info)


@pytest.mark.case_name("Batch info")
def test_batch_info():
    hardpy.set_batch_serial_number("batch_1")


@pytest.mark.case_name("DUT info")
def test_dut_info():
    serial_number = str(uuid4())[:6]
    hardpy.set_dut_serial_number(serial_number)
    hardpy.set_message(f"Serial number: {serial_number}")
    hardpy.set_dut_part_number("part_number_1")
    hardpy.set_dut_name("Test Device")
    hardpy.set_dut_type("PCBA")
    hardpy.set_dut_revision("REV1.0")

    info = {"sw_version": "1.0.0"}
    hardpy.set_dut_info(info)


@pytest.mark.case_name("Sub unit info")
def test_sub_unit_info():
    hardpy.set_dut_sub_unit(
        hardpy.SubUnit(
            serial_number=str(uuid4())[:6],
            part_number="part_number_1",
            type="PCBA",
            revision="REV2.0",
        ),
    )


@pytest.mark.case_name("Test stand info")
def test_stand_info():
    # Set test stand information
    test_stand_name = "Stand 1"
    hardpy.set_stand_name(test_stand_name)
    hardpy.set_stand_location("Moon")
    hardpy.set_stand_number(2)

    hardpy.set_stand_revision("HW1.0")

    stand_info = {
        "some_info": "123",
        "release": "1.0.0",
    }
    hardpy.set_stand_info(stand_info)
