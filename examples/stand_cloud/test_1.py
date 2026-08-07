from uuid import uuid4

import pytest

import jig

pytestmark = pytest.mark.module_name("Testing preparation")


@pytest.mark.case_name("Process info")
def test_process_info():
    jig.set_process_name("Acceptance Test")
    jig.set_process_number(1)

    process_info = {"stage": "production", "version": "1.0"}
    jig.set_process_info(process_info)


@pytest.mark.case_name("Batch info")
def test_batch_info():
    jig.set_batch_serial_number("batch_1")


@pytest.mark.case_name("DUT info")
def test_dut_info():
    serial_number = str(uuid4())[:6]
    jig.set_dut_serial_number(serial_number)
    jig.set_dut_part_number("part_number_1")
    jig.set_dut_name("Test Device")
    jig.set_dut_type("PCBA")
    jig.set_dut_revision("REV1.0")

    info = {"sw_version": "1.0.0"}
    jig.set_dut_info(info)


@pytest.mark.case_name("Sub unit info")
def test_sub_unit_info():
    jig.set_dut_sub_unit(
        jig.SubUnit(
            serial_number=str(uuid4())[:6],
            part_number="part_number_1",
            type="PCBA",
            revision="REV2.0",
        ),
    )


@pytest.mark.case_name("Test stand info")
def test_stand_info():
    test_stand_name = "Stand 1"
    jig.set_stand_name(test_stand_name)
    jig.set_stand_location("Moon")
    jig.set_stand_number(2)
    jig.set_stand_revision("HW1.0")

    stand_info = {
        "some_info": "123",
        "release": "1.0.0",
        "calibration_due": "2023-12-31",
    }
    jig.set_stand_info(stand_info)
    jig.set_message(f"Stand name: {test_stand_name}")
    assert True
