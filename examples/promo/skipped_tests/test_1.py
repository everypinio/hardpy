import pytest

pytestmark = pytest.mark.module_name("Skipped tests")

def test_a():
    assert False


@pytest.mark.dependency("test_1::test_a")
def test_b():
    assert False
