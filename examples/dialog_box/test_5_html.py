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
