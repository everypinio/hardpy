# Attempts

In **HardPy** library, the [@pytest.mark.attempt(n)](./../documentation/pytest_hardpy.md#attempt)
marker allows you to configure a test to be retried a specified number of
times `(n)` if it initially fails.
This functionality is particularly useful for tests that might encounter transient errors or
require multiple attempts to succeed due to external factors.
The code for this example can be seen inside the hardpy package
[Attempts](https://github.com/everypinio/hardpy/tree/main/examples/attempts).

Contains some examples of valid tests with attempts.

### how to start

1. Launch `hardpy init attempts`.
2. Launch [CouchDB instance](../documentation/database.md#couchdb-instance).
3. Modify the files described below.
4. Launch `hardpy run attempts`.

### conftest.py

```python
import datetime
import pytest

class CurrentMinute:
    def get_minute(self):
        current_time = datetime.datetime.now()
        return int(current_time.strftime("%M"))

@pytest.fixture
def current_minute():
    current_time = CurrentMinute()
    yield current_time
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
        dialog_text="Print 'ok', if you want to pass attempt.",
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
