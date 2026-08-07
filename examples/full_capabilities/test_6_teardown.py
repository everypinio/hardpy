"""Teardown module, runs after the main tests whatever their result."""

import pytest
from simulated_device import SimulatedDevice  # type: ignore[import-not-found]

from jig import (
    Group,
    get_current_report,
    set_message,
    set_run_artifact,
)

pytestmark = [
    pytest.mark.module_name("Teardown"),
    pytest.mark.module_group(Group.TEARDOWN),
]


@pytest.mark.case_name("Power off")
def test_power_off(device: SimulatedDevice):
    device.power_off()
    assert not device.is_powered, "The device is still powered"


@pytest.mark.case_name("Run summary")
def test_run_summary():
    """Store a summary of the run next to the report."""
    report = get_current_report()
    assert report, "The run report is not available"

    executed_cases = sum(len(module.cases) for module in report.modules.values())
    set_run_artifact({"executed_cases": executed_cases})
    set_message(f"{executed_cases} cases executed")
