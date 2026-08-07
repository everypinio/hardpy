import jig
import pytest
import math


@pytest.mark.case_name("Sine Wave Analysis")
@pytest.mark.module_name("Chart Demonstrations")
def test_sine_wave():
    """Test generating and analyzing a sine wave."""
    jig.set_message("Generating sine wave data...")

    # Generate sine wave data
    x_data = []
    y_data = []

    for i in range(100):
        x = i / 10.0  # 0 to 10
        y = math.sin(x)
        x_data.append(x)
        y_data.append(y)

    # Create chart
    chart = jig.Chart(
        title="Sine Wave",
        x_label="Time",
        y_label="Amplitude",
        type=jig.ChartType.LINE,
    )
    chart.add_series(x_data, y_data, "Sine Wave")

    jig.set_case_chart(chart)

    # Verify amplitude
    max_amplitude = max(y_data)
    min_amplitude = min(y_data)
    peak_to_peak = max_amplitude - min_amplitude

    jig.set_case_measurement(
        jig.NumericMeasurement(
            name="Peak-to-Peak Amplitude",
            value=peak_to_peak,
            unit="V",
            lower_limit=1.9,
            upper_limit=2.1,
        )
    )

    jig.set_message(f"Peak-to-peak amplitude: {peak_to_peak:.3f}V")

    assert 1.9 <= peak_to_peak <= 2.1, "Amplitude out of range"


@pytest.mark.case_name("Temperature Curve")
@pytest.mark.module_name("Chart Demonstrations")
def test_temperature_curve():
    """Test temperature rise curve."""
    jig.set_message("Recording temperature curve...")

    # Simulate temperature rise
    time_data = []
    temp_data = []

    for i in range(50):
        time = i * 2  # seconds
        # Exponential rise to 80°C
        temp = 25 + 55 * (1 - math.exp(-i / 20))
        time_data.append(time)
        temp_data.append(temp)

    # Create chart
    chart = jig.Chart(
        title="Temperature Rise Curve",
        x_label="Time (seconds)",
        y_label="Temperature (°C)",
        type=jig.ChartType.LINE,
    )
    chart.add_series(time_data, temp_data, "Temperature")

    jig.set_case_chart(chart)

    # Check final temperature
    final_temp = temp_data[-1]

    jig.set_case_measurement(
        jig.NumericMeasurement(
            name="Final Temperature",
            value=final_temp,
            unit="°C",
            upper_limit=85,
        )
    )

    jig.set_message(f"Final temperature: {final_temp:.1f}°C")

    assert final_temp < 85, f"Temperature too high: {final_temp}°C"
