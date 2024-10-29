# Couchdb load

This is an example of storing the test result in CouchDB.
Test reports are written to the **report** database at the end of 
the testing process via **CouchdbLoader**.
The code for this example can be seen inside the hardpy package 
[CouchDB Load](https://github.com/everypinio/hardpy/tree/main/examples/couchdb_load).

### how to start

1. Launch `hardpy init couchdb_load`.
2. Launch [CouchDH instance](../documentation/database.md#couchdb-instance).
3. Modify the files described below.
4. Launch `hardpy run couchdb_load`.

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

### test_1.py

Contains two simple examples of a valid test.

```python
def test_one():
    assert True

def test_two():
    assert True
```

### test_2.py

Contains two simple examples: a valid test and an invalid test.

```python
def test_three():
    assert True

def test_four():
    raise AssertionError
```
