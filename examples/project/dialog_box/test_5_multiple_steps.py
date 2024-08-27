import pytest

from hardpy import run_dialog_box
from hardpy.pytest_hardpy.utils.dialog_box import (
    DialogBox,
    MultistepWidget,
    ImageWidget,
    StepWidget,
)

pytestmark = pytest.mark.module_name("Multiple steps dialog box")


@pytest.mark.case_name("Multistep")
def test_multiple_steps():
    steps = [
        StepWidget("Step 1", text="Content for step", widget=None),
        StepWidget(
            "Step 2",
            text="Content for step 2",
            widget=ImageWidget(address="assets/test.png"),
        ),
        StepWidget("Step 3", text=None, widget=ImageWidget(address="assets/test.png")),
    ]
    dbx = DialogBox(
        dialog_text="Follow the steps and click Confirm",
        widget=MultistepWidget(steps),
    )
    response = run_dialog_box(dbx)
    assert response
