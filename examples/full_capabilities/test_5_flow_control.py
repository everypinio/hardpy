"""Retried tests and tests that depend on other tests."""

import pytest

from hardpy import (
    ComparisonOperation as CompOp,
    NumericMeasurement,
    get_current_attempt,
    set_case_artifact,
    set_case_measurement,
    set_message,
)

pytestmark = pytest.mark.module_name("Flow control")

MIN_LINK_QUALITY_PERCENT = 80.0
LINK_ATTEMPTS_BEFORE_SUCCESS = 1

_link_attempts = 0


@pytest.mark.attempt(3)
@pytest.mark.case_name("Communication link")
def test_communication_link():
    """Retry a test up to three times before reporting a failure.

    The simulated link needs a second attempt, as an unreliable one would.
    """
    global _link_attempts  # noqa: PLW0603
    _link_attempts += 1

    attempt = get_current_attempt()
    set_message(f"Attempt {attempt}", "attempt_status")

    assert _link_attempts > LINK_ATTEMPTS_BEFORE_SUCCESS, "The link did not come up"


@pytest.mark.dependency("test_5_flow_control::test_communication_link")
@pytest.mark.case_name("Link quality")
def test_link_quality():
    """Skip this test when the link test did not pass."""
    quality = 93.5

    measurement = NumericMeasurement(
        name="Link quality",
        value=quality,
        unit="%",
        operation=CompOp.GE,
        comparison_value=MIN_LINK_QUALITY_PERCENT,
    )
    set_case_measurement(measurement)

    assert measurement.result, f"Link quality {quality} % is too low"


@pytest.mark.dependency("test_2_measurements::test_supply_voltage")
@pytest.mark.case_name("Power budget")
def test_power_budget():
    """Depend on a test living in another module."""
    set_case_artifact({"power_budget_mw": 55})
