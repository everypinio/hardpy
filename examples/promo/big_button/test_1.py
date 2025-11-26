import pytest
import hardpy


pytestmark = pytest.mark.module_name("Big button")


@pytest.mark.case_name("Test 1")
def test_one():
    assert True
