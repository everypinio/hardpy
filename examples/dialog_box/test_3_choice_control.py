import pytest

from hardpy import (
    CheckboxWidget,
    DialogBox,
    HTMLComponent,
    ImageComponent,
    RadiobuttonWidget,
    run_dialog_box,
    set_message,
)

pytestmark = pytest.mark.module_name("Choice control dialog boxes")

test_html = """
<!DOCTYPE html>
<html>
<body>

<h1>Test HTML Page</h1>

<p>It is testing page.</p>
<p>You can put anything on it.</p>

</body>
</html>
"""


@pytest.mark.case_name("Test dialog box with radiobutton")
def test_radiobutton():
    dbx = DialogBox(
        dialog_text='Select item "one" out of several and click Confirm.',
        title_bar="Radiobutton example",
        widget=RadiobuttonWidget(fields=["one", "two", "three"]),
    )
    response = run_dialog_box(dbx)
    set_message(f"Selected item {response}")
    assert response == "one", "The answer is not correct"


@pytest.mark.case_name("Test dialog box with radiobutton with image")
def test_radiobutton_with_image():
    dbx = DialogBox(
        dialog_text='Select item "one" out of several and click Confirm.',
        title_bar="Radiobutton example",
        widget=RadiobuttonWidget(fields=["one", "two", "three"]),
        image=ImageComponent(address="assets/test.png", width=100),
    )
    response = run_dialog_box(dbx)
    set_message(f"Selected item {response}")
    assert response == "one", "The answer is not correct"


@pytest.mark.case_name("Test dialog box with radiobutton with html")
def test_radiobutton_with_html():
    dbx = DialogBox(
        dialog_text='Select item "one" out of several and click Confirm.',
        title_bar="Radiobutton example",
        widget=RadiobuttonWidget(fields=["one", "two", "three"]),
        html=HTMLComponent(
            html=test_html,
            is_raw_html=True,
            width=50,
        ),
    )
    response = run_dialog_box(dbx)
    set_message(f"Selected item {response}")
    assert response == "one", "The answer is not correct"


@pytest.mark.case_name("Test dialog box with radiobutton with pass_fail")
def test_radiobutton_with_pass_fail():
    dbx = DialogBox(
        dialog_text='Select item "one" out of several and click Pass or Fail.',
        title_bar="Radiobutton example with pass/fail",
        widget=RadiobuttonWidget(fields=["one", "two", "three"]),
        pass_fail=True,
    )
    response = run_dialog_box(dbx)
    set_message(f"Pass/Fail: {response.result}, Selected item: {response.data}")
    assert response.result
    assert response.data == "one", "The answer is not correct"


@pytest.mark.case_name("Test dialog box with checkbox")
def test_checkbox():
    dbx = DialogBox(
        dialog_text='Select items "one" and "two" and click the Confirm button',
        title_bar="Checkbox example",
        widget=CheckboxWidget(fields=["one", "two", "three"]),
    )
    response = run_dialog_box(dbx)
    set_message(f"Selected items {response}")
    correct_answer = {"one", "two"}
    assert set(response) == correct_answer, "The answer is not correct"


@pytest.mark.case_name("Test dialog box with checkbox with image")
def test_checkbox_with_image():
    dbx = DialogBox(
        dialog_text='Select items "one" and "two" and click the Confirm button',
        title_bar="Checkbox example",
        widget=CheckboxWidget(fields=["one", "two", "three"]),
        image=ImageComponent(address="assets/test.png", width=100),
    )
    response = run_dialog_box(dbx)
    set_message(f"Selected items {response}")
    correct_answer = {"one", "two"}
    assert set(response) == correct_answer, "The answer is not correct"


@pytest.mark.case_name("Test dialog box with checkbox with html")
def test_checkbox_with_html():
    dbx = DialogBox(
        dialog_text='Select items "one" and "two" and click the Confirm button',
        title_bar="Checkbox example",
        widget=CheckboxWidget(fields=["one", "two", "three"]),
        html=HTMLComponent(
            html=test_html,
            is_raw_html=True,
            width=50,
        ),
    )
    response = run_dialog_box(dbx)
    set_message(f"Selected items {response}")
    correct_answer = {"one", "two"}
    assert set(response) == correct_answer, "The answer is not correct"


@pytest.mark.case_name("Test dialog box with checkbox with pass_fail")
def test_checkbox_with_pass_fail():
    dbx = DialogBox(
        dialog_text='Select items "one" and "two" and click Pass or Fail button',
        title_bar="Checkbox example with pass/fail",
        widget=CheckboxWidget(fields=["one", "two", "three"]),
        pass_fail=True,
    )
    response = run_dialog_box(dbx)
    set_message(f"Pass/Fail: {response.result}, Selected items: {response.data}")
    assert response.result
    correct_answer = {"one", "two"}
    assert set(response.data) == correct_answer, "The answer is not correct"
