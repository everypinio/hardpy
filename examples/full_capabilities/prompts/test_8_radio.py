"""Radio-button choice dialog."""

import pytest

from jig import DialogBox, RadiobuttonWidget, run_dialog_box, set_case_artifact

pytestmark = pytest.mark.module_name("Radio")


@pytest.mark.case_name("Radio choice")
def test_radio():
    """Dialog that lets the operator pick exactly one option."""
    choice = run_dialog_box(
        DialogBox(
            title_bar="Revision",
            dialog_text="Select the board revision.",
            widget=RadiobuttonWidget(fields=["A", "B", "C"]),
        )
    )
    set_case_artifact({"revision": choice})
    assert choice in {"A", "B", "C"}
