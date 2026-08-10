"""Coarse autofocus search — lives in the ``autofocus`` section by directory."""

import pytest
from simulated_device import SimulatedDevice  # type: ignore[import-not-found]

from jig import (
    ComparisonOperation as CompOp,
    DialogBox,
    NumericMeasurement,
    run_dialog_box,
    set_case_measurement,
)

pytestmark = pytest.mark.module_name("Coarse search")

COARSE_PEAK_LIMITS_UM = (100.0, 140.0)


@pytest.mark.case_name("Prepare stage")
def test_prepare_stage():
    """Confirm the stage is clear before the coarse search (prompt in a section)."""
    confirmed = run_dialog_box(
        DialogBox(
            title_bar="Autofocus stage",
            dialog_text="Clear the stage and confirm the sample is seated.",
        )
    )
    assert confirmed, "The operator did not confirm the stage"


@pytest.mark.case_name("Coarse peak")
def test_coarse_peak(device: SimulatedDevice):
    """Find the coarse autofocus peak within the expected window."""
    peak = device.measure_autofocus_coarse_peak()
    lower_limit, upper_limit = COARSE_PEAK_LIMITS_UM

    measurement = NumericMeasurement(
        name="Coarse peak",
        value=peak,
        unit="µm",
        operation=CompOp.GELE,
        lower_limit=lower_limit,
        upper_limit=upper_limit,
    )
    set_case_measurement(measurement)

    assert measurement.result, f"Coarse peak {peak} µm is outside the limits"
