# Dialog box

This is an example of testing dialog boxes using the **HardPy** library.
The code for this example can be seen inside the hardpy package
[Dialog Box](https://github.com/everypinio/hardpy/tree/main/examples/dialog_box).

Contains some examples of valid tests for dialog boxes.
To test images, create an `assets` folder in the `dialog_box` folder with the image `test.png`.

### how to start

1. Launch `hardpy init dialog_box`.
2. Launch [CouchDB instance](../documentation/database.md#couchdb-instance).
3. Modify the files described below.
4. Launch `hardpy run dialog_box`.

### test_1_base_box.py

```python
import pytest
from hardpy import DialogBox, HTMLComponent, ImageComponent, run_dialog_box

pytestmark = pytest.mark.module_name("Base dialog box")

@pytest.mark.case_name("Empty test before")
def test_before():
    assert True

@pytest.mark.case_name("Base dialog box with image")
def test_base_dialog_box_with_image():
    dbx = DialogBox(
        title_bar="Operator check",
        dialog_text="Press the Confirm button",
        image=ImageComponent(address="assets/test.png", width=100, border=1),
        html=HTMLComponent(html="https://everypinio.github.io/hardpy/", width=50, is_raw_html=False),
        pass_fail=True,
    )
    response = run_dialog_box(dbx)
    assert response.result
    assert response.data

@pytest.mark.case_name("Empty test after")
def test_after():
    assert True
```

### test_2_input_field.py

```python
import pytest
from hardpy import (
    DialogBox,
    ImageComponent,
    NumericInputWidget,
    TextInputWidget,
    run_dialog_box,
    set_message,
)

pytestmark = pytest.mark.module_name("Input field dialog boxes")

@pytest.mark.case_name("Text input with image")
def test_text_input_with_image():
    dbx = DialogBox(
        dialog_text="Type 'ok' and press the Confirm button",
        title_bar="Example of text input",
        widget=TextInputWidget(),
        image=ImageComponent(address="assets/test.png", width=50),
        font_size=18,
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
```

### test_3_choice_control.py

```python
import pytest
from hardpy import (
    CheckboxWidget,
    DialogBox,
    RadiobuttonWidget,
    run_dialog_box,
    set_message,
)

pytestmark = pytest.mark.module_name("Choice control dialog boxes")

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
```

### test_4_multiple_steps.py

```python
import pytest
from hardpy import DialogBox, HTMLComponent, ImageComponent, MultistepWidget, StepWidget, run_dialog_box

pytestmark = pytest.mark.module_name("Multiple steps dialog box")

@pytest.mark.case_name("Multistep")
def test_multiple_steps():
    steps = [
        StepWidget("Step 1", text="Content for step"),
        StepWidget(
            "Step 2",
            text="Content for step 2",
            image=ImageComponent(address="assets/test.png", width=50),
        ),
        StepWidget(
            "Step 3",
            text=None,
            html=HTMLComponent(html="https://everypinio.github.io/hardpy/", width=50, is_raw_html=False),
        ),
    ]
    dbx = DialogBox(
        dialog_text="Follow the steps and click Confirm",
        widget=MultistepWidget(steps),
    )
    response = run_dialog_box(dbx)
    assert response
```

### test_5_html.py

```python
import pytest

from hardpy import DialogBox, HTMLComponent, run_dialog_box

pytestmark = pytest.mark.module_name("Dialog box with HTML")

@pytest.mark.case_name("Base dialog box with html code")
def test_base_dialog_box_with_html_code():
    test_html = """
    <!DOCTYPE html>
    <html>
    <body>

    <h1>Test HTML Page</h1>

    <p>It is testing page.</p>
    <p>You can put anything on it.</p>

    </body>
    </html>
    """
    dbx = DialogBox(
        title_bar="Operator check",
        dialog_text="Press the Confirm button",
        html=HTMLComponent(html=test_html, is_raw_html=True, width=50),
    )
    response = run_dialog_box(dbx)
    assert response

@pytest.mark.case_name("Base dialog box with html link")
def test_base_dialog_box_with_html_link():
    dbx = DialogBox(
        title_bar="Operator check",
        dialog_text="Press the Confirm button",
        html=HTMLComponent(
            html="https://everypinio.github.io/hardpy/",
            is_raw_html=False,
            border=2,
        ),
    )
    response = run_dialog_box(dbx)
    assert response
```
