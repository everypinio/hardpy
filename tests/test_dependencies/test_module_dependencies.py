from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from pytest import Pytester

status_test_header = """
        import pytest
        """


def test_module_dependency_from_passed_case(pytester: Pytester, hardpy_opts: list[str]):
    pytester.makepyfile(
        test_1="""
        import pytest
        def test_one():
            assert True
    """,
    )
    pytester.makepyfile(
        test_2="""
        import pytest
        pytestmark = pytest.mark.dependency("test_1::test_one")
        def test_one():
            assert True
    """,
    )
    result = pytester.runpytest(*hardpy_opts)
    result.assert_outcomes(passed=2)


def test_module_dependency_from_failed_case(pytester: Pytester, hardpy_opts: list[str]):
    pytester.makepyfile(
        test_1="""
        import pytest
        def test_one():
            assert False
    """,
    )
    pytester.makepyfile(
        test_2="""
        import pytest
        pytestmark = pytest.mark.dependency("test_1::test_one")
        def test_one():
            assert True
    """,
    )
    result = pytester.runpytest(*hardpy_opts)
    result.assert_outcomes(failed=1, skipped=1)


def test_module_dependency_from_skipped_case(
    pytester: Pytester,
    hardpy_opts: list[str],
):
    pytester.makepyfile(
        test_1="""
        import pytest

        def test_one():
            assert False
    """,
    )
    pytester.makepyfile(
        test_2="""
        import pytest

        pytestmark = pytest.mark.dependency("test_1::test_one")

        def test_one():
            assert True
    """,
    )
    pytester.makepyfile(
        test_3="""
        import pytest

        pytestmark = pytest.mark.dependency("test_2::test_one")

        def test_one():
            assert True
    """,
    )
    result = pytester.runpytest(*hardpy_opts)
    result.assert_outcomes(failed=1, skipped=2)


def test_module_dependency_chained(pytester: Pytester, hardpy_opts: list[str]):
    pytester.makepyfile(
        test_1="""
        import pytest
        def test_one():
            assert True
    """,
    )
    pytester.makepyfile(
        test_2="""
        import pytest
        pytestmark = pytest.mark.dependency("test_1::test_one")
        def test_one():
            assert False
    """,
    )
    pytester.makepyfile(
        test_3="""
        import pytest
        pytestmark = pytest.mark.dependency("test_2::test_one")
        def test_one():
            assert True
    """,
    )
    result = pytester.runpytest(*hardpy_opts)
    result.assert_outcomes(passed=1, failed=1, skipped=1)


def test_case_dependency_from_module(pytester: Pytester, hardpy_opts: list[str]):
    pytester.makepyfile(
        test_1="""
        import pytest

        def test_one():
            assert False
    """,
    )
    pytester.makepyfile(
        test_2="""
        import pytest

        pytestmark = pytest.mark.dependency("test_1")

        def test_one():
            assert True
    """,
    )
    result = pytester.runpytest(*hardpy_opts)
    result.assert_outcomes(failed=1, skipped=1)
