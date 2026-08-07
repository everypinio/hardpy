from collections.abc import Iterator
from pathlib import Path

import pytest
from simulated_device import SimulatedDevice  # type: ignore[import-not-found]

from jig import JsonLoader, get_current_report, set_operator_message

DUT_SERIAL_NUMBER = "SN-2026-000123"
REPORTS_DIR = Path.cwd() / "reports"


@pytest.fixture(scope="session")
def device() -> Iterator[SimulatedDevice]:
    """Provide a powered device for the whole test run."""
    device = SimulatedDevice(DUT_SERIAL_NUMBER)
    device.power_on()
    yield device
    device.power_off()


def save_report() -> None:
    """Store the finished run as a JSON report."""
    report = get_current_report()
    if not report:
        return
    is_saved = JsonLoader(REPORTS_DIR).load(report)
    if is_saved:
        set_operator_message(
            msg=f"Report saved in {REPORTS_DIR}",
            title="End of testing",
            block=False,
        )


@pytest.fixture(scope="session", autouse=True)
def fill_actions_after_test(post_run_functions: list):
    """Save the report once the run is over."""
    post_run_functions.append(save_report)
    yield
