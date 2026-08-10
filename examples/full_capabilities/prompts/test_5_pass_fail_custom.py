"""Pass / Fail dialog with custom button labels."""

import pytest

from jig import DialogBox, run_dialog_box

pytestmark = pytest.mark.module_name("Pass / Fail custom labels")


@pytest.mark.case_name("Custom pass fail")
def test_pass_fail_custom_labels():
    """Pass/Fail dialog whose buttons use custom labels."""
    response = run_dialog_box(
        DialogBox(
            title_bar="Assembly check",
            dialog_text="Is the shield installed?",
            pass_fail=True,
            button_text=["Installed", "Missing"],
        )
    )
    assert response.result, "The operator reported the shield as missing"
