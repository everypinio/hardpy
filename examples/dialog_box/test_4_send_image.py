import pytest

from hardpy import DialogBox, ImageWidget, run_dialog_box

pytestmark = pytest.mark.module_name("Image dialog box")


@pytest.mark.case_name("Image")
def test_upload_image():
    dbx = DialogBox(
        dialog_text="Test imageTest imageTest imageTest imageTest imageTest imageTest imageTest imageTest imageTest imageTest imageTest imageTest imageTest imageTest imageTest imageTest imageTest imageTest imageTest image",  # noqa: E501
        widget=ImageWidget(
            address="assets/test.icon",
            width=50,
        ),
    )
    response = run_dialog_box(dbx)
    assert response
