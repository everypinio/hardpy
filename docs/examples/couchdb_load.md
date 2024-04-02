# Couchdb load

This is an example of storing the test result in CouchDB.
Test reports are written to the **report** database at the end of the testing process via **CouchdbLoader**.

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

- The function of generating a report and recording it in the database `save_report_to_couchdb`;
- The list of actions that will be performed after testing is filled in function `fill_actions_after_test`;

```python
import pytest

from hardpy import (
    CouchdbLoader,
    CouchdbConfig,
    get_current_report,
)

def save_report_to_couchdb():
    report = get_current_report()
    if report:
        loader = CouchdbLoader(CouchdbConfig())
        loader.load(report)

@pytest.fixture(scope="session", autouse=True)
def fill_actions_after_test(post_run_functions: list):
    post_run_functions.append(save_report_to_couchdb)
    yield
```

### test_example_1.py

Contains two simple examples of a valid test.

```python
import pytest

def test_one():
    assert True

def test_two():
    assert True
```

### test_example_2.py

Contains two simple examples: a valid test and an invalid test.

```python
import pytest

def test_three():
    assert True

def test_four():
    assert False
```
