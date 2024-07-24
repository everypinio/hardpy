# Dialog Box

This is an example of testing dialog boxes using the **HardPy** library.

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

### test_dialog_box.py

Contains five examples of valid tests for dialog boxes.

```python
import pytest
import hardpy

@pytest.mark.case_name("Test base dialog box")
def test_base():
    dbx = hardpy.dialog_box.DialogBox(
        title_bar="Operator check",
        dialog_text="If you are not sleeping, press the Confirm button",
    )
    response = hardpy.run_dialog_box(dbx)
    assert response == None


@pytest.mark.case_name("Test dialog box with text input")
def test_text_input():
    widget = hardpy.dialog_box.DialogBoxWidget(
        type=hardpy.dialog_box.DialogBoxWidgetType.TEXT_INPUT,
    )

    dbx = hardpy.dialog_box.DialogBox(
        dialog_text="Type 'ok' and press the Confirm button",
        title_bar="Example of text input",
        widget=widget,
    )
    response = hardpy.run_dialog_box(dbx)
    assert response == "ok"


@pytest.mark.case_name("Test dialog box with num input")
def test_num_input():
    widget = hardpy.dialog_box.DialogBoxWidget(
        type=hardpy.dialog_box.DialogBoxWidgetType.NUMERIC_INPUT,
    )

    dbx = hardpy.dialog_box.DialogBox(
        dialog_text="Enter the number 123 and press the Confirm button",
        title_bar="Example of entering a number",
        widget=widget,
    )
    response = hardpy.run_dialog_box(dbx)
    assert response == 123.0


@pytest.mark.case_name("Radiobutton")
def test_radiobutton():
    dbx = DialogBox(
        dialog_text=f"Select one item (1) from several and click the Confirm button",
        title_bar="Radiobutton example",
        widget=DialogBoxWidget(
            DialogBoxWidgetType.RADIOBUTTON,
            {"options": ["one", "two", "three"]},
        ),
    )
    response = run_dialog_box(dbx)
    set_message(f"Selected item {response}")
    assert response == "one", "The answer is not correct"


@pytest.mark.case_name("Checkbox")
def test_checkbox():
    dbx = DialogBox(
        dialog_text=f"Select one or more items (1) and click the Confirm button",
        title_bar="Checkbox example",
        widget=DialogBoxWidget(
            DialogBoxWidgetType.CHECKBOX, {"options": ["one", "two", "three"]}
        ),
    )
    response = run_dialog_box(dbx)
    set_message(f"Selected item {response}")
    assert response == '["one"]', "The answer is not correct"
```

