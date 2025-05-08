from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from pytest import Pytester


def test_module_dependency_from_passed_case(pytester: Pytester, hardpy_opts: list):
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

        pytestmark = pytest.mark.dependency("test_1::test_a")

        def test_a():
            assert True
    """,
    )
    result = pytester.runpytest(*hardpy_opts)
    result.assert_outcomes(passed=2)


def test_module_dependency_from_failed_case(pytester: Pytester, hardpy_opts: list):
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

        pytestmark = pytest.mark.dependency("test_1::test_a")

        def test_a():
            assert True
    """,
    )
    result = pytester.runpytest(*hardpy_opts)
    result.assert_outcomes(failed=1, skipped=1)


def test_module_dependency_from_skipped_case(pytester: Pytester, hardpy_opts: list):
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

        pytestmark = pytest.mark.dependency("test_1::test_a")

        def test_a():
            assert True
    """,
    )
    pytester.makepyfile(
        test_3="""
        import pytest

        pytestmark = pytest.mark.dependency("test_2::test_a")

        def test_a():
            assert True
    """,
    )
    result = pytester.runpytest(*hardpy_opts)
    result.assert_outcomes(failed=1, skipped=2)


def test_module_dependency_chained(pytester: Pytester, hardpy_opts: list):
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

        pytestmark = pytest.mark.dependency("test_1::test_a")

        def test_a():
            assert False
    """,
    )
    pytester.makepyfile(
        test_3="""
        import pytest

        pytestmark = pytest.mark.dependency("test_2::test_a")

        def test_a():
            assert True
    """,
    )
    result = pytester.runpytest(*hardpy_opts)
    result.assert_outcomes(passed=1, failed=1, skipped=1)


def test_module_dependency_from_module(pytester: Pytester, hardpy_opts: list):
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

        pytestmark = pytest.mark.dependency("test_1")

        def test_a():
            assert True

        def test_b():
            assert False
    """,
    )
    result = pytester.runpytest(*hardpy_opts)
    result.assert_outcomes(failed=1, skipped=2)



