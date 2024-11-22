import pytest

from hardpy import (
    BaseWidget,
    DialogBox,
    ImageComponent,
    MultistepWidget,
    StepWidget,
    run_dialog_box,
)

pytestmark = pytest.mark.module_name("Multiple steps dialog box")


@pytest.mark.case_name("Multistep")
def test_multiple_steps():
    base_widget = BaseWidget(image = ImageComponent(address="assets/test.png", width=50))  # noqa: E501
    steps = [
        StepWidget("Step 1", text="Content for step", widget=None),
        StepWidget("Step 2", text="Content for step 2", widget=base_widget),
        StepWidget("Step 3", text=None, widget=base_widget),
    ]
    dbx = DialogBox(
        dialog_text="Follow the steps and click Confirm",
        widget=MultistepWidget(steps),
    )
    response = run_dialog_box(dbx)
    assert response
