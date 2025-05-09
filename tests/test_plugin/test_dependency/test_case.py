from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from pytest import Pytester


def test_case_passed(pytester: Pytester, hardpy_opts: list):
    pytester.makepyfile(
        test_1="""
        import pytest

        def test_a():
            assert True

        @pytest.mark.dependency("test_1::test_a")
        def test_b():
            assert True
    """,
    )
    result = pytester.runpytest(*hardpy_opts)
    result.assert_outcomes(passed=2)


def test_case_failed(pytester: Pytester, hardpy_opts: list):
    pytester.makepyfile(
        test_1="""
        import pytest

        def test_a():
            assert False

        @pytest.mark.dependency("test_1::test_a")
        def test_b():
            assert True
    """,
    )
    result = pytester.runpytest(*hardpy_opts)
    result.assert_outcomes(failed=1, skipped=1)


def test_case_skipped(pytester: Pytester, hardpy_opts: list):
    pytester.makepyfile(
        test_1="""
        import pytest

        def test_a():
            assert False

        @pytest.mark.dependency("test_1::test_a")
        def test_b():
            assert True

        @pytest.mark.dependency("test_1::test_b")
        def test_c():
            assert True
    """,
    )
    result = pytester.runpytest(*hardpy_opts)
    result.assert_outcomes(failed=1, skipped=2)


def test_case_not_skipped(pytester: Pytester, hardpy_opts: list):
    pytester.makepyfile(
        test_1="""
        import pytest

        def test_a():
            assert True

        @pytest.mark.dependency("test_1::test_a")
        def test_b():
            assert True

        @pytest.mark.dependency("test_1::test_b")
        def test_c():
            assert True
    """,
    )
    result = pytester.runpytest(*hardpy_opts)
    result.assert_outcomes(passed=3)

def test_module_passed(pytester: Pytester, hardpy_opts: list):
    pytester.makepyfile(
        test_1="""
        import pytest

        def test_a():
            assert True
    """,
    )
    pytester.makepyfile(
        test_2="""
        import pytest

        @pytest.mark.dependency("test_1")
        def test_a():
            assert True

        def test_b():
            assert True
    """,
    )
    result = pytester.runpytest(*hardpy_opts)
    result.assert_outcomes(passed=3)


def test_module_skipped(pytester: Pytester, hardpy_opts: list):
    pytester.makepyfile(
        test_1="""
        import pytest

        def test_a():
            assert False
    """,
    )
    pytester.makepyfile(
        test_2="""
        import pytest

        @pytest.mark.dependency("test_1")
        def test_a():
            assert True

        def test_b():
            assert True
    """,
    )
    result = pytester.runpytest(*hardpy_opts)
    result.assert_outcomes(failed=1, skipped=1, passed=1)
