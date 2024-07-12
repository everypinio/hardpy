import pytest
import hardpy
from hardpy import DialogBoxData, DialogBoxWidget, DialogBoxWidgetType


@pytest.mark.case_name("Test base dialog box")
def test_base_dialog_box():
    info = DialogBoxData(
        title_bar="Operator check",
        dialog_text="If you are not sleeping, press the Confirm button",
        widget_info=None,
    )
    response = hardpy.run_dialog_box(info)
    assert response == "ok"


@pytest.mark.case_name("Test dialog box with text input")
def test_dialog_box_with_text_input():
    info = DialogBoxData(
        title_bar="Example of text input",
        dialog_text="Type some text and press the Confirm button",
        widget_info=DialogBoxWidget(
            widget_type=DialogBoxWidgetType.TEXT_INPUT,
            widget_info={"text": "some text"},
        ),
    )
    response = hardpy.run_dialog_box(info)
    assert response == "ok"


@pytest.mark.case_name("Test dialog box with num input")
def test_dialog_box_with_num_input():
    info = DialogBoxData(
        title_bar="Example of entering a number",
        dialog_text="Enter the number 5 and press the Confirm button",
        widget_info=DialogBoxWidget(
            widget_type=DialogBoxWidgetType.NUMERIC_INPUT,
            widget_info={"text": "enter the number"},
        ),
    )
    response = hardpy.run_dialog_box(info)
    assert response == "ok"
