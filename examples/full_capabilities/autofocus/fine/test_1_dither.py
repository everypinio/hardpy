"""Nested ``autofocus/fine`` section — demonstrates recursive grouping."""

import pytest
from simulated_device import SimulatedDevice  # type: ignore[import-not-found]

from jig import (
    ComparisonOperation as CompOp,
    DialogBox,
    NumericMeasurement,
    run_dialog_box,
    set_case_measurement,
)

pytestmark = pytest.mark.module_name("Dither")

DITHER_LIMIT_UM = 5.0


@pytest.mark.case_name("Enable fine loop")
def test_enable_fine_loop():
    """Ask the operator to enable fine dither before measuring."""
    confirmed = run_dialog_box(
        DialogBox(
            title_bar="Fine autofocus",
            dialog_text="Enable the fine dither loop on the controller.",
            button_text=["Enabled"],
        )
    )
    assert confirmed, "The operator did not enable the fine loop"


@pytest.mark.case_name("Dither amplitude")
def test_dither_amplitude(device: SimulatedDevice):
    """Check that fine dither stays within the stability budget."""
    dither = device.measure_autofocus_dither()

    measurement = NumericMeasurement(
        name="Dither amplitude",
        value=dither,
        unit="µm",
        operation=CompOp.LE,
        comparison_value=DITHER_LIMIT_UM,
    )
    set_case_measurement(measurement)

    assert measurement.result, f"Dither {dither} µm is above the limit"
