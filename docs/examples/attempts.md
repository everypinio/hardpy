# Attempts

In **HardPy** library, the `@pytest.mark.attempt(n)` marker allows you to configure a test to be retried a specified number of times `(n)` if it initially fails. 
This functionality is particularly useful for tests that might encounter transient errors or require multiple attempts to succeed due to external factors.
The code for this example can be seen inside the hardpy package 
[Attempts](https://github.com/everypinio/hardpy/tree/main/examples/attempts).

Contains some examples of valid tests with attempts.

### how to start

1. Launch `hardpy init attempts`.
2. Launch [CouchDH instance](../documentation/database.md#couchdb-instance).
3. Modify the files described below.
4. Launch `hardpy run attempts`.

### conftest.py

```python
import datetime
import pytest
from hardpy import (
    CouchdbConfig,
    CouchdbLoader,
    get_current_report,
)

class CurrentMinute:
    """Class example."""

    def get_minute(self):
        """Get current minute."""
        current_time = datetime.datetime.now()
        return int(current_time.strftime("%M"))

@pytest.fixture
def current_minute():
    current_time = CurrentMinute()
    yield current_time

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


### test_1.py

```python
from time import sleep
import pytest
import hardpy
from hardpy import DialogBox, TextInputWidget, run_dialog_box

@pytest.mark.attempt(5)
def test_minute_parity(current_minute):
    attempt = hardpy.get_current_attempt()
    hardpy.set_message(f"Current attempt {attempt}", "updated_status")
    if attempt > 1:
        sleep(15)

    minute = current_minute.get_minute()
    hardpy.set_message(f"Current minute {minute}")
    hardpy.set_case_artifact({"minute": minute})

    assert minute % 2 == 0, f"The test failed because {minute} is odd! Try again!"

@pytest.mark.attempt(3)
def test_dialog_box():
    dbx = DialogBox(
        dialog_text="Print '123', if you want to fail attempt. Print 'ok', if you want to pass attempt. ",
        title_bar="Example of text input",
        widget=TextInputWidget(),
    )
    response = run_dialog_box(dbx)
    if response != "ok":
        dbx = DialogBox(
            dialog_text=f"Test attempt {hardpy.get_current_attempt()}",
            title_bar="Attempt message",
        )
        run_dialog_box(dbx)

    assert response == "ok", "The entered text is not correct"
```