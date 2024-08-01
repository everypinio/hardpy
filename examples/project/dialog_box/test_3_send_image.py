import os
from hardpy import run_dialog_box, set_message
from hardpy.pytest_hardpy.utils.dialog_box import (
    DialogBoxWidget,
    DialogBoxWidgetType,
    DialogBox,
)


def test_upload_image():
    dbx = DialogBox(
        dialog_text=f"Test image",
        widget=DialogBoxWidget(
            DialogBoxWidgetType.IMAGE,
            {"imageUrl": "http://localhost:8600/test_1.jpg"},
        ),
    )
    response = run_dialog_box(dbx)
    assert response is None
