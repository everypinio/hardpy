import pytest

from hardpy import DialogBox, HTMLComponent, run_dialog_box

pytestmark = pytest.mark.module_name("Dialog box with HTML")


@pytest.mark.case_name("Base dialog box with html code")
def test_dialog_box_with_html_code(generate_bokeh_html):
    test_html = open("plot.html", "r").read()

    dbx = DialogBox(
        title_bar="Operator check",
        dialog_text="Press the Confirm button",
        html=HTMLComponent(html=test_html, is_raw_html=True),
    )
    response = run_dialog_box(dbx)
    assert response
