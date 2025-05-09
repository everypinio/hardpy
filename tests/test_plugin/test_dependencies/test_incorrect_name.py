from __future__ import annotations

from typing import TYPE_CHECKING

from pytest import ExitCode

if TYPE_CHECKING:
    from pytest import Pytester


def test_case_dependency_incorrect_format(pytester: Pytester, hardpy_opts: list):
    # incorrect case dependencie format
    test_1 = """
        import pytest

        @pytest.mark.dependency(":::")

        def test_a():
            assert True
    """
    pytester.makepyfile(test_1)
    result = pytester.runpytest(*hardpy_opts)
    assert result.ret == ExitCode.NO_TESTS_COLLECTED

    # incorrect module dependencie format
    test_2="""
        import pytest

        pytestmark = pytest.mark.dependency(":::")

        def test_a():
            assert True
    """
    pytester.makepyfile(test_2)
    result = pytester.runpytest(*hardpy_opts)
    assert result.ret == ExitCode.NO_TESTS_COLLECTED


def test_not_exist_case(pytester: Pytester, hardpy_opts: list):
    test_1="""
        import pytest

        pytestmark = pytest.mark.dependency("test_1::a")

        def test_a():
            assert True
    """
    pytester.makepyfile(test_1)
    result = pytester.runpytest(*hardpy_opts)
    result.assert_outcomes(passed=1)

    test_2="""
        import pytest

        @pytest.mark.dependency("test_2::a")
        def test_a():
            assert True
    """
    pytester.makepyfile(test_2)
    result = pytester.runpytest(*hardpy_opts)
    result.assert_outcomes(passed=1)


def test_not_exist_module(pytester: Pytester, hardpy_opts: list):
    test_1="""
        import pytest

        pytestmark = pytest.mark.dependency("a")

        def test_a():
            assert True
    """
    pytester.makepyfile(test_1)
    result = pytester.runpytest(*hardpy_opts)
    result.assert_outcomes(passed=1)

    test_2="""
        import pytest

        def test_a():
            assert True

        @pytest.mark.dependency("a")
        def test_b():
            assert False

        def test_c():
            assert True
    """
    pytester.makepyfile(test_2)
    result = pytester.runpytest(*hardpy_opts)
    result.assert_outcomes(passed=2, failed=1)

def test_not_exist_module_and_case(pytester: Pytester, hardpy_opts: list):
    test_1="""
        import pytest

        pytestmark = pytest.mark.dependency("a::b")

        def test_a():
            assert True
    """
    pytester.makepyfile(test_1)
    result = pytester.runpytest(*hardpy_opts)
    result.assert_outcomes(passed=1)

    test_2="""
        import pytest

        def test_a():
            assert True

        @pytest.mark.dependency("a::b")
        def test_b():
            assert False

        def test_c():
            assert True
    """
    pytester.makepyfile(test_2)
    result = pytester.runpytest(*hardpy_opts)
    result.assert_outcomes(passed=2, failed=1)


