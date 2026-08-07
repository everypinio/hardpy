import pytest

import jig

pytestmark = pytest.mark.module_name("Jig template")


@pytest.mark.case_name("Test 1")
def test_one():
    assert True
