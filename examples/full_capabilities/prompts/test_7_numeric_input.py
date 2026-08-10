"""Numeric input dialog."""

import pytest

from jig import DialogBox, NumericInputWidget, run_dialog_box, set_case_artifact

pytestmark = pytest.mark.module_name("Numeric input")


@pytest.mark.case_name("Numeric input")
def test_numeric_input():
    """Dialog that collects a number from the operator."""
    value = run_dialog_box(
        DialogBox(
            title_bar="Counter reading",
            dialog_text="Enter the cycle counter value shown on the fixture.",
            widget=NumericInputWidget(),
        )
    )
    set_case_artifact({"cycles": value})
    assert isinstance(value, (int, float)), "Enter a number"
