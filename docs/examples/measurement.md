# Measurement

This is an example of how measurements can be saved in tests.

The [set_case_measurement](./../documentation/pytest_hardpy.md#set_case_measurement) function allows 
to save measurement result to database.
The code for this example can be seen inside the hardpy package
[Measurement](https://github.com/everypinio/hardpy/tree/main/examples/measurement).

### how to start

1. Launch `hardpy init measurement`.
2. Launch [CouchDB instance](../documentation/database.md#couchdb-instance).
3. Modify the files described below.
4. Launch `hardpy run measurement`.

### test_1.py

```python
import pytest

from hardpy import ComparisonOperation as CompOp, NumericMeasurement, set_case_measurement

pytestmark = pytest.mark.module_name("Numeric measurement")


@pytest.mark.case_name("Basic numeric operations")
def test_basic_numeric_operations():
    meas0 = NumericMeasurement(value=1.0)
    set_case_measurement(meas0)

    meas1 = NumericMeasurement(value=10, operation=CompOp.EQ, comparison_value=10)
    set_case_measurement(meas1)

    meas2 = NumericMeasurement(value=9, operation=CompOp.EQ, comparison_value=10)
    set_case_measurement(meas2)

    meas3 = NumericMeasurement(value=5, operation=CompOp.NE, comparison_value=3)
    set_case_measurement(meas3)

    meas4 = NumericMeasurement(value=7, operation=CompOp.GELE, lower_limit=5, upper_limit=10)
    set_case_measurement(meas4)

    assert meas1.result
    assert meas2.result, "value is not equal to 10"
    assert meas3.result
    assert meas4.result


@pytest.mark.case_name("Advanced numeric measurements")
def test_advanced_numeric_measurements():
    voltage_meas = NumericMeasurement(
        name="Voltage",
        value=1.2,
        unit="V",
        operation=CompOp.GELE,
        lower_limit=1.0,
        upper_limit=1.5,
    )
    set_case_measurement(voltage_meas)

    temperature_meas = NumericMeasurement(
        name="Temperature",
        value=23.5,
        unit="°C",
        operation=CompOp.GELE,
        lower_limit=20,
        upper_limit=25,
    )
    set_case_measurement(temperature_meas)

    percentage_meas = NumericMeasurement(
        value=98.6,
        unit="%",
        operation=CompOp.GE,
        comparison_value=95,
    )
    set_case_measurement(percentage_meas)

    minutes_meas = NumericMeasurement(
        name="Time",
        value=30,
        unit="′",
        operation=CompOp.EQ,
        comparison_value=30,
    )
    set_case_measurement(minutes_meas)

    assert all(
        [
            voltage_meas.result,
            temperature_meas.result,
            percentage_meas.result,
            minutes_meas.result,
        ],
    )


@pytest.mark.case_name("Failed numeric measurements")
def test_failed_numeric_measurements():
    high_voltage_meas = NumericMeasurement(
        name="High Voltage",
        value=15.0,
        unit="V",
        operation=CompOp.LE,
        comparison_value=12.0,
    )
    set_case_measurement(high_voltage_meas)

    low_temp_meas = NumericMeasurement(
        name="Low Temp",
        value=-10,
        unit="°C",
        operation=CompOp.GELE,
        lower_limit=0,
        upper_limit=50,
    )
    set_case_measurement(low_temp_meas)

    raw_meas = NumericMeasurement(name="Raw Value", value=42.0)
    set_case_measurement(raw_meas)

    rad_meas = NumericMeasurement(value=3.14, unit="rad")
    set_case_measurement(rad_meas)

    assert not high_voltage_meas.result, "Voltage too high"
    assert not low_temp_meas.result, "Temperature too low"
```

### test_2.py

```python
import pytest

from hardpy import (
    ComparisonOperation as CompOp,
    StringMeasurement,
    set_case_measurement,
)

pytestmark = pytest.mark.module_name("String measurement")


@pytest.mark.case_name("Basic string operations")
def test_basic_string_operations():
    meas1 = StringMeasurement(
        value="1.2.1",
        operation=CompOp.EQ,
        comparison_value="1.2.1",
    )
    set_case_measurement(meas1)

    meas2 = StringMeasurement(
        value="ABC",
        operation=CompOp.EQ,
        comparison_value="abc",
    )
    set_case_measurement(meas2)

    meas3 = StringMeasurement(
        value="ABC",
        operation=CompOp.EQ,
        casesensitive=False,
        comparison_value="abc",
    )
    set_case_measurement(meas3)

    assert meas1.result
    assert not meas2.result
    assert meas3.result


@pytest.mark.case_name("Advanced string measurements")
def test_advanced_string_measurements():
    simple_str_meas = StringMeasurement(
        value="abc", operation=CompOp.EQ, comparison_value="abc"
    )
    set_case_measurement(simple_str_meas)

    serial_meas = StringMeasurement(
        name="Serial Number",
        value="SN123456",
        operation=CompOp.NE,
        comparison_value="SN000000",
    )
    set_case_measurement(serial_meas)

    failed_str_meas = StringMeasurement(
        name="Wrong Code", value="FAIL", operation=CompOp.EQ, comparison_value="PASS"
    )
    set_case_measurement(failed_str_meas)

    info_meas = StringMeasurement(value="INFO")
    set_case_measurement(info_meas)

    assert simple_str_meas.result
    assert serial_meas.result
    assert not failed_str_meas.result, "Wrong status code"
```

### test_3.py

```python
import pytest

from hardpy import (
    ComparisonOperation as CompOp,
    NumericMeasurement,
    set_case_measurement,
)

pytestmark = pytest.mark.module_name("All comparison operations test")


@pytest.mark.case_name("Operation types with brackets")
def test_all_operation_types_with_brackets():
    meas_lt = NumericMeasurement(value=4, operation=CompOp.LT, comparison_value=5)
    set_case_measurement(meas_lt)

    meas_gelt = NumericMeasurement(
        value=3,
        operation=CompOp.GELT,
        lower_limit=2,
        upper_limit=4,
    )
    set_case_measurement(meas_gelt)

    meas_legt = NumericMeasurement(
        value=1,
        operation=CompOp.LEGT,
        lower_limit=2,
        upper_limit=4,
    )
    set_case_measurement(meas_legt)

    assert meas_lt.result
    assert meas_gelt.result
    assert meas_legt.result


@pytest.mark.case_name("Edge cases with units")
def test_edge_cases_with_units():
    meas_percent = NumericMeasurement(
        name="Efficiency",
        value=95.5,
        unit="%",
        operation=CompOp.GELE,
        lower_limit=90,
        upper_limit=100,
    )
    set_case_measurement(meas_percent)

    meas_degrees = NumericMeasurement(
        name="Angle",
        value=45,
        unit="°",
        operation=CompOp.GTLT,
        lower_limit=0,
        upper_limit=90,
    )
    set_case_measurement(meas_degrees)

    meas_minutes = NumericMeasurement(
        name="Duration",
        value=30,
        unit="′",
        operation=CompOp.LE,
        comparison_value=60,
    )
    set_case_measurement(meas_minutes)

    meas_voltage = NumericMeasurement(
        name="Voltage",
        value=3.3,
        unit="V",
        operation=CompOp.GELT,
        lower_limit=3.0,
        upper_limit=3.6,
    )
    set_case_measurement(meas_voltage)

    assert meas_percent.result
    assert meas_degrees.result
    assert meas_minutes.result
    assert meas_voltage.result


@pytest.mark.case_name("Boundary value tests")
def test_boundary_value_tests():
    meas_gt_boundary = NumericMeasurement(
        value=2.1,
        operation=CompOp.GTLT,
        lower_limit=2,
        upper_limit=4,
    )
    set_case_measurement(meas_gt_boundary)

    meas_ge_boundary = NumericMeasurement(
        value=2,
        operation=CompOp.GELE,
        lower_limit=2,
        upper_limit=4,
    )
    set_case_measurement(meas_ge_boundary)

    meas_mixed_boundary = NumericMeasurement(
        value=4,
        operation=CompOp.GTLE,
        lower_limit=2,
        upper_limit=4,
    )
    set_case_measurement(meas_mixed_boundary)

    assert meas_gt_boundary.result
    assert meas_ge_boundary.result
    assert meas_mixed_boundary.result
```
