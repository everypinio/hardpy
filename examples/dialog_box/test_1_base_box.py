import pytest

from hardpy import DialogBox, run_dialog_box

pytestmark = pytest.mark.module_name("Base dialog box")


def test_before():
    assert True


def test_base_dialog_box():
    dbx = DialogBox(
        title_bar="Operator check",
        dialog_text="Press the Confirm button",
    )
    response = run_dialog_box(dbx)
    assert response


def test_base_dialog_box_long_text():
    dbx = DialogBox(
        title_bar="Operator check",
        dialog_text="Press the Confirm button\nPress the Confirm button\nPress the Confirm button\nPress the Confirm button\nPress the Confirm button\nPress the Confirm button\nPress the Confirm button\nPress the Confirm button\nPress the Confirm button\nPress the Confirm button\nPress the Confirm button\nPress the Confirm button\nPress the Confirm button\nPress the Confirm button\nPress the Confirm button\nPress the Confirm button\nPress the Confirm button\nPress the Confirm button\nPress the Confirm button\nPress the Confirm button\nPress the Confirm button\nPress the Confirm button\nPress the Confirm button\nPress the Confirm button\nPress the Confirm button\nPress the Confirm button\nPress the Confirm button\nPress the Confirm button\nPress the Confirm button\nPress the Confirm button\nPress the Confirm button\nPress the Confirm button\nPress the Confirm button\nPress the Confirm button\nPress the Confirm button\n",  # noqa: E501
    )
    response = run_dialog_box(dbx)
    assert response


def test_after():
    assert True
