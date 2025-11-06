import pytest

import hardpy

pytestmark = pytest.mark.module_name("HardPy template")


@pytest.mark.case_name("Test 2")
def test_two():
    assert True
