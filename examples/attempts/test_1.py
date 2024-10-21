import datetime
from time import sleep

import pytest
from driver_example import DriverExample

import hardpy
from hardpy.pytest_hardpy.pytest_call import run_dialog_box, set_message
from hardpy.pytest_hardpy.utils.dialog_box import DialogBox, TextInputWidget

pytestmark = [
    pytest.mark.module_name("Main tests"),
]

count = 0


# @pytest.mark.attempt(5)
# def test_attempt_positive_test():
#     hardpy.set_message("Positive test")
#     assert True


# @pytest.mark.attempt(7)
# def test_attempt():
#     global count  # noqa: PLW0603
#     count += 1
#     sleep(0.5)
#     hardpy.set_message(f"Current minute {count}")
#     if count <= 3:  # noqa: PLR2004
#         msg = "Test failed intentionally"
#         raise Exception(msg)  # noqa: TRY002
#     assert True


@pytest.mark.attempt(5)
@pytest.mark.case_name("Text input")
def test_text_input():
    dbx = DialogBox(
        dialog_text="Type 'ok' and press the Confirm button",
        title_bar="Example of text input",
        # widget=TextInputWidget(),
    )
    response = run_dialog_box(dbx)
    set_message(f"Entered text {response}")
    assert False
    # assert response == "ok", "The entered text is not correct"


# @pytest.mark.attempt(3)
# def test_attempt_minute_parity():
#     current_time = datetime.datetime.now()  # noqa: DTZ005
#     minute = int(current_time.strftime("%M"))
#     hardpy.set_message(f"Current minute {minute}")
#     result = minute % 2
#     sleep(10)
#     data = {
#         "minute": minute,
#     }
#     hardpy.set_case_artifact(data)
#     assert result == 0, f"The test failed because {minute} is odd! Try again!"


# @pytest.mark.attempt(5)
# def test_minute_parity(driver_example: DriverExample):
#     minute = driver_example.current_minute
#     hardpy.set_message(f"Current minute {minute}")
#     result = minute % 2
#     data = {
#         "minute": minute,
#     }
#     hardpy.set_case_artifact(data)
#     assert result == 0, f"The test failed because {minute} is odd! Try again!"


# @pytest.mark.attempt(5)
# def test_attempt_negative_test():
#     hardpy.set_message("Negative test")
#     assert False  # noqa: B011, PT015
