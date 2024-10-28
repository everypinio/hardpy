import pytest

from hardpy import DialogBox, ImageWidget, run_dialog_box

pytestmark = pytest.mark.module_name("Image dialog box")


@pytest.mark.attempt(2)
@pytest.mark.case_name("Image")
def test_upload_image():
    dbx = DialogBox(
        dialog_text="Test image",  # noqa: E501
        widget=ImageWidget(
            # address="assets/sample_1920x1280.gif",
            # address="assets/test.webp",
            address="assets/test.png",
            width=200,
        ),
    )
    response = run_dialog_box(dbx)
    assert False
