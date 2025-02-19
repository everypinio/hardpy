# Operator message

The [set_operator_message](./../documentation/pytest_hardpy.md/#set_operator_message)
function is intended for sending messages to the operator.
Operator messages can be used before, after, and during tests.

**set_operator_message** can be used in conjunction with images and html pages.
To do this, the user can set the argument `image` with the
[ImageComponent](./../documentation/pytest_hardpy.md/#imagecomponent) class 
and the argument `html` with the [HTMLComponent](./../documentation/pytest_hardpy.md/#htmlcomponent) class.

The default message to the operator blocks further execution of the code,
but the user can set the argument `block=False` and the function will display the message
and continue execution of the test.
In this case, the user can clear the operator message with the
[clear_operator_message](./../documentation/pytest_hardpy.md/#clear_operator_message) function.

The [clear_operator_message](./../documentation/pytest_hardpy.md/#clear_operator_message)
is intended for clearing current operator message.

<h1 align="center">
    <img src="https://raw.githubusercontent.com/everypinio/hardpy/main/docs/img/operator_msg.png" alt="operator_msg">
</h1>

### how to start

1. Launch [CouchDH instance](../documentation/database.md#couchdb-instance).
2. Create a directory `<dir_name>` with the files described below.
3. Launch `hardpy run <dir_name>`.

### conftest.py

Contains settings and fixtures for all tests:

- The `finish_executing` function generates a report and saves it to the database.
- The `test_end_message` function shows message about completing of testing.
- The `fill_list_functions_after_test` function populates a list of actions to be performed post-test. You may rename this function as you want.

If the report database doesn't exist, the report won't be saved, and an error message will be displayed to the operator. Otherwise, a success message will be shown indicating successful report saving.

```python
import pytest
from hardpy import CouchdbConfig, CouchdbLoader, get_current_report, set_operator_message

def finish_executing():
    report = get_current_report()
    try:
        if report:
            loader = CouchdbLoader(CouchdbConfig(port=5986))
            loader.load(report)
            set_operator_message(msg="Saving report was successful", title="Operator message")
    except RuntimeError as e:
        set_operator_message(msg='The report was not recorded with error: "' + str(e) + '"', title="Operator message")

def test_end_message():
    set_operator_message(msg="Testing completed", title="Operator message")

@pytest.fixture(scope="session", autouse=True)
def fill_list_functions_after_test(post_run_functions: list):
    post_run_functions.append(test_end_message)
    post_run_functions.append(finish_executing)
    yield
```

### test_1.py

Contains examples of how to use operator messages.

```python
from time import sleep
from hardpy import clear_operator_message, set_message, set_operator_message

def test_block_operator_message():
    set_operator_message(msg="Test blocking operator message", title="Operator message")
    for i in range(3, 0, -1):
        set_message(f"Time left to complete test case {i} s", "updated_status")
        sleep(1)
    set_message("Test case finished", "updated_status")
    assert True

def test_not_block_operator_message():
    set_operator_message(msg="Test not blocking operator message", title="Operator message", block=False, font_size=18)
    for i in range(3, 0, -1):
        set_message(f"Time left to complete test case {i} s", "updated_status")
        sleep(1)
    set_message("Test case finished", "updated_status")
    sleep(2)
    assert True

def test_clear_operator_message():
    set_operator_message(msg="Test clearing operator message", title="Operator message", block=False)
    for i in range(3, 0, -1):
        set_message(f"Time left to complete test case {i} s", "updated_status")
        sleep(1)
    clear_operator_message()
    set_message("Test case finished", "updated_status")
    sleep(2)
    assert True
```

### test_2.py

```python
from time import sleep
from hardpy import ImageComponent, clear_operator_message, set_message, set_operator_message

def test_block_operator_message():
    set_operator_message(
        msg="Test blocking operator message",
        title="Operator message",
        image=ImageComponent(address="assets/test.png", width=100),
    )
    for i in range(3, 0, -1):
        set_message(f"Time left to complete test case {i} s", "updated_status")
        sleep(1)
    set_message("Test case finished", "updated_status")
    assert True

def test_not_block_operator_message():
    set_operator_message(
        msg="Test not blocking operator message",
        title="Operator message",
        image=ImageComponent(address="assets/test.png", width=100),
        block=False,
    )
    for i in range(3, 0, -1):
        set_message(f"Time left to complete test case {i} s", "updated_status")
        sleep(1)
    set_message("Test case finished", "updated_status")
    sleep(2)
    assert True

def test_clear_operator_message():
    set_operator_message(
        msg="Test clearing operator message",
        title="Operator message",
        image=ImageComponent(address="assets/test.png", width=100),
        block=False,
    )
    for i in range(3, 0, -1):
        set_message(f"Time left to complete test case {i} s", "updated_status")
        sleep(1)
    clear_operator_message()
    set_message("Test case finished", "updated_status")
    sleep(2)
    assert True
```

### test_3.py

```python
from time import sleep
from hardpy import HTMLComponent, set_message, set_operator_message

def test_operator_message_with_html():
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
    set_operator_message(
        msg="Test operator message with html",
        title="Operator message",
        html=HTMLComponent(html=test_html, is_raw_html=True),
    )
    for i in range(3, 0, -1):
        set_message(f"Time left to complete test case {i} s", "updated_status")
        sleep(1)
    set_message("Test case finished", "updated_status")
    assert True

def test_operator_message_with_html_and_border():
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
    set_operator_message(
        msg="Test operator message with html",
        title="Operator message",
        html=HTMLComponent(html=test_html, is_raw_html=True, border=10, width=20),
    )
    for i in range(3, 0, -1):
        set_message(f"Time left to complete test case {i} s", "updated_status")
        sleep(1)
    set_message("Test case finished", "updated_status")
    assert True
```
