import pytest

from hardpy import DialogBox, HTMLComponent, run_dialog_box

pytestmark = pytest.mark.module_name("Dialog box with HTML")


@pytest.mark.case_name("Base dialog box with html code")
def test_base_dialog_box_with_html_code():
    test_html = """
    <!DOCTYPE html>
    <html>
    <body>

    <h1>My First Heading</h1>

    <p>My first paragraph.</p>

    </body>
    </html>
    """
    dbx = DialogBox(
        title_bar="Operator check",
        dialog_text="Press the Confirm button",
        html=HTMLComponent(html=test_html, is_raw_html=True),
    )
    response = run_dialog_box(dbx)
    assert response


@pytest.mark.case_name("Base dialog box with html link")
def test_base_dialog_box_with_html_link():
    dbx = DialogBox(
        title_bar="Operator check",
        dialog_text="Press the Confirm button",
        html=HTMLComponent(
            html="https://en.wikipedia.org/wiki/Main_Page",
            is_raw_html=False,
        ),
    )
    response = run_dialog_box(dbx)
    assert response
