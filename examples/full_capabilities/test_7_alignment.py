"""Alignment checks grouped via the ``module_section`` marker (not a directory)."""

import pytest
from simulated_device import SimulatedDevice  # type: ignore[import-not-found]

from jig import (
    ComparisonOperation as CompOp,
    NumericMeasurement,
    set_case_measurement,
)

pytestmark = [
    pytest.mark.module_name("Alignment checks"),
    pytest.mark.module_section("Alignment"),
]

ALIGNMENT_OFFSET_LIMIT_UM = 1.0


@pytest.mark.case_name("Alignment offset")
def test_alignment_offset(device: SimulatedDevice):
    """Verify the optical alignment offset is within tolerance."""
    offset = device.measure_alignment_offset()

    measurement = NumericMeasurement(
        name="Alignment offset",
        value=offset,
        unit="µm",
        operation=CompOp.LE,
        comparison_value=ALIGNMENT_OFFSET_LIMIT_UM,
    )
    set_case_measurement(measurement)

    assert measurement.result, f"Alignment offset {offset} µm is above the limit"
