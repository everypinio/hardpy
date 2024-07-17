import pytest

import hardpy


@pytest.mark.case_name("Test base dialog box")
def test_base_dialog_box():
    info = hardpy.dialog_box.DialogBoxData(
        title_bar="Operator check",
        dialog_text="If you are not sleeping, press the Confirm button",
    )
    response = hardpy.run_dialog_box(info)
    assert response is None 


@pytest.mark.case_name("Test dialog box with text input")
def test_dialog_box_with_text_input():
    widget = hardpy.dialog_box.DialogBoxWidget(
        type=hardpy.dialog_box.DialogBoxWidgetType.TEXT_INPUT,
        info={"text": "Some text"},
    )

    info = hardpy.dialog_box.DialogBoxData(
        dialog_text="Type 'ok' and press the Confirm button",
        title_bar="Example of text input",
        widget=widget,
    )
    response = hardpy.run_dialog_box(info)
    assert response == "ok"


@pytest.mark.case_name("Test dialog box with num input")
def test_dialog_box_with_num_input():
    TEST_NUM = 123
    widget = hardpy.dialog_box.DialogBoxWidget(
        type=hardpy.dialog_box.DialogBoxWidgetType.NUMERIC_INPUT,
        info={"text": "Enter the number"},
    )

    info = hardpy.dialog_box.DialogBoxData(
        dialog_text=f"Enter the number {TEST_NUM} and press the Confirm button",
        title_bar="Example of entering a number",
        widget=widget,
    )
    response = int(hardpy.run_dialog_box(info))
    assert response == TEST_NUM
