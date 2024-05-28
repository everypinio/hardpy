import pytest
import hardpy

pytestmark = pytest.mark.module_dependency("test_1::test_five")


def test_one():
    assert True


def test_two():
    assert True


def test_three():
    assert True
