import pytest

from hardpy import DialogBox, run_dialog_box

pytestmark = pytest.mark.module_name("Base dialog box")


@pytest.mark.case_name("Empty test before")
def test_before() -> None:  # noqa: D103
    assert True  # noqa: S101


@pytest.mark.case_name("Base dialog box")
def test_base_dialog_box() -> None:
    dbx = DialogBox(
        title_bar="Operator check",
        dialog_text="Press the Confirm button",
    )
    response = run_dialog_box(dbx)
    assert response


@pytest.mark.case_name("Empty test after")
def test_after():
    assert True
