# Dialog Box

This is an example of testing dialog boxes using the **HardPy** library.
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

- The function of generating a report and recording it in the database `finish_executing`;
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


@pytest.fixture(scope="module")
def module_log(request):
    log_name = request.module.__name__
    yield logging.getLogger(log_name)


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

### test_dialog_box.py

Contains three examples of valid tests for dialog boxes.

```python
import pytest
import hardpy

@pytest.mark.case_name("Test base dialog box")
def test_base_dialog_box():
    info = hardpy.dialog_box.DialogBoxData(
        title_bar="Operator check",
        dialog_text="If you are not sleeping, press the Confirm button",
    )
    response = hardpy.run_dialog_box(info)
    assert response == None


@pytest.mark.case_name("Test dialog box with text input")
def test_dialog_box_with_text_input():
    widget = hardpy.dialog_box.DialogBoxWidget(
        type=hardpy.dialog_box.DialogBoxWidgetType.TEXT_INPUT,
        info={"text": "Some text"},
    )

    info = hardpy.dialog_box.DialogBoxData(
        dialog_text="Type 'ok' and press the Confirm button",
        title_bar="Example of text input",
        widget=widget,
    )
    response = hardpy.run_dialog_box(info)
    assert response == "ok"


@pytest.mark.case_name("Test dialog box with num input")
def test_dialog_box_with_num_input():
    widget = hardpy.dialog_box.DialogBoxWidget(
        type=hardpy.dialog_box.DialogBoxWidgetType.NUMERIC_INPUT,
        info={"text": "Enter the number"},
    )

    info = hardpy.dialog_box.DialogBoxData(
        dialog_text="Enter the number 123 and press the Confirm button",
        title_bar="Example of entering a number",
        widget=widget,
    )
    response = hardpy.run_dialog_box(info)
    assert response == 123.0
```

### Test base dialog box

Tests the basic dialog box without widgets.

**Data Passed:**
```python
info = hardpy.dialog_box.DialogBoxData(
    title_bar="Operator check",
    dialog_text="If you are not sleeping, press the Confirm button",
)
```
**User Output:**
A dialog box with the title "Operator check", the text "If you are not sleeping, press the Confirm button" and "Confirm" button. The user needs to press the "Confirm" button.

### Test dialog box with text input

Tests the dialog box with text input.

**Data Passed:**
```python
widget = hardpy.dialog_box.DialogBoxWidget(
    type=hardpy.dialog_box.DialogBoxWidgetType.TEXT_INPUT,
    info={"text": "Some text"},
)
info = hardpy.dialog_box.DialogBoxData(
    dialog_text="Type 'ok' and press the Confirm button",
    title_bar="Example of text input",
    widget=widget,
)
```
**User Output:**
A dialog box with the title "Example of text input", the text "Type 'ok' and press the Confirm button", text input field and "Confirm" button. The user needs to type "ok" and press the "Confirm" button.

### Test dialog box with num input

Tests the dialog box with numeric input.

**Data Passed:**
```python
widget = hardpy.dialog_box.DialogBoxWidget(
    type=hardpy.dialog_box.DialogBoxWidgetType.NUMERIC_INPUT,
    info={"text": "Enter the number"},
)
info = hardpy.dialog_box.DialogBoxData(
    dialog_text="Enter the number 123 and press the Confirm button",
    title_bar="Example of entering a number",
    widget=widget,
)
```
**User Output:**
A dialog box with the title "Example of entering a number"б the text "Enter the number 123 and press the Confirm button", тгьиук input field and "Confirm" button. The user needs to enter "123" and press the "Confirm" button.