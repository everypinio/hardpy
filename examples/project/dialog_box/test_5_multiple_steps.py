import pytest
from hardpy import run_dialog_box
from hardpy.pytest_hardpy.utils.dialog_box import (
    DialogBox,
    MultistepWidget,
)


@pytest.mark.case_name("Multistep")
def test_multiple_steps():
    dbx = DialogBox(
        dialog_text="Follow the steps and click Confirm",
        widget=MultistepWidget(fields=["Read first instruction", "Read second instruction", "Read third instruction"]),
    )
    response = run_dialog_box(dbx)
    assert response is None
