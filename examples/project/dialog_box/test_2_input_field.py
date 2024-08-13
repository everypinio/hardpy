import pytest
import requests

from hardpy import run_dialog_box, set_message
from hardpy.pytest_hardpy.utils.dialog_box import (
    DialogBoxWidget,
    DialogBoxWidgetType,
    DialogBox,
)


pytestmark = pytest.mark.module_name("Input field dialog boxes")


@pytest.mark.case_name("Text input")
def test_text_input():
    dbx = DialogBox(
        dialog_text="Type 'ok' and press the Confirm button",
        title_bar="Example of text input",
        widget=DialogBoxWidget(DialogBoxWidgetType.TEXT_INPUT),
    )
    response = run_dialog_box(dbx)
    set_message(f"Entered text {response}")
    assert response == "ok", "The entered text is not correct"


@pytest.mark.case_name("Numeric input")
def test_num_input():
    TEST_NUM = 123
    dbx = DialogBox(
        dialog_text=f"Enter the number {TEST_NUM} and press the Confirm button",
        title_bar="Example of entering a number",
        widget=DialogBoxWidget(DialogBoxWidgetType.NUMERIC_INPUT),
    )
    response = int(run_dialog_box(dbx))
    set_message(f"Entered number {response}")
    assert response == TEST_NUM, "The entered number is not correct"



