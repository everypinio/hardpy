"""Non-blocking operator message cleared by the test."""

from time import sleep

import pytest

from jig import clear_operator_message, set_message, set_operator_message

pytestmark = pytest.mark.module_name("Operator message (non-blocking)")


@pytest.mark.case_name("Non-blocking operator message")
def test_nonblocking_operator_message():
    """Show a non-blocking message, then clear it from the test."""
    set_operator_message(
        msg="This message will be cleared automatically.",
        title="Operator message",
        block=False,
        font_size=18,
    )
    for remaining in range(2, 0, -1):
        set_message(f"Clearing in {remaining} s", "updated_status")
        sleep(1)
    clear_operator_message()
    set_message("Cleared", "updated_status")
    sleep(1)
    assert True
