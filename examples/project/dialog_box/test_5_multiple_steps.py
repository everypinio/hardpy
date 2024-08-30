import pytest

from hardpy import run_dialog_box, DialogBox, ImageWidget, StepWidget, MultistepWidget

pytestmark = pytest.mark.module_name("Multiple steps dialog box")


# @pytest.mark.case_name("Multistep")
# def test_multiple_steps():
#     img_widget = ImageWidget(address="assets/test.png", width=50)
#     steps = [
#         StepWidget("Step 1", text="Content for step", widget=None),
#         StepWidget("Step 2", text="Content for step 2", widget=img_widget),
#         StepWidget("Step 3", text=None, widget=img_widget),
#     ]
#     dbx = DialogBox(
#         dialog_text="Follow the steps and click Confirm",
#         widget=MultistepWidget(steps),
#     )
#     response = run_dialog_box(dbx)
#     assert response
