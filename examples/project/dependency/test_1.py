import pytest
import hardpy


def test_one():
    assert True


@pytest.mark.case_dependency("test_1::test_one")
def test_two():
    assert True


def test_three():
    assert False


@pytest.mark.case_dependency("test_1::test_three")
def test_four():
    assert False


@pytest.mark.case_dependency("test_1::test_four")
def test_five():
    assert True
