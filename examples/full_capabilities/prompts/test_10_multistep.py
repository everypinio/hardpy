"""Multistep dialog."""

import pytest

from jig import (
    DialogBox,
    HTMLComponent,
    ImageComponent,
    MultistepWidget,
    StepWidget,
    run_dialog_box,
)

pytestmark = pytest.mark.module_name("Multistep")


@pytest.mark.case_name("Multistep")
def test_multistep():
    """Walk the operator through several steps in one dialog."""
    assert run_dialog_box(
        DialogBox(
            title_bar="Setup checklist",
            dialog_text="Complete each step before continuing.",
            widget=MultistepWidget(
                steps=[
                    StepWidget(
                        title="Power",
                        text="Connect the 3.3 V supply to J1.",
                    ),
                    StepWidget(
                        title="Reference",
                        text=None,
                        image=ImageComponent(address="assets/test.png", width=50),
                    ),
                    StepWidget(
                        title="Document",
                        text="Open the procedure if needed.",
                        html=HTMLComponent(
                            html="<p>See document <b>TP-100</b>.</p>",
                            width=100,
                        ),
                    ),
                ],
            ),
        )
    ), "The operator did not finish the steps"
