import pytest

from hardpy import (
    run_dialog_box,
    set_message,
    TextInputWidget,
    NumericInputWidget,
    DialogBox,
)

pytestmark = pytest.mark.module_name("Input field dialog boxes")


@pytest.mark.case_name("Text input")
def test_text_input():
    dbx = DialogBox(
        dialog_text="Type 'ok' and press the Confirm button",
        title_bar="Example of text input",
        widget=TextInputWidget(),
    )
    response = run_dialog_box(dbx)
    set_message(f"Entered text {response}")
    assert response == "ok", "The entered text is not correct"


@pytest.mark.case_name("Numeric input")
def test_num_input():

    test_num = 123
    dbx = DialogBox(
        dialog_text=f"Enter the number {test_num} and press the Confirm button",
        title_bar="Example of entering a number",
        widget=NumericInputWidget(),
    )
    response = int(run_dialog_box(dbx))
    set_message(f"Entered number {response}")
    assert response == test_num, "The entered number is not correct"
