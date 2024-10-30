import pytest

from hardpy import DialogBox, ImageWidget, run_dialog_box

pytestmark = pytest.mark.module_name("Image dialog box")


@pytest.mark.case_name("Image")
def test_upload_image_1():
    dbx = DialogBox(
        dialog_text="Test image",  # noqa: E501
        widget=ImageWidget(
            address="assets/test.png",
            width=100,
        ),
    )
    response = run_dialog_box(dbx)
    assert response


@pytest.mark.case_name("Image")
def test_upload_image_2():
    dbx = DialogBox(
        dialog_text="Test imageTest imageTest imageTest imageTest imageTest imageTest imageTest imageTest imageTest imageTest imageTest imageTest imageTest imageTest imageTest imageTest imageTest imageTest image",  # noqa: E501
        widget=ImageWidget(
            address="assets/test.png",
            width=100,
        ),
    )
    response = run_dialog_box(dbx)
    assert response


@pytest.mark.attempt(2)
@pytest.mark.case_name("Image")
def test_upload_image_3():
    dbx = DialogBox(
        dialog_text="Test image",  # noqa: E501
        widget=ImageWidget(
            address="assets/sample_1920x1280.gif",
            width=100,
        ),
    )
    response = run_dialog_box(dbx)
    assert response


@pytest.mark.case_name("Image")
def test_upload_image_4():
    dbx = DialogBox(
        dialog_text="Test imageTest imageTest imageTest imageTest imageTest imageTest imageTest imageTest imageTest imageTest imageTest imageTest imageTest imageTest imageTest imageTest imageTest imageTest image",  # noqa: E501
        widget=ImageWidget(
            address="assets/sample_1920x1280.gif",
            width=100,
        ),
    )
    response = run_dialog_box(dbx)
    assert response
