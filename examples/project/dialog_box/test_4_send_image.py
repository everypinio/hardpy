import pytest
from hardpy import run_dialog_box
from hardpy.pytest_hardpy.utils.dialog_box import (
    DialogBoxWidget,
    DialogBoxWidgetType,
    DialogBox,
    ImageInfo,
)


@pytest.mark.case_name("Image")
def test_upload_image():
    dbx = DialogBox(
        dialog_text="Test image",
        widget=DialogBoxWidget(
            DialogBoxWidgetType.IMAGE,
            ImageInfo(image_address="assets/test.png"),
        ),
    )
    response = run_dialog_box(dbx)
    assert response is None
