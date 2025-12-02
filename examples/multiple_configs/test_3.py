import pytest

import hardpy

pytestmark = pytest.mark.module_name("HardPy template")


@pytest.mark.case_name("Test 3")
def test_three():
    assert True
