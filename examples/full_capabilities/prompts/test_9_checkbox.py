"""Checkbox multi-select dialog."""

import pytest

from jig import CheckboxWidget, DialogBox, run_dialog_box, set_case_artifact

pytestmark = pytest.mark.module_name("Checkbox")


@pytest.mark.case_name("Checkbox choices")
def test_checkbox():
    """Dialog that lets the operator pick several options."""
    checked = run_dialog_box(
        DialogBox(
            title_bar="Options fitted",
            dialog_text="Check every option installed on the unit.",
            widget=CheckboxWidget(fields=["Wi-Fi", "GPS", "Cellular"]),
        )
    )
    set_case_artifact({"options": checked})
    assert isinstance(checked, list)
