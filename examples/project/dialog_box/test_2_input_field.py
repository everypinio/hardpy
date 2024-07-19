import pytest

from hardpy import dialog_box, run_dialog_box, set_message


pytestmark = pytest.mark.module_name("Input field dialog boxes")


@pytest.mark.case_name("Text input")
def test_text_input():
    widget = dialog_box.DialogBoxWidget(
        type=dialog_box.DialogBoxWidgetType.TEXT_INPUT,
        info={"text": "Some text"},
    )

    dbx = dialog_box.DialogBoxData(
        dialog_text="Type 'ok' and press the Confirm button",
        title_bar="Example of text input",
        widget=widget,
    )
    response = run_dialog_box(dbx)
    set_message(f"Entered text {response}")
    assert response == "ok", "The entered text is not correct"


@pytest.mark.case_name("Numeric input")
def test_num_input():
    TEST_NUM = 123
    widget = dialog_box.DialogBoxWidget(
        type=dialog_box.DialogBoxWidgetType.NUMERIC_INPUT,
        info={"text": "Enter the number"},
    )

    dbx = dialog_box.DialogBoxData(
        dialog_text=f"Enter the number {TEST_NUM} and press the Confirm button",
        title_bar="Example of entering a number",
        widget=widget,
    )
    response = int(run_dialog_box(dbx))
    set_message(f"Entered number {response}")
    assert response == TEST_NUM, "The entered number is not correct"
