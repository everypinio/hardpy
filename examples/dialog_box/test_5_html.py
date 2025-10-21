import pytest

from hardpy import DialogBox, HTMLComponent, run_dialog_box

pytestmark = pytest.mark.module_name("Dialog box with HTML")


@pytest.mark.case_name("Base dialog box with html code")
def test_base_dialog_box_with_html_code():
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
    dbx = DialogBox(
        title_bar="Operator check",
        dialog_text="Press the Confirm button",
        html=HTMLComponent(html=test_html, is_raw_html=True, width=50),
    )
    response = run_dialog_box(dbx)
    assert response


@pytest.mark.case_name("Base dialog box with html link")
def test_base_dialog_box_with_html_link():
    dbx = DialogBox(
        title_bar="Operator check",
        dialog_text="Press the Confirm button",
        html=HTMLComponent(
            html="https://everypinio.github.io/hardpy/",
            is_raw_html=False,
            width=50,
        ),
    )
    response = run_dialog_box(dbx)
    assert response


@pytest.mark.case_name("Base dialog box with html link and border")
def test_base_dialog_box_with_html_link_and_border():
    dbx = DialogBox(
        title_bar="Operator check",
        dialog_text="Press the Confirm button",
        html=HTMLComponent(
            html="https://everypinio.github.io/hardpy/",
            is_raw_html=False,
            border=3,
        ),
    )
    response = run_dialog_box(dbx)
    assert response


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

        <p>Please verify the equipment status and click Pass or Fail</p>
    </body>
    </html>
    """
    dbx = DialogBox(
        title_bar="Equipment Verification",
        dialog_text="Check the equipment status in the HTML below and make your decision:",  # noqa: E501
        html=HTMLComponent(html=test_html, is_raw_html=True, width=60),
        pass_fail=True,
    )
    response = run_dialog_box(dbx)
    assert response.result
    assert response.data
