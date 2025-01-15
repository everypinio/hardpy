import pytest

import hardpy
from hardpy import DialogBox, run_dialog_box, set_message


@pytest.mark.attempt(15)
@pytest.mark.case_name("Text input")
def test_text_input():
    dbx = DialogBox(
        dialog_text="Text",
        title_bar="Text",
    )
    response = run_dialog_box(dbx)
    set_message(f"Entered text {response}")
    assert False