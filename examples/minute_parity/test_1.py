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
    info = {
        "geo": "Moon",
    }
    hardpy.set_stand_info(info)
    assert True
