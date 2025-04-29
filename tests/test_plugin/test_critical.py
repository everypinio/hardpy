from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from pytest import Pytester

status_test_header = """
        import pytest
        """


def test_critical_marker_on_passed_test(pytester: Pytester, hardpy_opts: list[str]):
    pytester.makepyfile(
        test_file1="""
        import pytest

        @pytest.mark.critical
        def test_one():
            assert True

        def test_two():
            assert True

        def test_three():
            assert True
        """,
    )
    result = pytester.runpytest(*hardpy_opts)
    result.assert_outcomes(passed=3)


def test_critical_marker_on_failed_test(pytester: Pytester, hardpy_opts: list[str]):
    pytester.makepyfile(
        test_file1="""
        import pytest

        @pytest.mark.critical
        def test_one():
            assert False

        def test_two():
            assert True

        def test_three():
            assert True
        """,
    )
    result = pytester.runpytest(*hardpy_opts)
    result.assert_outcomes(failed=1, skipped=2)


def test_critical_module_marker_on_passed(pytester: Pytester, hardpy_opts: list[str]):
    pytester.makepyfile(
        test_file1="""
        import pytest

        pytestmark = pytest.mark.critical

        def test_one():
            assert True

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
    result.assert_outcomes(passed=6)


def test_critical_module_marker_on_failed(pytester: Pytester, hardpy_opts: list[str]):
    pytester.makepyfile(
        test_file1="""
        import pytest

        pytestmark = pytest.mark.critical

        def test_one():
            assert False

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
