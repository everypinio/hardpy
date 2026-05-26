"""Functional module - slow with a late failure.

By this point the operator has likely scrolled back to inspect earlier
modules. This module exercises the late-run auto-expand + auto-scroll
behavior: a single animation, no yank if the operator is near the bottom
watching live, and a clean reset on the next run.
"""

import time
import pytest

from hardpy import set_message

pytestmark = pytest.mark.module_name("Functional")


@pytest.mark.case_name("Boot sequence")
def test_func_boot():
    time.sleep(2.0)
    set_message("Device reached operational state in 2.4s")


@pytest.mark.case_name("LED indicators")
def test_func_leds():
    time.sleep(2.0)
    set_message("All LEDs cycled green / amber / red as expected")


@pytest.mark.case_name("Button response (fails)")
def test_func_button_fail():
    time.sleep(2.0)
    assert False, "Button SW2 did not register press within 500ms"


@pytest.mark.case_name("Final teardown")
def test_func_teardown():
    time.sleep(2.0)
    set_message("All resources released, device powered down")
