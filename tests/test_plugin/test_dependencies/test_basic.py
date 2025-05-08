from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from pytest import Pytester


def test_case_dependency_from_passed(pytester: Pytester, hardpy_opts: list[str]):
    pytester.makepyfile(
        test_1="""
        import pytest

        def test_one():
            assert True

        @pytest.mark.dependency("test_1::test_one")
        def test_two():
            assert True
    """,
    )
    result = pytester.runpytest(*hardpy_opts)
    result.assert_outcomes(passed=2)


def test_case_dependency_from_failed(pytester: Pytester, hardpy_opts: list[str]):
    pytester.makepyfile(
        test_1="""
        import pytest

        def test_one():
            assert False

        @pytest.mark.dependency("test_1::test_one")
        def test_two():
            assert False
    """,
    )
    result = pytester.runpytest(*hardpy_opts)
    result.assert_outcomes(failed=1, skipped=1)


def test_case_dependency_from_skipped(pytester: Pytester, hardpy_opts: list[str]):
    pytester.makepyfile(
        test_1="""
        import pytest

        def test_one():
            assert False

        @pytest.mark.dependency("test_1::test_one")
        def test_two():
            assert False

        @pytest.mark.dependency("test_1::test_two")
        def test_three():
            assert True
    """,
    )
    result = pytester.runpytest(*hardpy_opts)
    result.assert_outcomes(failed=1, skipped=2)


def test_case_dependency_from_not_skipped(pytester: Pytester, hardpy_opts: list[str]):
    pytester.makepyfile(
        test_1="""
        import pytest

        def test_one():
            assert True

        @pytest.mark.dependency("test_1::test_one")
        def test_two():
            assert True

        @pytest.mark.dependency("test_1::test_two")
        def test_five():
            assert True
    """,
    )
    result = pytester.runpytest(*hardpy_opts)
    result.assert_outcomes(passed=3)
