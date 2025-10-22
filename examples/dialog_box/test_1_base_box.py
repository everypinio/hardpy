import pytest

from hardpy import (
    DialogBox,
    ImageComponent,
    run_dialog_box,
)

pytestmark = pytest.mark.module_name("Base dialog box")


@pytest.mark.case_name("Empty test before")
def test_before():
    assert True


@pytest.mark.case_name("Base dialog box")
def test_base_dialog_box():
    dbx = DialogBox(
        title_bar="Operator check",
        dialog_text="Press the Confirm button",
    )
    response = run_dialog_box(dbx)
    assert response

@pytest.mark.case_name("Base dialog box with image")
def test_base_dialog_box_with_image():
    dbx = DialogBox(
        title_bar="Operator check",
        dialog_text="Press the Confirm button",
        image=ImageComponent(address="assets/test.png", width=100),
    )
    response = run_dialog_box(dbx)
    assert response


@pytest.mark.case_name("Base dialog box with pass_fail")
def test_base_dialog_box_with_pass_fail():
    dbx = DialogBox(
        title_bar="Operator check",
        dialog_text="Press Pass or Fail button",
        pass_fail=True,
    )
    response = run_dialog_box(dbx)
    assert response.result
    assert response.data


@pytest.mark.case_name("Base dialog box with image and pass_fail")
def test_base_dialog_box_with_image_and_pass_fail():
    dbx = DialogBox(
        title_bar="Operator check",
        dialog_text="Press Pass or Fail button",
        image=ImageComponent(address="assets/test.png", width=100),
        pass_fail=True,
    )
    response = run_dialog_box(dbx)
    assert response.result
    assert response.data


@pytest.mark.case_name("Empty test after")
def test_after():
    assert True
