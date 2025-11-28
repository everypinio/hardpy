import pytest

import hardpy

pytestmark = pytest.mark.module_name("HardPy template")


@pytest.mark.case_name("Test 1")
def test_one():
    assert True
