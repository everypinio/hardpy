import pytest

from hardpy import run_dialog_box, DuplicateDialogBoxError
from hardpy.pytest_hardpy.utils import DialogBox


pytestmark = pytest.mark.module_name("Base dialog box")


@pytest.mark.case_name("Dialog box with error")
def test_dialog_box_error():
    dbx_1 = DialogBox(
        title_bar="Operator check 1",
        dialog_text="Press the Confirm button",
    )
    response = run_dialog_box(dbx_1)
    dbx_2 = DialogBox(
        title_bar="Operator check 2",
        dialog_text="Press the Confirm button",
    )
    with pytest.raises(DuplicateDialogBoxError):
        response = run_dialog_box(dbx_2)
    assert response is None


@pytest.mark.case_name("Dialog box without title")
def test_dialog_without_title():
    dbx_1 = DialogBox(
        dialog_text="Press the Confirm button",
    )
    response = run_dialog_box(dbx_1)
    assert response is None
