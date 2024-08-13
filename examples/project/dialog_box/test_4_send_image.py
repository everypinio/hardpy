from hardpy import run_dialog_box
from hardpy.pytest_hardpy.utils.dialog_box import (
    DialogBoxWidget,
    DialogBoxWidgetType,
    DialogBox,
    ImageInfo,
)

def test_upload_image():
    dbx = DialogBox(
        dialog_text=f"Test image",
        widget=DialogBoxWidget(
            DialogBoxWidgetType.IMAGE,
            ImageInfo(image_address='assets/test.jpg'),
        ),
    )
    response = run_dialog_box(dbx)
    assert response is None
