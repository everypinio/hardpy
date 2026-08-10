"""Dialog with embedded raw HTML."""

import pytest

from jig import DialogBox, HTMLComponent, run_dialog_box

pytestmark = pytest.mark.module_name("HTML code")


@pytest.mark.case_name("HTML code")
def test_html_code():
    """Confirm dialog that embeds a raw HTML document."""
    html = """
    <!DOCTYPE html>
    <html>
    <body>
      <h1>Inline HTML</h1>
      <p>This content is rendered inside the dialog.</p>
    </body>
    </html>
    """
    assert run_dialog_box(
        DialogBox(
            title_bar="HTML code",
            dialog_text="Review the HTML panel, then confirm.",
            html=HTMLComponent(html=html, is_raw_html=True, width=50),
        )
    )
