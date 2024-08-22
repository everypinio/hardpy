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

Contains some examples of valid tests for dialog boxes.
To test images, create an `assets` folder in the `tests` folder with the image `test.png`.

```python
import pytest
import hardpy

@pytest.mark.case_name("Base dialog box")
def test_base_dialog_box():
    dbx = DialogBox(
        title_bar="Operator check",
        dialog_text="Press the Confirm button",
    )
    response = run_dialog_box(dbx)
    assert response


@pytest.mark.case_name("Text input")
def test_text_input():
    dbx = DialogBox(
        dialog_text="Type 'ok' and press the Confirm button",
        title_bar="Example of text input",
        widget=TextInputWidget(),
    )
    response = run_dialog_box(dbx)
    set_message(f"Entered text {response}")
    assert response == "ok", "The entered text is not correct"


@pytest.mark.case_name("Numeric input")
def test_num_input():
    test_num = 123
    dbx = DialogBox(
        dialog_text=f"Enter the number {test_num} and press the Confirm button",
        title_bar="Example of entering a number",
        widget=NumericInputWidget(),
    )
    response = int(run_dialog_box(dbx))
    set_message(f"Entered number {response}")
    assert response == test_num, "The entered number is not correct"


@pytest.mark.case_name("Test dialog box with radiobutton")
def test_radiobutton():
    dbx = DialogBox(
        dialog_text='Select item "one" out of several and click Confirm.',
        title_bar="Radiobutton example",
        widget=RadiobuttonWidget(fields=["one", "two", "three"]),
    )
    response = run_dialog_box(dbx)
    set_message(f"Selected item {response}")
    assert response == "one", "The answer is not correct"


@pytest.mark.case_name("Test dialog box with checkbox")
def test_checkbox():
    dbx = DialogBox(
        dialog_text='Select items "one" and "two" and click the Confirm button',
        title_bar="Checkbox example",
        widget=CheckboxWidget(fields=["one", "two", "three"]),
    )
    response = run_dialog_box(dbx)
    set_message(f"Selected item {response}")
    correct_answer = {"one", "two"}
    assert set(response) == correct_answer, "The answer is not correct"

@pytest.mark.case_name("Image")
def test_upload_image():
    dbx = DialogBox(
        dialog_text="Test image",
        widget=ImageWidget(address="assets/test.png"),
    )
    response = run_dialog_box(dbx)
    assert response

@pytest.mark.case_name("Multistep")
def test_multiple_steps():
    steps = [
        StepWidget("Step 1", text="Content for step", widget=None),
        StepWidget("Step 2", text="Content for step 2", widget=ImageWidget(address="assets/test.png")),
        StepWidget("Step 3", text=None, widget=ImageWidget(address="assets/test.png")),
    ]
    dbx = DialogBox(
        dialog_text="Follow the steps and click Confirm",
        widget=MultistepWidget(steps),
    )
    response = run_dialog_box(dbx)
    assert response is None
```
