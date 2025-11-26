import pytest

pytestmark = pytest.mark.module_name("Critical tests")

@pytest.mark.critical
def test_core_feature():
    assert False  # This will fail

def test_secondary_feature():
    assert True  # This will be skipped
