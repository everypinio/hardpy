from time import sleep

import hardpy


def test_block_operator_message():
    hardpy.set_operator_message(
        msg="Test blocking operator message",
        title="Operator message",
    )
    for i in range(3, 0, -1):
        hardpy.set_message(f"Time left to complete test case {i} s", "updated_status")
        sleep(1)
    hardpy.set_message("Test case finished", "updated_status")
    assert True


def test_not_block_operator_message():
    hardpy.set_operator_message(
        msg="Test not blocking operator message",
        title="Operator message",
        blocking=False,
    )
    for i in range(3, 0, -1):
        hardpy.set_message(f"Time left to complete test case {i} s", "updated_status")
        sleep(1)
    hardpy.set_message("Test case finished", "updated_status")
    sleep(2)
    assert True


def test_clear_operator_message():
    hardpy.set_operator_message(
        msg="Test clearing operator message",
        title="Operator message",
        blocking=False,
    )
    for i in range(3, 0, -1):
        hardpy.set_message(f"Time left to complete test case {i} s", "updated_status")
        sleep(1)
    hardpy.clear_operator_message()
    hardpy.set_message("Test case finished", "updated_status")
    sleep(2)
    assert True
