import pytest

from hardpy import (
    CheckboxWidget,
    DialogBox,
    RadiobuttonWidget,
    run_dialog_box,
    set_message,
)
from hardpy.pytest_hardpy.utils.dialog_box import ImageWidget

pytestmark = pytest.mark.module_name("Choice control dialog boxes")


# @pytest.mark.case_name("Test dialog box with radiobutton")
# def test_radiobutton():
#     dbx = DialogBox(
#         dialog_text='Select item "one" out of several and click Confirm.',
#         title_bar="Radiobutton example",
#         widget=RadiobuttonWidget(fields=["one", "two", "three"]),
#     )
#     response = run_dialog_box(dbx)
#     set_message(f"Selected item {response}")
#     assert response == "one", "The answer is not correct"


# @pytest.mark.case_name("Test dialog box with checkbox")
# def test_checkbox():
#     dbx = DialogBox(
#         dialog_text='Select items "one" and "two" and click the Confirm button',
#         title_bar="Checkbox example",
#         widget=CheckboxWidget(fields=["one", "two", "three"]),
#     )
#     response = run_dialog_box(dbx)
#     set_message(f"Selected item {response}")
#     correct_answer = {"one", "two"}
#     assert set(response) == correct_answer, "The answer is not correct"


# @pytest.mark.case_name("Test dialog box with radiobutton with image")
# def test_radiobutton_with_image():
#     dbx = DialogBox(
#         dialog_text='Select item "one" out of several and click Confirm.',
#         title_bar="Radiobutton example",
#         widget=RadiobuttonWidget(fields=["one", "two", "three"]),
#         image=ImageWidget(address="assets/test.png", width=50),
#     )
#     response = run_dialog_box(dbx)
#     set_message(f"Selected item {response}")
#     assert response == "one", "The answer is not correct"


# @pytest.mark.case_name("Test dialog box with checkbox with image")
# def test_checkbox_with_image():
#     dbx = DialogBox(
#         dialog_text='Select items "one" and "two" and click the Confirm button',
#         title_bar="Checkbox example",
#         widget=CheckboxWidget(fields=["one", "two", "three"]),
#         image=ImageWidget(address="assets/test.png", width=50),
#     )
#     response = run_dialog_box(dbx)
#     set_message(f"Selected item {response}")
#     correct_answer = {"one", "two"}
#     assert set(response) == correct_answer, "The answer is not correct"