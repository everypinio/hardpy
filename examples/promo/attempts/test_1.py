from time import sleep

import pytest

import hardpy
from hardpy import DialogBox, TextInputWidget, run_dialog_box

pytestmark = pytest.mark.module_name("Production Testing")


@pytest.mark.attempt(3)
def test_operator_confirmation():
    dbx = DialogBox(
        dialog_text="Enter 'PASS' to confirm successful equipment testing",
        title_bar="Operator Confirmation",
        widget=TextInputWidget(),
    )
    response = run_dialog_box(dbx)
    if response != "PASS":
        dbx = DialogBox(
            dialog_text=f"Failed attempt {hardpy.get_current_attempt()}/3. Check the equipment and repeat the test.",
            title_bar="Testing Status",
        )
        run_dialog_box(dbx)

    assert response == "PASS", "Operator did not confirm successful equipment testing"
