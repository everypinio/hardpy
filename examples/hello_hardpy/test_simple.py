import random

import pytest

import hardpy
from hardpy import Chart, ChartType, set_case_chart

pytestmark = pytest.mark.module_name("Charts")


@pytest.mark.case_name("Test 1")
def test_1():
    hardpy.set_message(f"Iteration : Checking subsystem ")
    chart = Chart()
    chart.add_series(x_data=[1, 2, 3], y_data=[1, 2, 3], marker_name="a")
    chart.add_series(x_data=[1, 2, 4], y_data=[5, 4, 3], marker_name="b")
    set_case_chart(chart)


@pytest.mark.case_name("Test 2")
def test_2():
    chart = Chart(
        type=ChartType.LINE,
        title="title",
        x_label="x_label",
        y_label="y_label",
        marker_name=[None, None],
        x_data=[[1, 2], [1, 2]],
        y_data=[[3, 4], [3, 4]],
    )
    set_case_chart(chart)
    for i in range(100):
        sensor_value = random.uniform(40, 60)
        hardpy.set_message(f"temperature_{i}: {sensor_value:.1f}°C")

    sensors = {
        "temperature": [random.uniform(40, 60) for _ in range(100)],
        "voltage": [random.uniform(11.5, 12.5) for _ in range(100)],
        "current": [random.uniform(0.2, 0.3) for _ in range(100)],
        "fan_speed": [random.randint(2000, 2500) for _ in range(100)],
    }

    hardpy.set_message("All readings within normal range")
    hardpy.set_case_artifact(sensors)


@pytest.mark.case_name("Test 3 - Multiple Charts")
def test_3():
    chart1 = Chart(
        type=ChartType.LINE,
        title="Temperature Monitoring",
        x_label="Time (seconds)",
        y_label="Temperature (°C)",
        marker_name=["Sensor A", "Sensor B"],
        x_data=[[i for i in range(100)], [i for i in range(100)]],
        y_data=[
            [random.uniform(40, 60) for _ in range(100)],
            [random.uniform(35, 55) for _ in range(100)],
        ],
    )
    set_case_chart(chart1)

    hardpy.set_message("First chart: Temperature data displayed")

    chart2 = Chart(
        type=ChartType.LINE,
        title="Electrical Parameters",
        x_label="Time (seconds)",
        y_label="Value",
        marker_name=["Voltage", "Current", "Power"],
        x_data=[[i for i in range(50)], [i for i in range(50)], [i for i in range(50)]],
        y_data=[
            [random.uniform(11.5, 12.5) for _ in range(50)],
            [random.uniform(0.2, 0.3) for _ in range(50)],
            [random.uniform(2.3, 3.5) for _ in range(50)],
        ],
    )
    set_case_chart(chart2)

    hardpy.set_message("Second chart: Electrical parameters displayed")

    chart3 = Chart(
        type=ChartType.LINE,
        title="Combined Metrics",
        x_label="Measurement Cycle",
        y_label="Normalized Value",
        marker_name=["Efficiency", "Performance", "Quality"],
        x_data=[[i for i in range(30)], [i for i in range(30)], [i for i in range(30)]],
        y_data=[
            [random.uniform(0.8, 1.0) for _ in range(30)],
            [random.uniform(0.7, 0.95) for _ in range(30)],
            [random.uniform(0.85, 0.98) for _ in range(30)],
        ],
    )
    set_case_chart(chart3)

    hardpy.set_message("Third chart: Performance metrics displayed")
    hardpy.set_message("All charts successfully generated")

    system_data = {
        "timestamps": [i for i in range(100)],
        "temperature_sensor_a": [random.uniform(40, 60) for _ in range(100)],
        "temperature_sensor_b": [random.uniform(35, 55) for _ in range(100)],
        "voltage_readings": [random.uniform(11.5, 12.5) for _ in range(50)],
        "current_readings": [random.uniform(0.2, 0.3) for _ in range(50)],
    }

    hardpy.set_case_artifact(system_data)
    hardpy.set_message("Test completed with multiple charts")


@pytest.mark.case_name("Debug Messages Demonstration")
def test_debug_messages():
    """Test generates various debug messages"""
    for i in range(50):
        hardpy.set_message(f"Iteration {i+1}/50: Checking subsystem {i+1}")

    # Simulate different log levels
    if i % 10 == 1:
        hardpy.set_message("WARN: Temporary performance delays detected")
    elif i % 10 == 3:
        hardpy.set_message("ERROR: Sensor malfunction detected")

    hardpy.set_message("Demonstration completed successfully")
    hardpy.set_case_artifact({"iterations": 50, "status": "completed"})


@pytest.mark.case_name("Line chart with logarithmic X axis")
def test_line_log_x():
    """Test with logarithmic X axis"""
    chart = Chart(
        type=ChartType.LINE_LOG_X,
        title="Logarithmic X Axis",
        x_label="Log X",
        y_label="Linear Y",
    )
    x_data = [10**i for i in range(5)]
    y_data = [i**2 for i in range(5)]
    chart.add_series(x_data=x_data, y_data=y_data, marker_name="Quadratic")
    set_case_chart(chart)


@pytest.mark.case_name("Line chart with logarithmic Y axis")
def test_line_log_y():
    """Test with logarithmic Y axis"""
    chart = Chart(
        type=ChartType.LINE_LOG_Y,
        title="Logarithmic Y Axis",
        x_label="Linear X",
        y_label="Log Y",
    )
    x_data = list(range(1, 6))
    y_data = [10**i for i in range(5)]
    chart.add_series(x_data=x_data, y_data=y_data, marker_name="Exponential")
    set_case_chart(chart)


@pytest.mark.case_name("Double logarithmic chart")
def test_log_x_y():
    """Test with both logarithmic axes"""
    chart = Chart(
        type=ChartType.LOG_X_Y,
        title="Double Logarithmic Plot",
        x_label="Log X",
        y_label="Log Y",
    )
    x_data = [10**i for i in range(1, 6)]
    y_data = [10**i for i in range(1, 6)]
    chart.add_series(x_data=x_data, y_data=y_data, marker_name="Linear in log-log")
    set_case_chart(chart)


@pytest.mark.case_name("3 Graphs Test")
def test_3_graphs():
    """Test with 3 different graphs"""
    chart = Chart(
        type=ChartType.LINE,
        title="Three Graphs Comparison",
        x_label="X Values",
        y_label="Y Values",
    )

    # First graph: linear function
    x_data = list(range(1, 11))
    y_data = [x for x in x_data]
    chart.add_series(x_data=x_data, y_data=y_data, marker_name="Linear y = x")

    # Second graph: quadratic function
    y_data = [x**2 for x in x_data]
    chart.add_series(x_data=x_data, y_data=y_data, marker_name="Quadratic y = x²")

    # Third graph: exponential function
    y_data = [2**x for x in x_data]
    chart.add_series(x_data=x_data, y_data=y_data, marker_name="Exponential y = 2^x")

    set_case_chart(chart)
    hardpy.set_message("Created chart with 3 different mathematical functions")


@pytest.mark.case_name("5 Graphs Test")
def test_5_graphs():
    """Test with 5 different graphs"""
    chart = Chart(
        type=ChartType.LINE,
        title="Five Graphs Comparison",
        x_label="X Values",
        y_label="Y Values",
    )

    x_data = list(range(1, 21))

    # Different mathematical functions
    functions = [
        ("Linear", lambda x: x),
        ("Quadratic", lambda x: x**2),
        ("Square Root", lambda x: x**0.5),
        ("Logarithmic", lambda x: math.log(x) if x > 0 else 0),
        ("Sine", lambda x: math.sin(x / 2)),
    ]

    for name, func in functions:
        y_data = [func(x) for x in x_data]
        chart.add_series(x_data=x_data, y_data=y_data, marker_name=name)

    set_case_chart(chart)
    hardpy.set_message("Created chart with 5 different mathematical functions")


@pytest.mark.case_name("7 Graphs Test")
def test_7_graphs():
    """Test with 7 different graphs"""
    chart = Chart(
        type=ChartType.LINE,
        title="Seven Graphs Comparison",
        x_label="X Values",
        y_label="Y Values",
    )

    x_data = list(range(1, 15))

    # Different mathematical functions with various parameters
    functions = [
        ("Linear", lambda x: x),
        ("Quadratic", lambda x: x**2),
        ("Cubic", lambda x: x**3),
        ("Square Root", lambda x: math.sqrt(x)),
        ("Exponential", lambda x: 1.5**x),
        ("Logarithmic", lambda x: math.log(x + 1)),
        ("Sine Wave", lambda x: 2 * math.sin(x)),
    ]

    for name, func in functions:
        y_data = [func(x) for x in x_data]
        chart.add_series(x_data=x_data, y_data=y_data, marker_name=name)

    set_case_chart(chart)
    hardpy.set_message("Created chart with 7 different mathematical functions")


@pytest.mark.case_name("100 Points Test")
def test_100_points():
    """Test with 100 data points"""
    chart = Chart(
        type=ChartType.LINE,
        title="100 Data Points Chart",
        x_label="Time (ms)",
        y_label="Signal Amplitude",
    )

    # Generate 100 points with some noise
    x_data = list(range(100))
    base_signal = [math.sin(x / 10) for x in x_data]
    noise = [random.uniform(-0.2, 0.2) for _ in x_data]
    y_data = [signal + n for signal, n in zip(base_signal, noise)]

    chart.add_series(x_data=x_data, y_data=y_data, marker_name="Noisy Sine Wave")

    # Add a smoothed version
    smoothed = []
    for i in range(len(y_data)):
        if i == 0:
            smoothed.append(y_data[i])
        else:
            smoothed.append(0.8 * smoothed[i - 1] + 0.2 * y_data[i])

    chart.add_series(x_data=x_data, y_data=smoothed, marker_name="Smoothed Signal")

    set_case_chart(chart)
    hardpy.set_message(
        "Created chart with 100 data points showing noisy signal and smoothed version"
    )


@pytest.mark.case_name("Multiple Graphs with 100 Points")
def test_multiple_graphs_100_points():
    """Test with multiple graphs, each with 100 points"""
    chart = Chart(
        type=ChartType.LINE,
        title="Multiple Graphs with 100 Points Each",
        x_label="Sample Number",
        y_label="Value",
    )

    x_data = list(range(100))

    # Generate different types of signals
    signals = [
        ("Random Noise", [random.uniform(-1, 1) for _ in range(100)]),
        ("Sine Wave", [math.sin(x / 5) for x in x_data]),
        ("Ramp", [x / 50 for x in x_data]),
        ("Square Wave", [1 if x % 20 < 10 else -1 for x in x_data]),
        ("Triangle Wave", [abs((x % 20) - 10) / 5 - 1 for x in x_data]),
    ]

    for name, y_data in signals:
        chart.add_series(x_data=x_data, y_data=y_data, marker_name=name)

    set_case_chart(chart)
    hardpy.set_message(
        "Created multiple graphs with 100 points each, showing different signal types"
    )


# Добавляем импорт math для математических функций
import math
