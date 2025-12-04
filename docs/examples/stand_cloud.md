# StandCloud

This is an example of using **pytest-hardpy** functions, storing
the result to [StandCloud](./../documentation/stand_cloud.md).
This example is similar to [Minute parity](./minute_parity.md),
but the test results are stored in StandCloud instead of CouchDB.
The code for this example can be seen inside the hardpy package
[StandCloud](https://github.com/everypinio/hardpy/tree/main/examples/stand_cloud).

After testing is complete, data is sent to **StandCloud** by setting the 
`autosync` to `true` in the **[stand_cloud]** section of the **hardpy.toml** file, 
and by setting the value of the `api_key` variable.
If there is no connection to **StandCloud**, **HardPy** will attempt to send data 
to **StandCloud** at the specified `autosync_timeout` interval (in minutes).

### how to start

1. Login to [standcloud.io](https://standcloud.io).
2. Create a company or login to an existing one.
3. Create and copy the API key.
4. Launch `hardpy init stand_cloud --sc-api-key <your_api_key> --sc-autosync` 
   or `hardpy init stand_cloud` and manually modify the 
   **[stand_cloud]** section in **hardpy.toml**.
5. Launch [CouchDB instance](../documentation/database.md#couchdb-instance).
6. Modify the files described below. Copying the **hardpy.toml** file will 
   suffice for sending data to **StandCloud** after testing.
7. Launch `hardpy run stand_cloud`.

### hardpy.toml

```toml
title = "HardPy TOML config"
tests_name = "StandCloud"

[database]
user = "dev"
password = "dev"
host = "localhost"
port = 5984

[frontend]
host = "localhost"
port = 8000
language = "en"
full_size_button = false
sound_on = true
measurement_display = true
manual_collect = false

[frontend.modal_result]
enable = true
auto_dismiss_pass = true
auto_dismiss_timeout = 5

[stand_cloud]
address = "standcloud.io"
connection_only = false
autosync = false
autosync_timeout = 30
api_key = "<your_api_key>"
```

### conftest.py

Contains settings and fixtures for all tests:

- The example of devices used as a fixture in `driver_example`;

```python
import pytest
from driver_example import DriverExample

@pytest.fixture(scope="session")
def driver_example():
    example = DriverExample()
    yield example
```

### driver_example.py

An example of writing a simple device driver.
The driver returns the current minute in the OS.

```python
import datetime

class DriverExample:
    @property
    def current_minute(self):
        current_time = datetime.datetime.now()
        return int(current_time.strftime("%M"))
```

### test_1.py

Contains tests related to preparation for the testing process:

- The name of the test module for the web interface is set to `pytest.mark.module_name`;
- The name of the test cases for the web interface is set to `pytest.mark.case_name`;
- The device under test (DUT) info is stored in the database in `test_dut_info`;
- The test stand info is store in the database in `test_stand_info`;

```python
from uuid import uuid4
import pytest
import hardpy

pytestmark = pytest.mark.module_name("Testing preparation")

@pytest.mark.case_name("Process info")
def test_process_info():
    hardpy.set_process_name("Acceptance Test")
    hardpy.set_process_number(1)

    process_info = {"stage": "production", "version": "1.0"}
    hardpy.set_process_info(process_info)


@pytest.mark.case_name("Batch info")
def test_batch_info():
    hardpy.set_batch_serial_number("batch_1")


@pytest.mark.case_name("DUT info")
def test_dut_info():
    serial_number = str(uuid4())[:6]
    hardpy.set_dut_serial_number(serial_number)
    hardpy.set_message(f"Serial number: {serial_number}")
    hardpy.set_dut_part_number("part_number_1")
    hardpy.set_dut_name("Test Device")
    hardpy.set_dut_type("PCBA")
    hardpy.set_dut_revision("REV1.0")

    info = {"sw_version": "1.0.0"}
    hardpy.set_dut_info(info)

@pytest.mark.case_name("Sub unit info")
def test_sub_unit_info():
    hardpy.set_dut_sub_unit(
        hardpy.SubUnit(
            serial_number=str(uuid4())[:6],
            part_number="part_number_1",
            type="PCBA",
            revision="REV2.0"
        )
    )

@pytest.mark.case_name("Test stand info")
def test_stand_info():
    test_stand_name = "Stand 1"
    hardpy.set_stand_name(test_stand_name)
    hardpy.set_stand_location("Moon")
    hardpy.set_stand_number(2)
    hardpy.set_stand_revision("HW1.0")

    stand_info = {"some_info": "123", "release": "1.0.0", "calibration_due": "2023-12-31"}
    hardpy.set_stand_info(stand_info)
    hardpy.set_message(f"Stand name: {test_stand_name}")
    assert True
```

### test_2.py

Contains basic tests:

- The name of the test module for the web interface is set to `pytest.mark.module_name`;
- The name of the test cases for the web interface is set to `pytest.mark.case_name`;
- An example of using a driver to get the current minute in `test_minute_parity`;
- An example of saving a test case measurement to the database using `set_case_measurement` 
  and `NumericMeasurement`;
- An example of using `ErrorCode`.

```python
import pytest
from driver_example import DriverExample

import hardpy

pytestmark = pytest.mark.module_name("Main tests")

@pytest.mark.case_name("Minute check")
def test_minute_parity(driver_example: DriverExample):
    minute = driver_example.current_minute
    result = minute % 2
    hardpy.set_case_measurement(hardpy.NumericMeasurement(value=minute, name="Current minute"))
    error_code = 1
    error_msg = f"The test failed because {minute} is odd! Try again!"
    assert result == 0, hardpy.ErrorCode(error_code, error_msg)
```

### test_3.py

Contains the final tests of the testing process:

- The name of the test module for the web interface is set to `pytest.mark.module_name`;
- The name of the test cases for the web interface is set to `pytest.mark.case_name`;
- An example of setting and updating a message for a web interface using `set_message`;
- `test_3` depends on `test_minute_parity` from `test_2`.
Dependency is set to `pytest.mark.dependency`.
If `test_2::test_minute_parity` fails, `test_3` will be skipped

```python
from time import sleep
import pytest
import hardpy

pytestmark = [
    pytest.mark.module_name("End of testing"),
    pytest.mark.dependency("test_2::test_minute_parity"),
]

@pytest.mark.case_name("Final case")
def test_one():
    for i in range(5, 0, -1):
        hardpy.set_message(f"Time left until testing ends {i} s", "updated_status")
        sleep(1)
    hardpy.set_message("Testing ended", "updated_status")
    assert True
```

### manual StandCloud syncronization

If you want to control the sending of reports to **StandCloud** yourself, 
the following code, which you can add to `conftest.py`, will allow you to do so.

Remember to also set `autosync=false` in the stand_cloud section of 
the **hardpy.toml** file.


```python
# conftest.py
from http import HTTPStatus

import pytest
from driver_example import DriverExample

from hardpy import (
    StandCloudError,
    StandCloudLoader,
    get_current_report,
    set_operator_message,
)

@pytest.fixture(scope="session")
def driver_example():
    example = DriverExample()
    yield example

def finish_executing():
    report = get_current_report()
    if report:
        try:
            loader = StandCloudLoader()
            response = loader.load(report)
            if response.status_code != HTTPStatus.CREATED:
                set_operator_message(
                    "Report not uploaded to StandCloud, "
                    f"status code: {response.status_code}, text: {response.text}",
                )
        except StandCloudError as exc:
            set_operator_message(f"{exc}")

@pytest.fixture(scope="session", autouse=True)
def fill_actions_after_test(post_run_functions: list):
    post_run_functions.append(finish_executing)
    yield
```
