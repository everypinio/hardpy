from time import sleep

import pytest
import hardpy
from hardpy import DialogBoxData, DialogBoxWidget, DialogBoxWidgetType
from hardpy.pytest_hardpy.utils import NodeInfo

pytestmark = [
    pytest.mark.module_name("End of testing"),
    pytest.mark.dependency("test_2::test_minute_parity"),
]


@pytest.mark.case_name("Final case")
def test_one():
    for i in range(5, 0, -1):
        hardpy.set_message(f"Time left until testing ends {i} s", "updated_status")
        sleep(1)
    hardpy.set_message("Testing ended", "updated_status")
    assert True


@pytest.mark.case_name("Test dialog box")
def test_1_dialog_box():
    info = DialogBoxData(
        title_bar="Second dialog box",
        dialog_text="Enjoy the finished dialog box again",
        widget_info=DialogBoxWidget(
            widget_info={"text": "Text"}, widget_type=DialogBoxWidgetType.CHECKBOX
        ),
    )
    response = hardpy.run_dialog_box(info)
    assert response == "ok"
