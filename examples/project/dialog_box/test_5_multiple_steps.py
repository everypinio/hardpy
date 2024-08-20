import pytest
from hardpy import run_dialog_box
from hardpy.pytest_hardpy.utils.dialog_box import (
    DialogBox,
    MultistepWidget,
)

pytestmark = pytest.mark.module_name("Multiple steps dialog box")

@pytest.mark.case_name("Multistep")
def test_multiple_steps():
    steps = [
        {"title": "Read 1", "content": "Content for step"},
        {"title": "Read 2", "content": "Content for step"},
        {"title": "Read 3", "content": "Content for step"},
    ]
    dbx = DialogBox(
        dialog_text="Follow the steps and click Confirm",
        widget=MultistepWidget(steps),
    )
    response = run_dialog_box(dbx)
    assert response is None
