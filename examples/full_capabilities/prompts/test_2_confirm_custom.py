"""Confirm dialog with a custom button label."""

import pytest

from jig import DialogBox, run_dialog_box

pytestmark = pytest.mark.module_name("Confirm custom label")


@pytest.mark.case_name("Custom confirm")
def test_confirm_custom_label():
    """Confirm dialog whose single button uses a custom label."""
    assert run_dialog_box(
        DialogBox(
            title_bar="Custom confirm",
            dialog_text="Press Ready when the fixture is loaded.",
            button_text=["Ready"],
        )
    )
