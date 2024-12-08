import pytest

from hardpy import (
    DialogBox,
    ImageComponent,
    MultistepWidget,
    StepWidget,
    run_dialog_box,
)

pytestmark = pytest.mark.module_name("Multiple steps dialog box")


@pytest.mark.case_name("Multistep")
def test_multiple_steps():
    steps = [
        StepWidget("Step 1", text="Content for step"),
        StepWidget(
            "Step 2",
            text="Content for step 2",
            image=ImageComponent(address="assets/image.png", width=100),
        ),
        StepWidget(
            "Step 3",
            text=None,
            image=ImageComponent(address="assets/test.png", width=50),
        ),
    ]
    dbx = DialogBox(
        dialog_text="Follow the steps and click Confirm",
        widget=MultistepWidget(steps),
    )
    response = run_dialog_box(dbx)
    assert response
