# Minute parity

This is an example of using **pytest-hardpy** functions, storing the result to CouchDB and writing a simple driver.

### how to start

1. Launch [CouchDH instance](../documentation/database.md#couchdb-instance).
2. Create a directory `<dir_name>` with the files described below.
3. Launch `hardpy-panel <dir_name>`.

### pytest.ini

It is a file of built-in configuration options that determine how live logging works and 
enable **pytest-hardpy** plugin for launching via pytest.

```ini
[pytest]
log_cli = true
log_cli_level = INFO
log_cli_format = %(asctime)s [%(levelname)s] %(message)s
log_cli_date_format = %H:%M:%S
addopts = --hardpy-pt
```

### conftest.py

Contains settings and fixtures for all tests:

- The function of generating a report and recording it in the database `finish_executing`;
- The example of devices used as a fixture in `driver_example`;
- The list of actions that will be performed after testing is filled in function `fill_actions_after_test`;
- The module log is created in fixture `module_log`;

```python
import logging
import pytest

from hardpy import (
    CouchdbLoader,
    CouchdbConfig,
    get_current_report,
)
from driver_example import DriverExample

@pytest.fixture(scope="module")
def module_log(request):
    log_name = request.module.__name__
    yield logging.getLogger(log_name)

@pytest.fixture(scope="session")
def driver_example():
    example = DriverExample()
    yield example
    example.random_method()

def finish_executing():
    report = get_current_report()
    if report:
        loader = CouchdbLoader(CouchdbConfig())
        loader.load(report)

@pytest.fixture(scope="session", autouse=True)
def fill_actions_after_test(post_run_functions: list):
    post_run_functions.append(finish_executing)
    yield
```

### driver_example.py

An example of writing a simple device driver.
The driver returns the current minute in the OS.

```python
import datetime
from logging import getLogger

class DriverExample(object):
    def __init__(self):
        self._log = getLogger(__name__)

    @property
    def current_minute(self):
        current_time = datetime.datetime.now()
        return int(current_time.strftime("%M"))

    def random_method(self):
        self._log.warning("Random method")
```

### test_1.py

Contains tests related to preparation for the testing process:

- The name of the test module for the web interface is set to `pytest.mark.module_name`;
- The name of the test cases for the web interface is set to `pytest.mark.case_name`;
- The device under test (DUT) info is stored in the database in `test_dut_info`;
- The test stand info is store in the database in `test_stand_info`;

```python
import logging
from uuid import uuid4

import pytest
import hardpy

pytestmark = pytest.mark.module_name("Testing preparation")

@pytest.mark.case_name("DUT info")
def test_dut_info(module_log: logging.Logger):
    serial_number = str(uuid4())[:6]
    module_log.info(f"DUT serial number {serial_number}")
    hardpy.set_dut_serial_number(serial_number)
    info = {"batch": "test_batch", "board_rev": "rev_1"}
    hardpy.set_dut_info(info)
    assert True

@pytest.mark.case_name("Test stand info")
def test_stand_info(module_log: logging.Logger):
    test_stand_name = "Stand 1"
    module_log.info(f"Stand name: {test_stand_name}")
    info = {"name": "Test stand 1"}
    hardpy.set_stand_info(info)
    assert True
```

### test_2.py

Contains basic tests:

- The name of the test module for the web interface is set to `pytest.mark.module_name`;
- The name of the test cases for the web interface is set to `pytest.mark.case_name`;
- An example of using a driver to get the current minute in `test_minute_parity`;
- An example of saving a test case artifact to the database using `set_case_artifact`;

```python
import pytest
import hardpy

from driver_example import DriverExample

pytestmark = pytest.mark.module_name("Main tests")

@pytest.mark.case_name("Minute check")
def test_minute_parity(driver_example: DriverExample):
    minute = driver_example.current_minute
    hardpy.set_message(f"Current minute {minute}")
    result = minute % 2
    data = {"minute": minute}
    hardpy.set_case_artifact(data)
    assert (result == 0), f"The test failed because {minute} is odd! Try again!"
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
