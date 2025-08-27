# Measurement

This is an example of how measurements can be saved in tests.

The [set_measurement](./../documentation/pytest_hardpy.md#set_measurement) function allows 
to save measurement result to database.
The code for this example can be seen inside the hardpy package
[Measurement](https://github.com/everypinio/hardpy/tree/main/examples/measurement).

### how to start

1. Launch `hardpy init measurement`.
2. Launch [CouchDH instance](../documentation/database.md#couchdb-instance).
3. Modify the files described below.
4. Launch `hardpy run measurement`.

### test_1.py

```python
import pytest

from hardpy import ComparisonOperation as CompOp, NumericMeasurement, set_measurement, set_message

pytestmark = pytest.mark.module_name("Numeric measurement")

@pytest.mark.case_name("Test 1")
def test_1():
    meas0 = NumericMeasurement(value=1.0)
    set_measurement(meas0)
    set_message(f"{meas0.value}")
    meas1 = NumericMeasurement(value=10, operation=CompOp.EQ, comparison_value=10)
    set_measurement(meas1)
    meas2 = NumericMeasurement(value=9, operation=CompOp.EQ, comparison_value=10)
    set_measurement(meas2)
    assert meas1.result
    assert meas2.result, "value is not equal to 10"

@pytest.mark.case_name("Test 2")
def test_2():
    meas = NumericMeasurement(value=5, operation=CompOp.NE, comparison_value=3)
    set_measurement(meas)
    assert meas.result

@pytest.mark.case_name("Test 3")
def test_3():
    meas = NumericMeasurement(value=7, operation=CompOp.GELE, lower_limit=5, upper_limit=10)
    set_measurement(meas)
    assert meas.result
```

### test_2.py

```python
import pytest

from hardpy import ComparisonOperation as CompOp, StringMeasurement, set_measurement

pytestmark = pytest.mark.module_name("String measurement")

@pytest.mark.case_name("Test 1")
def test_1():
    meas1 = StringMeasurement(value="1.2.1", operation=CompOp.EQ, comparison_value="1.2.1")
    set_measurement(meas1)
    assert meas1.result

    meas2 = StringMeasurement(value="ABC", operation=CompOp.EQ, comparison_value="abc")
    meas3 = StringMeasurement(value="ABC", operation=CompOp.EQ, casesensitive=False, comparison_value="abc")
    assert not meas2.result
    assert meas3.result
```
