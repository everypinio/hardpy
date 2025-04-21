from uuid import uuid4

import pytest

import hardpy

pytestmark = pytest.mark.module_name("Testing preparation")


@pytest.mark.case_name("DUT info")
def test_dut_info():
    serial_number = str(uuid4())[:6]
    hardpy.set_dut_serial_number(serial_number)
    hardpy.set_dut_part_number("part_number_1")
    info = {
        "batch": "test_batch",
        "board_rev": "rev_1",
    }
    hardpy.set_dut_info(info)
    assert True


@pytest.mark.case_name("Test stand info")
def test_stand_info():
    test_stand_name = "Stand 1"
    hardpy.set_stand_name(test_stand_name)
    hardpy.set_stand_location("Moon")
    info = {
        "some_info": "123",
        "release": "1.0.0",
    }
    hardpy.set_stand_info(info)
    assert True
