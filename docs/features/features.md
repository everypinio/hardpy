# Features

## Viewing tests in the operator panel

The operator panel allows you to view the test hierarchy with **test folder/test file/function** levels.
See the [HardPy panel](./../documentation/hardpy_panel.md) for more information.
User can launch operator panel using [hardpy run](./../documentation/cli.md#hardpy-run) command.

## Running tests

Based on pytest **HardPy** allows you to run pytest tests in the browser or command line.
For running tests in browser run tests using [hardpy run](./../documentation/cli.md#hardpy-run) command.

```bash
hardpy run
```

and press the **Start** button.
Alternatively, the user can start the operator panel with the “Start” button and run tests with pytest.

```bash
python -m pytest
```

The user can also run tests without the operator panel, just using the `hardpy start` command or
using `pytest`.

## Stopping the tests

The user can stop the tests during execution from the operator panel by clicking on the **Stop** button
or using the `hardpy stop` command.
It is possible to stop tests from the console by sending an interrupt, e.g. “Ctrl-C” in Linux.

## Checking the status of tests

The user can check the status of tests using the `hardpy status` command.

## Storing test result in database

**HardPy** does not allow you to run tests without a running **CouchDB** database.
This is a NoSQL database that ensures that the results of the current test run are committed,
even if the tests are aborted early.

To save the report history, the user must configure the **conftest.py** file using the
[CouchdbLoader](./../documentation/pytest_hardpy.md#couchdbloader) or another adapter to save the data.
By default, only the current report in the [runstore](./../documentation/database.md#runstore-scheme)
database is stored in **CouchDB**.

An example of configuring **conftest.py** to store test run history can be found in several examples,
including the [couchdb_load](./../examples/couchdb_load.md) and
[minute_parity](./../examples/minute_parity.md).

## Creating template project

The **HardPy** can create template project using the [hardpy init](./../documentation/cli.md#hardpy-init)
command. An example of usage can be found in the **how to init** section among the examples, e.g. in
[minute parity](./../examples/minute_parity.md#how-to-start).

```bash
hardpy init minute_parity
```

## Interacting with tests in the operator panel

The user can interact with the tests through dialog boxes in the operator panel.
**HardPy** provides the ability to enter [text](./../documentation/hardpy_panel.md#text-input-field) or
[numbers](./../documentation/hardpy_panel.md#number-input-field), make selections using
[checkboxes](./../documentation/hardpy_panel.md#checkbox) or
[radio buttons](./../documentation/hardpy_panel.md#radiobutton),
guide the user through [multiple steps](./../documentation/hardpy_panel.md#multiple-steps)
in a single window, display [images](./../documentation/pytest_hardpy.md#imagecomponent) to the user,
and insert [HTML components](./../documentation/pytest_hardpy.md#htmlcomponent) into the dialog box using iframes.

In dialog boxes, the user must confirm their action by clicking the **Confirm** button.
Closing the dialog box prematurely will abort the test.

If the user only needs to provide information, an
[operator message](./../documentation/hardpy_panel.md#operator-message) can be used.
Unlike dialog boxes, the user cannot enter any information, only close the window.
User can also close the operator message from within the test code and run it in non-blocking mode,
so that displaying the window does not stop the test.

## Running multiple test attempts

The **HardPy** allows the user to attach an [attempt](./../documentation/pytest_hardpy.md#attempt)
marker to a test, which allows the test to be repeated as many times as specified in
the marker's content in the event of failure.

## Skipping the tests

The **HardPy** allows the user to skip tests on [dependency](./../documentation/pytest_hardpy.md#dependency)
markers. The user can specify that a test or an entire module depends on another test.
In this way, tests can be defined whose failure will prevent the marked tests from running.

## Running some instance in single stand

A user can run multiple **HardPy** instances on a single stand.
The startup is described in the [Multiple Stand](./../examples/multiple_stands.md) example.

## Storing test result to StandCloud

**HardPy** allows user to send test results to **StandCloud**, a data storage and analysis platform.
See the [StandCloud](./../documentation/stand_cloud.md) section and the
[StandCloud example](./../examples/stand_cloud.md) for more information.

## Logging approaches in HardPy

**HardPy** provides several methods for logging and user interaction during testing.
Choose the appropriate method based on whether you need to store information in the
database or just display messages to the operator.

### Database logging with set_message

The [set_message](./../documentation/pytest_hardpy.md#set_message) function stores the log message in the report.
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

The [run_dialog_box](./../documentation/pytest_hardpy.md#run_dialog_box)
function creates dialog boxes for operator input with various widgets (text, numeric, checkboxes).
Supports titles, images, and HTML content.
Can be used to notify and interact with the user, but does not save the information in the report.
The user can save the information separately using the
[set_case_artifact](./../documentation/pytest_hardpy.md#set_case_artifact),
[set_module_artifact](./../documentation/pytest_hardpy.md#set_module_artifact) or
[set_run_artifact](./../documentation/pytest_hardpy.md#set_run_artifact) functions.
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

The [set_operator_message](./../documentation/pytest_hardpy.md#set_operator_message)
function displays non-interactive notifications without database storage.
The user can save the information separately using the
[set_case_artifact](./../documentation/pytest_hardpy.md#set_case_artifact),
[set_module_artifact](./../documentation/pytest_hardpy.md#set_module_artifact) or
[set_run_artifact](./../documentation/pytest_hardpy.md#set_run_artifact) functions.
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

### Choosing the right method

| Method                  | Database Storage | User Interaction | Best For |
|-------------------------|------------------|------------------|----------|
| `set_message`           | Yes              | No               | Permanent logs |
| `run_dialog_box`        | No               | Yes              | Test steps requiring input |
| `set_operator_message`  | No               | No               | Important notifications |

## Reading test result from StandCloud

**HardPy** allows user to read test result from **StandCloud**.
See the [StandCloud reader](./../examples/stand_cloud_reader.md) for more information.
