import pytest

from hardpy import (
    DialogBox,
    NumericInputWidget,
    TextInputWidget,
    run_dialog_box,
    set_message,
)
from hardpy.pytest_hardpy.utils.dialog_box import ImageWidget

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


@pytest.mark.case_name("Text input with image")
def test_text_input_with_image():
    dbx = DialogBox(
        dialog_text="Type 'ok' and press the Confirm button",
        title_bar="Example of text input",
        widget=TextInputWidget(),
        image=ImageWidget(address="assets/test.png", width=50, border=0),
    )
    response = run_dialog_box(dbx)
    set_message(f"Entered text {response}")
    assert response == "ok", "The entered text is not correct"


@pytest.mark.case_name("Numeric input with image")
def test_num_input_with_image():
    test_num = 123
    dbx = DialogBox(
        dialog_text=f"Enter the number {test_num} and press the Confirm button",
        title_bar="Example of entering a number",
        widget=NumericInputWidget(),
        image=ImageWidget(address="assets/test.png", width=50, border=1),
    )
    response = int(run_dialog_box(dbx))
    set_message(f"Entered number {response}")
    assert response == test_num, "The entered number is not correct"