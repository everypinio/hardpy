"""Base confirm dialog."""

import pytest

from jig import DialogBox, run_dialog_box

pytestmark = pytest.mark.module_name("Confirm")


@pytest.mark.case_name("Confirm")
def test_confirm():
    """Plain confirm dialog with the default Confirm button."""
    assert run_dialog_box(
        DialogBox(
            title_bar="Confirm",
            dialog_text="Press Confirm to continue.",
        )
    )
