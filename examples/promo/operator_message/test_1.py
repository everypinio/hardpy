from time import sleep
from hardpy import clear_operator_message, set_message, set_operator_message

pytestmark = pytest.mark.module_name("Operator message")

def test_block_operator_message():
    set_operator_message(msg="Test blocking operator message", title="Operator message")
    for i in range(3, 0, -1):
        set_message(f"Time left to complete test case {i} s", "updated_status")
        sleep(1)
    set_message("Test case finished", "updated_status")
    assert True
