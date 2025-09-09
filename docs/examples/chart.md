# Chart

This is an example of how charts can be saved in tests.

The [set_case_chart](./../documentation/pytest_hardpy.md#set_case_chart) function allows 
to save chart (data series) result to database.

### how to start

1. Launch `hardpy init charts`.
2. Launch [CouchDB instance](../documentation/database.md#couchdb-instance).
3. Modify the files described below.
4. Launch `hardpy run charts`.

### test_1.py

```python
import pytest

from hardpy import Chart, ChartType, set_case_chart

pytestmark = pytest.mark.module_name("Charts")

@pytest.mark.case_name("Line chart")
def test_line_chart():
    chart = Chart(
        type=ChartType.LINE,
        title="title",
        x_label="x_label",
        y_label="y_label",
        marker_name=[None, None],
        x_data=[ [1, 2], [1, 2] ],
        y_data=[ [3, 4], [3, 4] ],
    )
    set_case_chart(chart)

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


@pytest.mark.case_name("Line chart with logarithmic Y axis")
def test_line_log_y():
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
```
