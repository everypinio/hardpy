import pytest

import hardpy


@pytest.mark.case_name("Test base dialog box")
def test_base_dialog_box():
    info = hardpy.dialog_box.DialogBoxData(
        title_bar="Operator check",
        dialog_text="If you are not sleeping, press the Confirm button",
        widget_info=None,
    )
    response = hardpy.run_dialog_box(info)
    assert response == None


@pytest.mark.case_name("Test dialog box with text input")
def test_dialog_box_with_text_input():
    info = hardpy.dialog_box.DialogBoxData(
        dialog_text="Type 'ok' and press the Confirm button",
        title_bar="Example of text input",
        widget_info=hardpy.dialog_box.DialogBoxWidget(
            widget_type=hardpy.dialog_box.DialogBoxWidgetType.TEXT_INPUT,
            widget_info={"text": "Some text"},
        ),
    )
    response = hardpy.run_dialog_box(info)
    assert response == "ok"


@pytest.mark.case_name("Test dialog box with num input")
def test_dialog_box_with_num_input():
    info = hardpy.dialog_box.DialogBoxData(
        dialog_text="Enter the number 123 and press the Confirm button",
        title_bar="Example of entering a number",
        widget_info=hardpy.dialog_box.DialogBoxWidget(
            widget_type=hardpy.dialog_box.DialogBoxWidgetType.NUMERIC_INPUT,
            widget_info={"text": "Enter the number"},
        ),
    )
    response = hardpy.run_dialog_box(info)
    assert response == 123.0
