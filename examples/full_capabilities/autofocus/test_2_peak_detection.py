"""Fine peak detection at the autofocus section root."""

import pytest
from simulated_device import SimulatedDevice  # type: ignore[import-not-found]

from jig import (
    ComparisonOperation as CompOp,
    NumericMeasurement,
    set_case_measurement,
)

pytestmark = pytest.mark.module_name("Peak detection")

FINE_PEAK_LIMITS_UM = (110.0, 125.0)


@pytest.mark.case_name("Fine peak")
def test_fine_peak(device: SimulatedDevice):
    """Confirm the fine autofocus peak is near the coarse result."""
    peak = device.measure_autofocus_fine_peak()
    lower_limit, upper_limit = FINE_PEAK_LIMITS_UM

    measurement = NumericMeasurement(
        name="Fine peak",
        value=peak,
        unit="µm",
        operation=CompOp.GELE,
        lower_limit=lower_limit,
        upper_limit=upper_limit,
    )
    set_case_measurement(measurement)

    assert measurement.result, f"Fine peak {peak} µm is outside the limits"
