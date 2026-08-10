"""Confirm dialog with a reference image."""

import pytest

from jig import DialogBox, ImageComponent, run_dialog_box

pytestmark = pytest.mark.module_name("Confirm with image")


@pytest.mark.case_name("Confirm with image")
def test_confirm_with_image():
    """Confirm dialog that shows a reference picture."""
    assert run_dialog_box(
        DialogBox(
            title_bar="Reference picture",
            dialog_text="Compare the board with the picture, then confirm.",
            image=ImageComponent(address="assets/test.png", width=50),
        )
    )
