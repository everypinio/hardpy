import pytest

from hardpy import run_dialog_box, set_message
from hardpy.pytest_hardpy.utils.dialog_box import (
    DialogBoxWidget,
    DialogBoxWidgetType,
    DialogBox,
    RadiobuttonInfo,
    CheckboxInfo,
)


pytestmark = pytest.mark.module_name("Choice control dialog boxes")

@pytest.mark.case_name("Radiobutton")
def test_radiobutton():
    dbx = DialogBox(
        dialog_text=f"Select one item (1) from several and click the Confirm button",
        title_bar="Radiobutton example",
        widget=DialogBoxWidget(
            DialogBoxWidgetType.RADIOBUTTON,
            RadiobuttonInfo(fields=["one", "two", "three"]),
        ),
    )
    response = run_dialog_box(dbx)
    set_message(f"Selected item {response}")
    assert response == "one", "The answer is not correct"


@pytest.mark.case_name("Checkbox")
def test_checkbox():
    dbx = DialogBox(
        dialog_text=f"Select one or more items (1) and click the Confirm button",
        title_bar="Checkbox example",
        widget=DialogBoxWidget(
            DialogBoxWidgetType.CHECKBOX, CheckboxInfo(fields=["one", "two", "three"]),
        ),
    )
    response = run_dialog_box(dbx)
    set_message(f"Selected item {response}")
    assert response == '["one"]', "The answer is not correct"