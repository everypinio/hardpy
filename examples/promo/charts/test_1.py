import pytest

from hardpy import Chart, ChartType, set_case_chart

pytestmark = pytest.mark.module_name("Charts")


@pytest.mark.case_name("Multiple charts")
def test_multiple_charts():
    chart = Chart()
    chart.add_series(x_data=[1, 2, 3], y_data=[1, 2, 3], marker_name="a")
    chart.add_series(x_data=[1, 2, 4], y_data=[5, 4, 3], marker_name="b")
    set_case_chart(chart)


@pytest.mark.case_name("Line chart with logarithmic X axis")
def test_line_log_x():
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
