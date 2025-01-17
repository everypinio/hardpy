from time import sleep

from hardpy import (
    ImageComponent,
    clear_operator_message,
    set_message,
    set_operator_message,
)


def test_block_operator_message():
    set_operator_message(
        msg="Test blocking operator message",
        title="Operator message",
        image=ImageComponent(address="assets/image.png", width=100),
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
        image=ImageComponent(address="assets/image.png", width=100),
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
