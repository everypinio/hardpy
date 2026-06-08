"""Burst module — one case that streams 42 measurements at 0.5s intervals.

The runningIndex stays put for ~21s; only the row's content grows. Verifies
that we don't repeatedly snap-scroll while data flows into a stable row,
and that the newest measurement stays visible at the bottom of the row.
"""

import time
import pytest

from hardpy import (
    ComparisonOperation as CompOp,
    NumericMeasurement,
    set_case_measurement,
)

pytestmark = pytest.mark.module_name("Burst")


@pytest.mark.case_name("Stream 42 measurements (0.5s interval)")
def test_burst_measurements():
    for i in range(42):
        meas = NumericMeasurement(
            value=24.0 + 0.05 * i,
            name=f"Sample {i + 1:02d}",
            unit="C",
            operation=CompOp.LE,
            comparison_value=60.0,
        )
        set_case_measurement(meas)
        time.sleep(0.5)
