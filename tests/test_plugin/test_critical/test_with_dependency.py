from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from pytest import Pytester


import_header = """
        import pytest
        import hardpy
"""


def test_critical_with_dependency(pytester: Pytester, hardpy_opts: list[str]):
    pytester.makepyfile(
        test_file1="""
        import pytest

        @pytest.mark.critical
        def test_one():
            assert False

        @pytest.mark.dependency("test_file1::test_one")
        def test_two():
            assert True

        def test_three():
            assert True
        """,
        test_file2="""
        import pytest

        def test_one():
            assert True

        def test_two():
            assert True

        def test_three():
            assert True
        """,
    )
    result = pytester.runpytest(*hardpy_opts)
    result.assert_outcomes(failed=1, skipped=5)


def test_critical_case_with_dependency_passed(pytester: Pytester, hardpy_opts: list):
    """Critical test with dependency that passed."""
    pytester.makepyfile(
        test_1="""
        import pytest

        def test_a():
            assert True

        @pytest.mark.critical
        @pytest.mark.dependency("test_1::test_a")
        def test_b():
            assert True
    """,
    )
    result = pytester.runpytest(*hardpy_opts)
    result.assert_outcomes(passed=2)


def test_critical_case_with_dependency_failed(pytester: Pytester, hardpy_opts: list):
    """Critical test with dependency that failed."""
    pytester.makepyfile(
        test_1="""
        import pytest

        def test_a():
            assert False

        @pytest.mark.critical
        @pytest.mark.dependency("test_1::test_a")
        def test_b():
            assert True

        def test_c():
            assert True
    """,
    )
    result = pytester.runpytest(*hardpy_opts)
    result.assert_outcomes(failed=1, skipped=2)


def test_critical_case_with_skipped_dependency(pytester: Pytester, hardpy_opts: list):
    """Critical test with dependency that was skipped."""
    pytester.makepyfile(
        test_1="""
        import pytest

        def test_a():
            pytest.skip()

        @pytest.mark.critical
        @pytest.mark.dependency("test_1::test_a")
        def test_b():
            assert True
    """,
    )
    result = pytester.runpytest(*hardpy_opts)
    result.assert_outcomes(skipped=2)


def test_critical_module_with_dependency_passed(pytester: Pytester, hardpy_opts: list):
    """Critical module with dependency that passed."""
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

        pytestmark = [
            pytest.mark.critical,
            pytest.mark.dependency("test_1"),
        ]

        def test_b():
            assert True
    """,
    )
    result = pytester.runpytest(*hardpy_opts)
    result.assert_outcomes(passed=2)


def test_critical_module_with_dependency_failed(pytester: Pytester, hardpy_opts: list):
    """Critical module with dependency that failed."""
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

        pytestmark = [
            pytest.mark.critical,
            pytest.mark.dependency("test_1"),
        ]

        def test_b():
            assert True
    """,
    )
    pytester.makepyfile(
        test_3="""
        import pytest

        def test_a():
            assert False
    """,
    )
    result = pytester.runpytest(*hardpy_opts)
    result.assert_outcomes(failed=1, skipped=2)


def test_first_module_critical_failed(pytester: Pytester, hardpy_opts: list):
    """First module is critical and failed - check timing."""
    pytester.makepyfile(
        test_1="""
        import pytest

        pytestmark = pytest.mark.critical

        def test_a():
            assert False
    """,
    )
    pytester.makepyfile(
        test_2="""
        import pytest

        def test_b():
            assert True
    """,
    )
    result = pytester.runpytest(*hardpy_opts)
    result.assert_outcomes(failed=1, skipped=1)


def test_middle_module_critical_failed(pytester: Pytester, hardpy_opts: list):
    """Middle module is critical and failed - check timing."""
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

        pytestmark = pytest.mark.critical

        def test_b():
            assert False
    """,
    )
    pytester.makepyfile(
        test_3="""
        import pytest

        def test_c():
            assert True
    """,
    )
    result = pytester.runpytest(*hardpy_opts)
    result.assert_outcomes(passed=1, failed=1, skipped=1)
