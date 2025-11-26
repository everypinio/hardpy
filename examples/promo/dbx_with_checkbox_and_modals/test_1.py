import pytest

from hardpy import (
    CheckboxWidget,
    DialogBox,
    run_dialog_box,
    set_message,
)

pytestmark = pytest.mark.module_name("Choice control dialog boxes")


@pytest.mark.case_name("Test dialog box with checkbox")
def test_checkbox():
    dbx = DialogBox(
        dialog_text='Select items "one" and "two" and click the Confirm button',
        title_bar="Checkbox example",
        widget=CheckboxWidget(fields=["one", "two", "three"]),
    )
    response = run_dialog_box(dbx)
    set_message(f"Selected items {response}")
    correct_answer = {"one", "two"}
    assert set(response) == correct_answer, "The answer is not correct"
