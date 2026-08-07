import pytest

import jig

pytestmark = pytest.mark.module_name("Jig template")


@pytest.mark.case_name("Test 3")
def test_three():
    assert True
