# Features

## Operator panel

### Viewing tests in the operator panel

The operator panel allows you to view the test hierarchy with **test folder/test file/function** levels.
An example of its use can be found on page [Jig panel](./../documentation/jig_panel.md).
User can launch operator panel using [jig run](./../documentation/cli.md#jig-run) command.

<h1 align="center">
    <img src="https://raw.githubusercontent.com/everypinio/jig/main/docs/img/jig_panel.gif" alt="jig panel" style="width:600;">
</h1>

### Interacting with tests in the operator panel

The user can interact with the tests through dialog boxes in the operator panel.
**Jig** provides the ability to enter [text](./../documentation/jig_panel.md#text-input-field) or
[numbers](./../documentation/jig_panel.md#number-input-field), make selections using
[checkboxes](./../documentation/jig_panel.md#checkbox) or
[radio buttons](./../documentation/jig_panel.md#radiobutton),
guide the user through [multiple steps](./../documentation/jig_panel.md#multiple-steps)
in a single window, display [images](./../documentation/pytest_jig.md#imagecomponent) to the user,
and insert [HTML components](./../documentation/pytest_jig.md#htmlcomponent) into the dialog box using iframes.

In dialog boxes, the user must confirm their action by clicking the **Confirm** button.
Closing the dialog box prematurely will abort the test.

If the user only needs to provide information, an
[operator message](./../documentation/jig_panel.md#operator-message) can be used.
Unlike dialog boxes, the user cannot enter any information, only close the window.
User can also close the operator message from within the test code and run it in non-blocking mode,
so that displaying the window does not stop the test.

### Operator panel language

The user can set one of the following operator panel languages ​​via the *jig.toml*.
Available languages are [there](./../documentation/jig_panel.md#languages).

The example of file:

```toml
[frontend]
language = "zh"
```

### Full-size start/stop button

**Jig** provides a full-size start/stop button layout option for improved usability across different devices and use cases.

**Configuration**:
Enable the full-size button in your `jig.toml`:

```toml
[frontend]
full_size_button = true
```

### Test completion modal results

**Jig** provides configurable modal result windows that display test completion status with detailed information:

- **PASS results**: Green modal with auto-dismiss functionality
- **FAIL results**: Red modal showing detailed failed test cases list
- **STOP results**: Yellow modal displaying stopped test case information

**Configuration Options** in `jig.toml`:
```toml
[frontend.modal_result]
enable = true
auto_dismiss_pass = true
auto_dismiss_timeout = 5
```

**Features**:

- **Auto-dismiss**: PASS results automatically close after configurable timeout.
- **Manual dismissal**: Click anywhere or press any key to close modal.
- **Detailed reporting**: Failed test cases show module names, case names, and assertion messages.
- **Keyboard integration**: Space key handling respects modal visibility states.
- **Responsive design**: Adapts to different screen sizes with optimal readability.

### Sound notifications

**Jig** provides configurable sound notifications for test completion events.
Users can enable audio feedback when tests reach completion status (PASS/FAIL/STOP).

**Configuration**:
Enable sound notifications in your `jig.toml`:

```toml
[frontend]
sound_on = true
```

### Manual test selection

**Jig** supports manual test selection, allowing operators to choose specific test cases
to run instead of executing the entire test plan.

**Key capabilities**:

- **Checkbox-based selection**: Each test case and module displays checkboxes for selection
- **Bulk operations**: Select or deselect all tests in a module with a single checkbox
- **Visual feedback**: Selected tests are marked for execution, non-selected tests are skipped

**Workflow**:

1. Enable manual collect mode in settings menu
2. Select desired tests using checkboxes
3. Disable manual collect mode
4. Start test execution - only selected tests will run

**Configuration**:
Enable manual test selection in your `jig.toml`:

```toml
[frontend]
manual_collect = true
```

### Test history

The operator panel provides a test history view that allows operators to browse results of previous test runs.

**Features**:

- **History List**: View a chronological list of past test executions.
- **Detailed Results**: Click on a history entry to see the specific test results, including status and measurements for each test case.

<h1 align="center">
    <img src="https://raw.githubusercontent.com/everypinio/jig/main/docs/img/test_history.png" alt="test history">
</h1>

**Configuration**:

The test history feature is disabled by default. 
You can disable it in your `jig.toml`:

```toml
[frontend]
test_history = true
```

## CLI

### Creating template project

The **Jig** can create template project using the [jig init](./../documentation/cli.md#jig-init)
command. An example of usage can be found in the **how to init** section among the examples, e.g. in
[minute parity](./../examples/minute_parity.md#how-to-start).

```bash
jig init minute_parity
```

### Running the Jig server

Based on pytest **Jig** allows you to run pytest tests in the browser or from the command line.
To run the **Jig** server and view tests in the browser, execute the 
[jig run](./../documentation/cli.md#jig-run) command.

```bash
jig run <project_path>
```

For example:

```bash
jig run examples/minute_parity 
```

### Starting the tests

The user can start the operator panel with the **Start** button.
As an alternative, the user can start the tests using the 
[jig start](./../documentation/cli.md#jig-start) command.

```bash
jig start <project_path>
```

For example:

```bash
jig start examples/minute_parity 
```

Through the CLI, the user can start **Jig** 
[with arguments](./../documentation/cli.md#jig-start) that will be used during testing.

```bash
jig start --arg device_id=123 --arg operator_name=user examples/minute_parity 
```

The user can also start the tests using **pytest**.

```bash
python -m pytest
```

### Stopping the tests

The user can stop the tests during execution from the operator panel by clicking on the **Stop** button
or using the [jig stop](./../documentation/cli.md#jig-stop) command.
It is possible to stop tests from the console by sending an interrupt, e.g. “Ctrl-C” in Linux.

### Checking the status of tests

The user can check the status of tests using the [jig status](./../documentation/cli.md#jig-status) command.

## Database

### Storing test result in database

**Jig** allows you to run tests with a running [CouchDB](https://couchdb.apache.org/) database.
This is a NoSQL database that ensures that the results of the current test run are committed,
even if the tests are aborted early.

To save the report history, the user must configure the **conftest.py** file using the
[CouchdbLoader](./../documentation/pytest_jig.md#couchdbloader) or another adapter to save the data.
By default, only the current report in the [runstore](./../documentation/database.md#runstore-scheme)
database is stored in **CouchDB**.

The test report format (database scheme) is described in the
[database runstore](./../documentation/database.md#runstore-scheme) section.

An example of configuring **conftest.py** to store test run history can be found in several examples,
including the [couchdb_load](./../examples/couchdb_load.md) and
[minute_parity](./../examples/minute_parity.md).

### JSON

With **Jig**, you can run tests without a database and save the test data to local JSON documents. 
These documents have a structure similar to that of databases and documents in **CouchDB**. 
A .jig/storage folder is created by default in the project folder, 
where test reports can be found in the **runstore** folder.

An example of its use can be found on page [JSON storage](./../examples/json_storage.md).

### Other databases

In order to save data to other databases, users will need to write their own adapter class to convert their 
Jig [runstore schema](./../documentation/database.md#runstore-scheme) data into a suitable format.
Next, the user should call their adapter class in the same way that [CouchdbLoader](./../documentation/pytest_jig.md#couchdbloader) 
is called in the [couchdb_load](./../examples/couchdb_load.md) and
[minute_parity](./../examples/minute_parity.md) examples.

## Pytest markers

### Running multiple test attempts

The **Jig** allows the user to attach an [attempt](./../documentation/pytest_jig.md#attempt)
marker to a test, which allows the test to be repeated as many times as specified in
the marker's content in the event of failure.

### Skipping the tests

The **Jig** allows the user to skip tests on [dependency](./../documentation/pytest_jig.md#dependency)
markers.
The user can specify that a test or an entire module depends on another test.
In this way, tests can be defined whose failure will prevent the marked tests from running.
The user can also create a dependency on several test cases or modules.
If the name of the dependency does not exist, the test will be started.

```python
#test_1.py
import pytest

def test_a():
    assert False

@pytest.mark.dependency("test_1::test_a")
def test_b():
    assert True
```

```python
#test_2.py
import pytest

pytestmark = pytest.mark.dependency("test_1")

def test_a():
    assert False

def test_b():
    assert True

@pytest.mark.dependency("test_2::test_a")
@pytest.mark.dependency("test_2::test_b")
def test_c():
    assert True
```

An example of its use can be found on page [skip test](./../examples/skip_test.md).

### Critical tests

The **Jig** allows the user to skip subsequent tests marked as [critical](./../documentation/pytest_jig.md#critical)
marker, if a critical test fails or is skipped.
The user can designate individual tests or entire modules as critical.
If a test case is marked as critical, its failure will skip all remaining tests in the current and subsequent modules.  
If an entire module is marked as critical, the failure of any test within it will skip all remaining tests in that module and subsequent modules.  

**Example (test level):**

```python
@pytest.mark.critical
def test_a():
    assert False

def test_b():
    assert True
```

**Example (module level):**

```python
pytestmark = pytest.mark.critical

def test_c():
    assert True
```

An example of its use can be found on page [critical](./../examples/critical_test.md).

### Test case and test module grouping

The **Jig** allows users to organize tests into logical groups: `setup`, `main`, and `teardown`.
This grouping helps structure test execution flow and reporting.

Users can designate individual tests or entire modules with specific groups.
By default, all tests are in the `main` group.

**Example (test case level):**

```python
import pytest
from jig.pytest_jig.utils.const import Group

@pytest.mark.case_group(Group.SETUP)
def test_setup_case():
    # This test will be executed first as part of setup
    assert initialize_system()

@pytest.mark.case_group(Group.MAIN)
def test_main_functionality():
    # This is a main test case
    assert check_system_operation()

@pytest.mark.case_group(Group.TEARDOWN)
def test_cleanup():
    # This test will clean up after execution
    assert cleanup_resources()
```

**Example (module level):**

```python
import pytest
from jig.pytest_jig.utils.const import Group

# All tests in this module will be teardown tests
pytestmark = pytest.mark.module_group(Group.TEARDOWN)

def test_cleanup_database():
    assert clear_database_tables()

def test_release_resources():
    assert free_allocated_memory()

def test_generate_final_report():
    assert create_execution_summary()
```

An example of its use can be found on page [test grouping documentation](./../documentation/pytest_jig.md#case_group).

## Logging approaches in Jig

**Jig** provides several methods for logging and user interaction during testing.
Choose the appropriate method based on whether you need to store information in the
database or just display messages to the operator.

### Database logging with set_message

The [set_message](./../documentation/pytest_jig.md#set_message) function stores the log message in the report.
Messages without specified keys get auto-generated keys, while known keys update existing messages.
Perfect for tracking test progress, recording measurements, system states, and verification results.

```python
def test_temperature_sensor():
    temp = read_temperature()
    if temp > 50:
        set_message(f"Warning: High temperature {temp}°C", "temp_warning")
    else:
        set_message(f"Normal temperature {temp}°C")
```

### Interactive dialogs with run_dialog_box

The [run_dialog_box](./../documentation/pytest_jig.md#run_dialog_box)
function creates dialog boxes for operator input with various widgets (text, numeric, checkboxes).
Supports titles, images, and HTML content.
Can be used to notify and interact with the user, but does not save the information in the report.
The user can save the information separately using the
[set_case_artifact](./../documentation/pytest_jig.md#set_case_artifact),
[set_module_artifact](./../documentation/pytest_jig.md#set_module_artifact) or
[set_run_artifact](./../documentation/pytest_jig.md#set_run_artifact) functions.
Essential for manual equipment verification, test configuration confirmation, and safety checks.

```python
def test_manual_calibration():
    dialog = DialogBox(
        dialog_text="Connect calibration device and press Confirm",
        title_bar="Calibration Setup",
        widget=RadioButtonWidget(options=["Ready", "Skip", "Abort"])
    )
    response = run_dialog_box(dialog)
    assert response == "Ready", "Calibration was not confirmed"
```

### Operator messages with set_operator_message

The [set_operator_message](./../documentation/pytest_jig.md#set_operator_message)
function displays non-interactive notifications without database storage.
The user can save the information separately using the
[set_case_artifact](./../documentation/pytest_jig.md#set_case_artifact),
[set_module_artifact](./../documentation/pytest_jig.md#set_module_artifact) or
[set_run_artifact](./../documentation/pytest_jig.md#set_run_artifact) functions.
Can be used to notify and interact with the user, but does not save the information in the report.
Supports titles, images, and HTML content, with optional blocking until dismissed.
Ideal for equipment setup instructions, test phase transitions, and important warnings.

```python
def test_system_startup():
    set_operator_message(
        msg="Please power on all test equipment",
        title="Initial Setup",
        image=ImageComponent(address="assets/power_on.png"),
        block=True
    )
```

### Logging recommendation

| Method                  | Database Storage | User Interaction | Best For |
|-------------------------|------------------|------------------|----------|
| `set_message`           | Yes              | No               | Permanent logs |
| `run_dialog_box`        | No               | Yes              | Test steps requiring input |
| `set_operator_message`  | No               | No               | Important notifications |


## StandCloud

### Storing test result to StandCloud

**Jig** allows user to send test results to **StandCloud**, a data storage and analysis platform.
An example of its use can be found on pages [StandCloud](./../documentation/stand_cloud.md)
and [StandCloud example](./../examples/stand_cloud.md).

### Reading test result from StandCloud

**Jig** allows user to read test result from **StandCloud**.
An example of its use can be found on page [StandCloud reader](./../examples/stand_cloud_reader.md).

## Other

### Measurement

**Jig** allows users to save their measurement data to a database and display it in the operator panel.
The [set_case_measurement](./../documentation/pytest_jig.md#set_case_measurement)
function allows each individual test case to store measurements as a list.

**Display format in operator panel:**

- **Name Value Unit** - for measurements with all components (e.g., "Voltage 12.3 V")
- **Value Unit** - for measurements without names (e.g., "5°", "98.6%", "45″")  
- **Name Value** - for measurements without units (e.g., "Banana 15")

**Special formatting for units:**

- Symbols `%`, `°`, `′`, `″` are displayed without space (e.g., "23.5°C", "98.6%")
- Other units are displayed with space (e.g., "12.3 V", "3.14 rad")

**Configuration:**
Enable measurement display in your `jig.toml`:

```toml
[frontend]
measurement_display = true
```

**Features:**

- Support for both numeric and string measurements
- Clean, minimal tag-based display
- Proper handling of special units (°, %, etc.)

An example of its use can be found on page [measurement](./../examples/measurement.md).

### Chart

**Jig** allows users to save their chart (data series) to a database.
The [set_case_chart](./../documentation/pytest_jig.md#set_case_chart) 
function allows each individual test case to store a single chart.
An example of its use can be found on page [chart](./../examples/chart.md).

### Multiple Jig instances in a single stand

A user can run multiple **Jig** instances on a single stand.
To create a document in the database for storing test data, each stand that 
runs on a single computer must have a unique combination of 
[frontend](./../documentation/jig_config.md#frontend) host and port.
The startup is described in the [Multiple Stand](./../examples/multiple_stands.md) example.

### Multiple test plan configurations

**Jig** allows the user to define and manage multiple test configurations within a single project. 
This feature enables flexible test execution, allowing different sets of tests or 
variations of the same tests to be run by simply selecting a configuration.
This is achieved by defining different `pytest.ini` files for each configuration and referencing 
them in the main `jig.toml` file. 

An example of its use can be found on page [Multiple configs](./../examples/multiple_configs.md).
