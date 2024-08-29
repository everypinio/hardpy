# Dialog Box

This is an example of testing dialog boxes using the **HardPy** library.
The code for this example can be seen inside the hardpy package [Dialog Box](https://github.com/everypinio/hardpy/tree/main/examples/project/dialog_box).

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
    dbx = hardpy.DialogBox(
        title_bar="Operator check",
        dialog_text="Press the Confirm button",
    )
    response = hardpy.run_dialog_box(dbx)
    assert response


@pytest.mark.case_name("Text input")
def test_text_input():
    dbx = hardpy.DialogBox(
        dialog_text="Type 'ok' and press the Confirm button",
        title_bar="Example of text input",
        widget=TextInputWidget(),
    )
    response = hardpy.run_dialog_box(dbx)
    hardpy.set_message(f"Entered text {response}")
    assert response == "ok", "The entered text is not correct"


@pytest.mark.case_name("Numeric input")
def test_num_input():
    test_num = 123
    dbx = hardpy.DialogBox(
        dialog_text=f"Enter the number {test_num} and press the Confirm button",
        title_bar="Example of entering a number",
        widget=hardpy.NumericInputWidget(),
    )
    response = int(hardpy.run_dialog_box(dbx))
    hardpy.set_message(f"Entered number {response}")
    assert response == test_num, "The entered number is not correct"


@pytest.mark.case_name("Test dialog box with radiobutton")
def test_radiobutton():
    dbx = hardpy.DialogBox(
        dialog_text='Select item "one" out of several and click Confirm.',
        title_bar="Radiobutton example",
        widget=hardpy.RadiobuttonWidget(fields=["one", "two", "three"]),
    )
    response = run_dialog_box(dbx)
    hardpy.set_message(f"Selected item {response}")
    assert response == "one", "The answer is not correct"


@pytest.mark.case_name("Test dialog box with checkbox")
def test_checkbox():
    dbx = hardpy.DialogBox(
        dialog_text='Select items "one" and "two" and click the Confirm button',
        title_bar="Checkbox example",
        widget=hardpy.CheckboxWidget(fields=["one", "two", "three"]),
    )
    response = hardpy.run_dialog_box(dbx)
    hardpy.set_message(f"Selected item {response}")
    correct_answer = {"one", "two"}
    assert set(response) == correct_answer, "The answer is not correct"

@pytest.mark.case_name("Image")
def test_upload_image():
    dbx = hardpy.DialogBox(
        dialog_text="Test image",
        widget=hardpy.ImageWidget(address="assets/test.png"),
    )
    response = hardpy.run_dialog_box(dbx)
    assert response

@pytest.mark.case_name("Multistep")
def test_multiple_steps():
    steps = [
        hardpy.StepWidget("Step 1", text="Content for step", widget=None),
        hardpy.StepWidget("Step 2", text="Content for step 2", widget=hardpy.ImageWidget(address="assets/test.png")),
        hardpy.StepWidget("Step 3", text=None, widget=hardpy.ImageWidget(address="assets/test.png")),
    ]
    dbx = hardpy.DialogBox(
        dialog_text="Follow the steps and click Confirm",
        widget=hardpy.MultistepWidget(steps),
    )
    response = hardpy.run_dialog_box(dbx)
    assert response
```
