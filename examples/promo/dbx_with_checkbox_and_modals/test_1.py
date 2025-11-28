import pytest

from hardpy import (
    CheckboxWidget,
    DialogBox,
    run_dialog_box,
    set_message,
)

pytestmark = pytest.mark.module_name("Production Test - Function Verification")


@pytest.mark.case_name("Optional Features Selection Test")
def test_optional_features_selection():
    dbx = DialogBox(
        dialog_text='Select "Ethernet" and "RS-485" communication interfaces and click Confirm',
        title_bar="Communication Interfaces Configuration",
        widget=CheckboxWidget(fields=["Ethernet", "RS-485", "Wi-Fi"]),
    )
    response = run_dialog_box(dbx)
    set_message(f"Selected interfaces: {response}")
    correct_answer = {"Ethernet", "RS-485"}
    assert set(response) == correct_answer, "Incorrect communication interfaces selected"
