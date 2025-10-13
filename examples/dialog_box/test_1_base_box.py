import pytest

from hardpy import (
    DialogBox,
    HTMLComponent,
    ImageComponent,
    run_dialog_box,
)

pytestmark = pytest.mark.module_name("Base dialog box")

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


@pytest.mark.case_name("Empty test before")
def test_before():
    assert True


@pytest.mark.case_name("Dialog box with html and pass/fail buttons")
def test_dialog_box_with_html_and_pass_fail():
    test_html = """
    <!DOCTYPE html>
    <html>
    <head>
        <style>
            .status-box {
                border: 2px solid #333;
                padding: 10px;
                margin: 10px;
                border-radius: 5px;
                background-color: #f0f0f0;
            }
            .pass { color: green; font-weight: bold; }
            .fail { color: red; font-weight: bold; }
        </style>
    </head>
    <body>
        <h1>Equipment Status Check</h1>

        <div class="status-box">
            <h2>Current Status:</h2>
            <p>Voltage: <span class="pass">12.5V ✓</span></p>
            <p>Current: <span class="pass">2.1A ✓</span></p>
            <p>Temperature: <span class="fail">45°C ⚠️</span></p>
        </div>

        <p>Please verify the equipment status and click PASS or FAIL</p>
    </body>
    </html>
    """
    dbx = DialogBox(
        title_bar="Equipment Verification",
        dialog_text="Check the equipment status in the HTML below and make your decision:",
        html=HTMLComponent(html=test_html, is_raw_html=True, width=60),
        pass_fail=True,
    )
    result = run_dialog_box(dbx)
    assert isinstance(result, bool)


@pytest.mark.case_name("Base dialog box")
def test_base_dialog_box():
    dbx = DialogBox(
        title_bar="Operator check",
        dialog_text="Press the Confirm button",
    )
    response = run_dialog_box(dbx)
    assert response


@pytest.mark.case_name("Base dialog box with image")
def test_base_dialog_box_with_image():
    dbx = DialogBox(
        title_bar="Operator check",
        dialog_text="Press the Confirm button",
        image=ImageComponent(address="assets/test.png", width=100),
    )
    response = run_dialog_box(dbx)
    assert response


@pytest.mark.case_name("Base dialog box with pass_fail")
def test_base_dialog_box_with_pass_fail():
    dbx = DialogBox(
        title_bar="Operator check",
        dialog_text="Press PASS or FAIL button",
        pass_fail=True,
    )
    result = run_dialog_box(dbx)
    # Now returns tuple (pass_fail_result, widget_data)
    assert isinstance(result, bool)


@pytest.mark.case_name("Base dialog box with image and pass_fail")
def test_base_dialog_box_with_image_and_pass_fail():
    dbx = DialogBox(
        title_bar="Operator check",
        dialog_text="Press PASS or FAIL button",
        image=ImageComponent(address="assets/test.png", width=100),
        pass_fail=True,
    )
    result = run_dialog_box(dbx)
    # Now returns tuple (pass_fail_result, widget_data)
    assert isinstance(result, bool)


@pytest.mark.case_name("Empty test after")
def test_after():
    assert True
