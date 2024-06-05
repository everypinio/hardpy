# pytest-hardpy

**pytest-hardpy** is a pytest plugin that helps you save test data in a
database for test reporting and viewing test data in the web interface.

## Plugin registration

To use the **pytest-hardpy** you need to enable it.
You can do this via the `pytest.ini` file.

**Example:**

```ini
# pytest.ini
[pytest]
addopts = --hardpy-pt
```

Another way to enable a plugin without `pytest.ini` file is to run tests with the option `--hardpy-pt`.

```bash
pytest --hardpy-pt tests
```

If tests are run via [hardpy-panel](hardpy_panel.md), then the pytest-hardpy plugin will be enabled for tests by default.

## Functions

#### set_dut_info

This function records a dictionary containing information about the test stand.
When called again, the information will be added to DB.

**Arguments:**

- `info` *(dict)*: DUT info

**Example:**

```python
def test_dut_info():
    set_dut_info({"batch": "test_batch", "board_rev": "rev_1"})
```
#### set_dut_serial_number

Writes a string with a serial number.
When called again, the Exception DuplicateSerialNumberError will be caused.

**Arguments:**

- `serial_number` *(str)*: DUT serial number

**Example:**

```python
def test_serial_number():
    set_dut_serial_number("1234")
```

#### set_stand_info

Writes a dictionary with information about the test stand.
When called again, the information will be added to DB.

**Arguments:**

- `info` *(dict)*: test stand info

**Raises**

- `DuplicateSerialNumberError`: if serial number is already set

**Example:**

```python
def test_stand_info():
    set_stand_info({"name": "Test stand 1"})
```

#### set_case_artifact

Writes a dictionary with a test case artifact.
When called again, the data will be added to DB.

Artifacts are saved only in the **runstore** database
because the state in **statestore** and case artifact must be separated.

**Arguments:**

- `data` *(dict)*: data

**Example:**

```python
def test_case_artifact():
    set_case_artifact({"data_str": "123DATA"})
```

#### set_module_artifact

Writes a dictionary with a module test artifact.
When called again, the data will be added to DB.

Artifacts are saved only in the **runstore** database
because the state in **statestore** and module artifact must be separated.

**Arguments:**

- `data` *(dict)*: data

**Example:**

```python
def test_module_artifact():
    set_module_artifact({"data_str": "456DATA"})
```

#### set_run_artifact

Writes a dictionary with a test run artifact.
When called again, the data will be added to DB.

Artifacts are saved only in the **runstore** database
because the state in **statestore** and run artifact must be separated.

**Arguments:**

- `data` *(dict)*: data

**Example:**

```python
def test_run_artifact():
    set_run_artifact({"data_str": "789DATA"})
```

#### set_driver_info

The function records a dictionary containing information about the driver.
The data is updated with new information each time the function is called.

Driver data is stored in both **statestore** and **runstore** databases.

**Arguments:**

- `drivers` *(dict)*: A dictionary of drivers, where keys are driver names and values are driver-specific data.

**Example:**

```python
def test_driver_info():
    drivers = {
        "driver_1": {
            "name": "Driver A",
            "type": "network"
        }
    }
    set_driver_info(drivers)
```

#### set_message

Writes a string with a message.
If a message is sent without a key, the key will be generated automatically and the messages will be appended.
If the message is sent with a known key, it will be updated.

**Arguments:**

- `msg` *(str)*: Message content.
- `msg_key` *(Optional[str])*: Message ID. If not specified, a random ID will be generated.

**Example:**

```python
def test_message():
    set_message("Test message")
    set_message("Update message 1", "msg_upd")
    set_message("Update message 2", "msg_upd")
```

#### get_current_report

Returns the current report from the database **runstore**.

**Returns:**

- *(ResultRunStore | None)*: report, or None if not found or invalid

**Example:**

```python
def test_current_report():
    report = get_current_report()
```

## Class

#### CouchdbLoader

Used to write reports to the database **CouchDB**.

**Example:**

```python
# conftest
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

## Fixture

#### post_run_functions

To execute actions at the end of testing, you can use the fixture **post_run_functions**.
This fixture is a `list[Callable]` and you can write functions into it that must be executed at the end of testing.

Fill this list in conftest.py and functions from this list will be called after tests run (at the end of pytest_sessionfinish).

**Returns:**

- *(list[Callable])*: list of post run methods

**Example:**

```python
# conftest.py file
def finish_executing():
    print("Pytest finished")


@pytest.fixture(scope="session", autouse=True)
def fill_actions_after_test(post_run_functions: list):
    post_run_functions.append(finish_executing)
    yield
```

## Marker

#### case_name

Sets a text name for the test case (default: function name)

**Example:**

```python
@pytest.mark.case_name("Simple case 1")
def test_one():
    assert 42 == 42
```

#### module_name

Sets a text name for the test module (file) (default: module name)

**Example:**

```python
pytestmark = pytest.mark.module_name("Module 1")
```

#### dependency

Skips the test case/module if the main test fails/skipped/errored.

**Example:**

```python
#test_1.py
def test_one():
    assert False

@pytest.mark.dependency("test_1::test_one")
def test_two():
    assert True
```

## Options

**pytest-hardpy** has several options to run:

#### hardpy_pt

Option to enable the **pytest-hardpy** plugin.

```bash
--hardpy-pt
```

#### db_user

The CouchDB instance user name for the **statestore** and **runstore** databases.
The default is *dev*.

```bash
--hardpy-dbu DB_USER
```

#### db_pswd

The CouchDB instance password for the **statestore** and **runstore** databases.
The default is *dev*.

```bash
--hardpy-dbpw DB_PSWD
```

#### db_port

The CouchDB instance port number for the **statestore** and **runstore** databases.
The default is *5984*.

```bash
--hardpy-dbp DB_PORT
```

#### db_host

The CouchDB instance hostname for the **statestore** and **runstore** databases.
The default is *localhost*.

```bash
--hardpy-dbh DB_HOST
```
