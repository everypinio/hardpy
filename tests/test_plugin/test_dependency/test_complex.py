from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from pytest import Pytester


def test_multiple_module_dependencies_passed(pytester: Pytester, hardpy_opts: list):
    """Verify handling of multiple dependencies with mixed results.

    PR-130: https://github.com/everypinio/hardpy/pull/130
    """
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

        def test_a():
            assert True
        """,
    )
    pytester.makepyfile(
        test_3="""
        import pytest

        pytestmark = [
            pytest.mark.dependency("test_1::test_a"),
            pytest.mark.dependency("test_2::test_a"),
        ]

        def test_c():
            assert True
        """,
    )
    result = pytester.runpytest(*hardpy_opts)
    result.assert_outcomes(passed=3)


def test_multiple_module_dependencies_skipped(pytester: Pytester, hardpy_opts: list):
    """Verify handling of multiple dependencies with mixed results.

    PR-130: https://github.com/everypinio/hardpy/pull/130
    """
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

        def test_a():
            assert False
        """,
    )
    pytester.makepyfile(
        test_3="""
        import pytest

        pytestmark = [
            pytest.mark.dependency("test_1::test_a"),
            pytest.mark.dependency("test_2::test_a"),
        ]

        def test_c():
            assert True
        """,
    )
    result = pytester.runpytest(*hardpy_opts)
    result.assert_outcomes(passed=1, failed=1, skipped=1)


def test_module_by_module_skipped(pytester: Pytester, hardpy_opts: list):
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

        pytestmark = [
            pytest.mark.dependency("test_1::test_a"),
            pytest.mark.dependency("test_2::test_a"),
        ]

        def test_a():
            assert True
        """,
    )
    pytester.makepyfile(
        test_4="""
        import pytest

        pytestmark = pytest.mark.dependency("test_3")

        def test_a():
            assert True
        """,
    )
    result = pytester.runpytest(*hardpy_opts)
    result.assert_outcomes(passed=1, failed=1, skipped=2)


def test_module_by_module_passed(pytester: Pytester, hardpy_opts: list):
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
    pytester.makepyfile(
        test_3="""
        import pytest

        pytestmark = [
            pytest.mark.dependency("test_1::test_a"),
            pytest.mark.dependency("test_2::test_a"),
        ]

        def test_a():
            assert True
        """,
    )
    pytester.makepyfile(
        test_4="""
        import pytest

        pytestmark = pytest.mark.dependency("test_3")

        def test_a():
            assert True
        """,
    )
    result = pytester.runpytest(*hardpy_opts)
    result.assert_outcomes(passed=4)


def test_module_by_module_failed(pytester: Pytester, hardpy_opts: list):
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
        """,
    )
    pytester.makepyfile(
        test_3="""
        import pytest

        pytestmark = [
            pytest.mark.dependency("test_1"),
            pytest.mark.dependency("test_2"),
        ]

        def test_a():
            assert True
        """,
    )
    pytester.makepyfile(
        test_4="""
        import pytest

        pytestmark = pytest.mark.dependency("test_3::test_a")

        def test_a():
            assert True
        """,
    )
    result = pytester.runpytest(*hardpy_opts)
    result.assert_outcomes(failed=1, skipped=3)


def test_multiple_case_dependencies(pytester: Pytester, hardpy_opts: list):
    """Verify multiple dependencies within a single test case.

    PR-130: https://github.com/everypinio/hardpy/pull/130
    """
    pytester.makepyfile(
        test_1="""
        import pytest

        def test_a():
            assert True

        def test_b():
            assert True

        def test_c():
            assert False

        @pytest.mark.dependency("test_1::test_a")
        @pytest.mark.dependency("test_1::test_b")
        @pytest.mark.dependency("test_1::test_c")
        def test_d():
            assert True

        def test_e():
            assert True
    """,
    )
    result = pytester.runpytest(*hardpy_opts)
    result.assert_outcomes(passed=3, failed=1, skipped=1)

def test_module_failed_case_dependencies_passed(pytester: Pytester, hardpy_opts: list):
    """Added by https://github.com/everypinio/hardpy/pull/143 PR-143."""
    pytester.makepyfile(
        test_1="""
        import pytest

        def test_a():
            assert True

        def test_b():
            assert False

        @pytest.mark.dependency("test_1::test_a")
        def test_c() -> None:
            assert True
    """,
    )
    pytester.makepyfile(
        test_2="""
        import pytest

        @pytest.mark.dependency("test_1::test_a")
        def test_a():
            assert True

        def test_b():
            assert True

        def test_c() -> None:
            assert True
    """,
    )
    result = pytester.runpytest(*hardpy_opts)
    result.assert_outcomes(failed=1, passed=5)


def test_module_failed_case_dependencies_skipped(pytester: Pytester, hardpy_opts: list):
    """Added by https://github.com/everypinio/hardpy/pull/143 PR-143."""
    pytester.makepyfile(
        test_1="""
        import pytest

        def test_a():
            assert False

        def test_b():
            assert False

        @pytest.mark.dependency("test_1::test_a")
        def test_c() -> None:
            assert True
    """,
    )
    pytester.makepyfile(
        test_2="""
        import pytest

        @pytest.mark.dependency("test_1::test_a")
        def test_a():
            assert True

        def test_b():
            assert True

        def test_c() -> None:
            assert True
    """,
    )
    result = pytester.runpytest(*hardpy_opts)
    result.assert_outcomes(failed=2, passed=2, skipped=2)
