import pytest

from hardpy import (
    DialogBox,
    TextInputWidget,
    run_dialog_box,
    set_message,
)

pytestmark = pytest.mark.module_name("Input field dialog boxes")


# @pytest.mark.attempt(5)
# @pytest.mark.case_name("Text input")
# def test_text_input():s
#     dbx = DialogBox(
#         dialog_text="Type 'ok' and press the Confirm button",
#         title_bar="Example of text input",
#         widget=TextInputWidget(),
#     )
#     response = run_dialog_box(dbx)
#     set_message(f"Entered text {response}")
#     assert response == "ok", "The entered text is not correct"
