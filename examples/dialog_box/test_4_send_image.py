import pytest

from hardpy import DialogBox, ImageWidget, run_dialog_box

pytestmark = pytest.mark.module_name("Image dialog box")


@pytest.mark.case_name("Image")
def test_upload_image():
    dbx = DialogBox(
        dialog_text="Test image",
        widget=ImageWidget(
            address="assets/test.png",
            # width=50,
        ),
    )
    response = run_dialog_box(dbx)
    assert response
