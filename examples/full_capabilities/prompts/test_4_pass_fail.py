"""Pass / Fail dialog."""

import pytest

from jig import DialogBox, run_dialog_box

pytestmark = pytest.mark.module_name("Pass / Fail")


@pytest.mark.case_name("Pass or fail")
def test_pass_fail():
    """Dialog with Pass and Fail buttons."""
    response = run_dialog_box(
        DialogBox(
            title_bar="Visual check",
            dialog_text="Does the board look correct?",
            pass_fail=True,
        )
    )
    assert response.result, "The operator pressed Fail"
