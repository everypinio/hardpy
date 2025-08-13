from datetime import datetime
from uuid import uuid4

import pytest

import hardpy

pytestmark = pytest.mark.module_name("Testing preparation")


@pytest.mark.case_name("DUT info")
def test_dut_info():
    serial_number = str(uuid4())[:6]
    hardpy.set_dut_serial_number(serial_number)
    hardpy.set_dut_part_number("part_number_1")

    hardpy.set_dut_name("Test Device")
    with pytest.raises(hardpy.DuplicateDutNameError):
        hardpy.set_dut_name("Another Device")

    hardpy.set_dut_type("PCBA")
    with pytest.raises(hardpy.DuplicateDutTypeError):
        hardpy.set_dut_type("Module")

    hardpy.set_dut_revision("REV1.0")
    with pytest.raises(hardpy.DuplicateDutRevisionError):
        hardpy.set_dut_revision("REV2.0")

    info = {
        "batch": "test_batch",
        "board_rev": "rev_1",
        "manufacture_date": datetime.now().date().isoformat(),
    }
    hardpy.set_dut_info(info)
    hardpy.set_message(f"Serial number: {serial_number}")
    hardpy.set_message("Part number: part_number_1")
    hardpy.set_message(f"Device type: PCBA, Revision: REV1.0")
    assert True


@pytest.mark.case_name("Test stand info")
def test_stand_info():
    test_stand_name = "Stand 1"
    hardpy.set_stand_name(test_stand_name)
    hardpy.set_stand_location("Moon")
    hardpy.set_stand_number(2)

    hardpy.set_stand_revision("HW1.0")
    with pytest.raises(hardpy.DuplicateStandRevisionError):
        hardpy.set_stand_revision("HW2.0")

    hardpy.set_process_name("Acceptance Test")
    with pytest.raises(hardpy.DuplicateProcessNameError):
        hardpy.set_process_name("Production Test")

    hardpy.set_process_number(1)
    with pytest.raises(hardpy.DuplicateProcessNumberError):
        hardpy.set_process_number(2)

    process_info = {
        "stage": "production",
        "version": "1.0",
        "started_at": datetime.now().isoformat(),
    }
    hardpy.set_process_info(process_info)

    stand_info = {
        "some_info": "123",
        "release": "1.0.0",
        "calibration_due": "2023-12-31",
    }
    hardpy.set_stand_info(stand_info)
    hardpy.set_message(f"Stand name: {test_stand_name}")
    hardpy.set_message(f"Process: Acceptance Test #1")
    assert True
