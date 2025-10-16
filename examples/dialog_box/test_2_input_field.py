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
    result = run_dialog_box(dbx)
    assert result.pass_fail_result is None
    assert result.widget_result == "ok"
    set_message(f"Entered text {result.widget_result}")


@pytest.mark.case_name("Text input with image")
def test_text_input_with_image():
    dbx = DialogBox(
        dialog_text="Type 'ok' and press the Confirm button",
        title_bar="Example of text input",
        widget=TextInputWidget(),
        image=ImageComponent(address="assets/test.png", width=100),
        font_size=18,
    )
    result = run_dialog_box(dbx)
    assert result.pass_fail_result is None
    assert result.widget_result == "ok"
    set_message(f"Entered text {result.widget_result}")


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
    result = run_dialog_box(dbx)
    assert result.pass_fail_result is None
    assert result.widget_result == "ok"
    set_message(f"Entered text {result.widget_result}")


@pytest.mark.case_name("Text input with pass_fail")
def test_text_input_with_pass_fail():
    dbx = DialogBox(
        dialog_text="Type 'ok' and press PASS or FAIL button",
        title_bar="Example of text input with pass/fail",
        widget=TextInputWidget(),
        font_size=18,
        pass_fail=True,
    )
    result = run_dialog_box(dbx)
    assert result.is_pass
    assert result.widget_result == "ok"
    set_message(f"Pass/Fail: {result.is_pass}, Entered text: {result.widget_result}")


@pytest.mark.case_name("Numeric input")
def test_num_input():
    test_num = 123
    dbx = DialogBox(
        dialog_text=f"Enter the number {test_num} and press the Confirm button",
        title_bar="Example of entering a number",
        widget=NumericInputWidget(),
    )
    result = run_dialog_box(dbx)
    assert result.pass_fail_result is None
    assert int(result.widget_result) == test_num
    set_message(f"Entered number {result.widget_result}")


@pytest.mark.case_name("Numeric input with image")
def test_num_input_with_image():
    test_num = 123
    dbx = DialogBox(
        dialog_text=f"Enter the number {test_num} and press the Confirm button",
        title_bar="Example of entering a number",
        widget=NumericInputWidget(),
        image=ImageComponent(address="assets/test.png", width=100),
    )
    result = run_dialog_box(dbx)
    assert result.pass_fail_result is None
    assert int(result.widget_result) == test_num
    set_message(f"Entered number {result.widget_result}")


@pytest.mark.case_name("Numeric input with html")
def test_num_input_with_html():
    test_num = 123
    dbx = DialogBox(
        dialog_text=f"Enter the number {test_num} and press the Confirm button",
        title_bar="Example of entering a number",
        widget=NumericInputWidget(),
        html=HTMLComponent(html=test_html, is_raw_html=True, width=50),
    )
    result = run_dialog_box(dbx)
    assert result.pass_fail_result is None
    assert int(result.widget_result) == test_num
    set_message(f"Entered number {result.widget_result}")


@pytest.mark.case_name("Numeric input with pass_fail")
def test_num_input_with_pass_fail():
    test_num = 123
    dbx = DialogBox(
        dialog_text=f"Enter the number {test_num} and press PASS or FAIL button",
        title_bar="Example of entering a number with pass/fail",
        widget=NumericInputWidget(),
        pass_fail=True,
    )
    result = run_dialog_box(dbx)
    assert result.is_pass
    assert int(result.widget_result) == test_num
    set_message(f"Pass/Fail: {result.is_pass}, Entered number: {result.widget_result}")
