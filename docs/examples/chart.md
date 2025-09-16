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

@pytest.mark.case_name("Test 1")
def test_1():
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
        x_data=[ [1, 2], [1, 2] ],
        y_data=[ [3, 4], [3, 4] ],
    )
    set_case_chart(chart)
```
