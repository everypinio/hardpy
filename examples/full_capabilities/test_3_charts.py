"""Charts attached to a test case."""

import pytest
from simulated_device import SimulatedDevice  # type: ignore[import-not-found]

from jig import (
    Chart,
    ChartType,
    ComparisonOperation as CompOp,
    NumericMeasurement,
    set_case_chart,
    set_case_measurement,
)

pytestmark = pytest.mark.module_name("Charts")

MAX_STARTUP_CURRENT_MA = 60.0
MIN_PASSBAND_GAIN_DB = -1.0


@pytest.mark.case_name("Startup current")
def test_startup_current(device: SimulatedDevice):
    """Attach a single series chart, one point per sample."""
    times, currents = device.record_startup_current()

    chart = Chart(
        title="Startup current",
        x_label="Time, ms",
        y_label="Current, mA",
        type=ChartType.LINE,
    )
    chart.add_series(times, currents, "Inrush")
    set_case_chart(chart)

    peak_current = max(currents)
    measurement = NumericMeasurement(
        name="Peak startup current",
        value=peak_current,
        unit="mA",
        operation=CompOp.LE,
        comparison_value=MAX_STARTUP_CURRENT_MA,
    )
    set_case_measurement(measurement)

    assert measurement.result, f"Peak current {peak_current:.1f} mA is too high"


@pytest.mark.case_name("Frequency response")
def test_frequency_response(device: SimulatedDevice):
    """Attach a chart with several series and a logarithmic X axis."""
    frequencies, gains = device.sweep_frequency_response()
    tolerance_db = [-3.0] * len(frequencies)

    chart = Chart(
        title="Frequency response",
        x_label="Frequency, Hz",
        y_label="Gain, dB",
        type=ChartType.LINE_LOG_X,
    )
    chart.add_series(frequencies, gains, "Measured")
    chart.add_series(frequencies, tolerance_db, "Tolerance")
    set_case_chart(chart)

    passband_gain = gains[0]
    measurement = NumericMeasurement(
        name="Passband gain",
        value=passband_gain,
        unit="dB",
        operation=CompOp.GE,
        comparison_value=MIN_PASSBAND_GAIN_DB,
    )
    set_case_measurement(measurement)

    assert measurement.result, f"Gain {passband_gain:.2f} dB is too low"
