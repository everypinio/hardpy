"""Text input dialog."""

import pytest

from jig import DialogBox, TextInputWidget, run_dialog_box, set_case_artifact

pytestmark = pytest.mark.module_name("Text input")


@pytest.mark.case_name("Text input")
def test_text_input():
    """Dialog that collects a free-form string from the operator."""
    value = run_dialog_box(
        DialogBox(
            title_bar="Operator note",
            dialog_text="Type any short note about the unit.",
            widget=TextInputWidget(),
        )
    )
    set_case_artifact({"note": value})
    assert isinstance(value, str) and value.strip(), "Enter a non-empty note"
