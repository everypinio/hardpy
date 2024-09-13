from time import sleep

import pytest
import hardpy

pytestmark = [
    pytest.mark.module_name("End of testing"),
    pytest.mark.dependency("test_2::test_minute_parity"),
]


@pytest.mark.case_name("Final case")
def test_one():
    for i in range(5, 0, -1):
        hardpy.set_message(f"Time left until testing ends {i} s", "updated_status")
        sleep(1)
    hardpy.set_message("Testing ended", "updated_status")
    assert True
