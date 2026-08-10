"""Blocking operator message."""

from time import sleep

import pytest

from jig import set_message, set_operator_message

pytestmark = pytest.mark.module_name("Operator message (blocking)")


@pytest.mark.case_name("Blocking operator message")
def test_blocking_operator_message():
    """Show a blocking operator message while the case continues briefly."""
    set_operator_message(
        msg="This blocking message stays until dismissed.",
        title="Operator message",
    )
    for remaining in range(2, 0, -1):
        set_message(f"Finishing in {remaining} s", "updated_status")
        sleep(1)
    set_message("Done", "updated_status")
    assert True
