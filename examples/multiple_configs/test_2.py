import pytest

import jig

pytestmark = pytest.mark.module_name("Jig template")


@pytest.mark.case_name("Test 2")
def test_two():
    assert True
