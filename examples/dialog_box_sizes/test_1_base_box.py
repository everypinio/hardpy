import pytest

from hardpy import DialogBox, run_dialog_box
from hardpy.pytest_hardpy.utils.dialog_box import ImageWidget

pytestmark = pytest.mark.module_name("Base dialog box")


@pytest.mark.case_name("Empty test before")
def test_before():
    assert True


# @pytest.mark.case_name("Base dialog box with image")
# def test_base_dialog_box_with_image():
#     dbx = DialogBox(
#         title_bar="Operator check",
#         dialog_text="Press the Confirm button",
#         image=ImageWidget(address="assets/test.png", width=50, border=1),
#     )
#     response = run_dialog_box(dbx)
#     assert response


# @pytest.mark.case_name("Base dialog box")
# def test_base_dialog_box():
#     dbx = DialogBox(
#         title_bar="Operator check",
#         dialog_text="Press the Confirm button",
#     )
#     response = run_dialog_box(dbx)
#     assert response


# @pytest.mark.case_name("Empty test after")
# def test_after():
#     assert True
