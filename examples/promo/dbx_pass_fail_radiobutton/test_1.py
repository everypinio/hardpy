import pytest

from hardpy import (
    CheckboxWidget,
    DialogBox,
    HTMLComponent,
    ImageComponent,
    RadiobuttonWidget,
    run_dialog_box,
    set_message,
)

pytestmark = pytest.mark.module_name("Choice control dialog boxes")


@pytest.mark.case_name("Test dialog box with radiobutton with pass_fail")
def test_radiobutton_with_pass_fail():
    dbx = DialogBox(
        dialog_text='Select item "one" out of several and click Pass or Fail.',
        title_bar="Radiobutton example with pass/fail",
        widget=RadiobuttonWidget(fields=["one", "two", "three"]),
        pass_fail=True,
    )
    response = run_dialog_box(dbx)
    set_message(f"Pass/Fail: {response.result}, Selected item: {response.data}")
    assert response.result
    assert response.data == "one", "The answer is not correct"
