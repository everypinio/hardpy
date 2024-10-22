from time import sleep

import pytest

import hardpy
from hardpy import DialogBox, TextInputWidget, run_dialog_box


@pytest.mark.attempt(5)
def test_attempt_always_positive_test():
    hardpy.set_message(
        f"Current attempt {hardpy.get_current_attempt()}",
        "updated_status",
    )
    assert True


count = 0


@pytest.mark.attempt(7)
def test_four_attempts():
    global count  # noqa: PLW0603
    count += 1
    sleep(0.5)
    hardpy.set_message(
        f"Current attempt {hardpy.get_current_attempt()}",
        "updated_status",
    )
    if count <= 3:  # noqa: PLR2004
        msg = "Test failed intentionally"
        raise Exception(msg)  # noqa: TRY002
    assert True


@pytest.mark.attempt(3)
def test_dialog_box():
    dbx = DialogBox(
        dialog_text="Type 'ok' and press the Confirm button",
        title_bar="Example of text input",
        widget=TextInputWidget(),
    )
    response = run_dialog_box(dbx)
    attempt = hardpy.get_current_attempt()
    if attempt <= 3:  # noqa: PLR2004
        dbx = DialogBox(
            dialog_text=f"Reconnect and try again. Test attempt {hardpy.get_current_attempt()}",
            title_bar="Attempt message",
        )
        run_dialog_box(dbx)
    else:
        dbx = DialogBox(
            dialog_text=f"Test failed on attempt {hardpy.get_current_attempt()}",
            title_bar="Attempt message",
        )
        run_dialog_box(dbx)
    assert response == "ok", "The entered text is not correct"


@pytest.mark.attempt(5)
def test_dialog_box_failed():
    dbx = DialogBox(
        dialog_text="This test is always negative",
        title_bar="Example",
    )
    response = run_dialog_box(dbx)
    hardpy.set_message(
        f"Current attempt {hardpy.get_current_attempt()}. Response: {response}",
        "updated_status",
    )
    assert False  # noqa: B011, PT015
