import pytest

from hardpy import (
    DialogBox,
    HTMLComponent,
    ImageComponent,
    NumericInputWidget,
    TextInputWidget,
    run_dialog_box,
    set_message,
)

pytestmark = pytest.mark.module_name("Input field dialog boxes")

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


@pytest.mark.case_name("Text input")
def test_text_input():
    dbx = DialogBox(
        dialog_text="Type 'ok' and press the Confirm button",
        title_bar="Example of text input",
        widget=TextInputWidget(),
        font_size=18,
    )
    response = run_dialog_box(dbx)
    set_message(f"Entered text {response}")
    assert response == "ok", "The entered text is not correct"


@pytest.mark.case_name("Text input with image")
def test_text_input_with_image():
    dbx = DialogBox(
        dialog_text="Type 'ok' and press the Confirm button",
        title_bar="Example of text input",
        widget=TextInputWidget(),
        image=ImageComponent(address="assets/test.png", width=100),
        font_size=18,
    )
    response = run_dialog_box(dbx)
    set_message(f"Entered text {response}")
    assert response == "ok", "The entered text is not correct"


@pytest.mark.case_name("Text input with html")
def test_text_input_with_html():
    dbx = DialogBox(
        dialog_text="Type 'ok' and press the Confirm button",
        title_bar="Example of text input",
        widget=TextInputWidget(),
        html=HTMLComponent(
            html=test_html,
            is_raw_html=True,
            width=50,
        ),
        font_size=18,
    )
    response = run_dialog_box(dbx)
    set_message(f"Entered text {response}")
    assert response == "ok", "The entered text is not correct"


@pytest.mark.case_name("Text input with pass_fail")
def test_text_input_with_pass_fail():
    dbx = DialogBox(
        dialog_text="Type 'ok' and press Pass or Fail button",
        title_bar="Example of text input with pass/fail",
        widget=TextInputWidget(),
        font_size=18,
        pass_fail=True,
    )
    response = run_dialog_box(dbx)
    set_message(f"Pass/Fail: {response.result}, Entered text: {response.data}")
    assert response.result
    assert response.data == "ok", "The entered text is not correct"


@pytest.mark.case_name("Numeric input")
def test_num_input():
    test_num = 123
    dbx = DialogBox(
        dialog_text=f"Enter the number {test_num} and press the Confirm button",
        title_bar="Example of entering a number",
        widget=NumericInputWidget(),
    )
    response = int(run_dialog_box(dbx))
    set_message(f"Entered number {response}")
    assert response == test_num, "The entered number is not correct"


@pytest.mark.case_name("Numeric input with image")
def test_num_input_with_image():
    test_num = 123
    dbx = DialogBox(
        dialog_text=f"Enter the number {test_num} and press the Confirm button",
        title_bar="Example of entering a number",
        widget=NumericInputWidget(),
        image=ImageComponent(address="assets/test.png", width=100),
    )
    response = int(run_dialog_box(dbx))
    set_message(f"Entered number {response}")
    assert response == test_num, "The entered number is not correct"


@pytest.mark.case_name("Numeric input with html")
def test_num_input_with_html():
    test_num = 123
    dbx = DialogBox(
        dialog_text=f"Enter the number {test_num} and press the Confirm button",
        title_bar="Example of entering a number",
        widget=NumericInputWidget(),
        html=HTMLComponent(html=test_html, is_raw_html=True, width=50),
    )
    response = int(run_dialog_box(dbx))
    set_message(f"Entered number {response}")
    assert response == test_num, "The entered number is not correct"


@pytest.mark.case_name("Numeric input with pass_fail")
def test_num_input_with_pass_fail():
    test_num = 123
    dbx = DialogBox(
        dialog_text=f"Enter the number {test_num} and press Pass or Fail button",
        title_bar="Example of entering a number with pass/fail",
        widget=NumericInputWidget(),
        pass_fail=True,
    )
    response = run_dialog_box(dbx)
    set_message(f"Pass/Fail: {response.result}, Entered number: {response.data}")
    assert response.result
    assert int(response.data) == test_num, "The entered number is not correct"
