import logging
from uuid import uuid4

import pytest
import hardpy
from hardpy.pytest_hardpy.pytest_call import (
    DialogBoxData,
    DialogBoxWidget,
    DialogBoxWidgetType,
)


pytestmark = pytest.mark.module_name("Testing preparation")


@pytest.mark.case_name("DUT info")
def test_dut_info(module_log: logging.Logger):
    serial_number = str(uuid4())[:6]
    module_log.info(f"DUT serial number {serial_number}")
    hardpy.set_dut_serial_number(serial_number)
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
    info = {
        "name": "Test stand 1",
    }
    hardpy.set_stand_info(info)
    assert True


def test_1_dialog_box():
    info = DialogBoxData(
        title_bar="Dialog box title",
        dialog_text="Doalog box text",
        widget_info=DialogBoxWidget(
            widget_info={"text": "Text"}, widget_type=DialogBoxWidgetType.CHECKBOX
        ),
    )
    response = hardpy.run_dialog_box(info)
    assert response == "ok"
