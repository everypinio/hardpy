"""Dialog with an HTML URL iframe."""

import pytest

from jig import DialogBox, HTMLComponent, run_dialog_box

pytestmark = pytest.mark.module_name("HTML URL")


@pytest.mark.case_name("HTML URL")
def test_html_url():
    """Confirm dialog that loads a remote page in an iframe."""
    assert run_dialog_box(
        DialogBox(
            title_bar="HTML URL",
            dialog_text="Review the documentation page, then confirm.",
            html=HTMLComponent(
                html="https://everypinio.github.io/jig/",
                is_raw_html=False,
                width=50,
                border=2,
            ),
        )
    )
