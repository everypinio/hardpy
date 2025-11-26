from time import sleep

import pytest

import hardpy
from hardpy import DialogBox, TextInputWidget, run_dialog_box

pytestmark = pytest.mark.module_name("Attempts")

@pytest.mark.attempt(3)
def test_dialog_box():
    dbx = DialogBox(
        dialog_text="Print 'ok', if you want to pass attempt.",
        title_bar="Example of text input",
        widget=TextInputWidget(),
    )
    response = run_dialog_box(dbx)
    if response != "ok":
        dbx = DialogBox(
            dialog_text=f"Test attempt {hardpy.get_current_attempt()}",
            title_bar="Attempt message",
        )
        run_dialog_box(dbx)

    assert response == "ok", "The entered text is not correct"
