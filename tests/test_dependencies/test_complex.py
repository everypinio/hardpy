from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from pytest import Pytester

status_test_header = """
        import pytest
        """


def test_multiple_dependencies_mixed_results(
    pytester: Pytester, hardpy_opts: list[str],
):
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
        def test_two():
            assert False
        """,
    )
    pytester.makepyfile(
        test_3="""
        import pytest
        pytestmark = [
            pytest.mark.dependency("test_1::test_one"),
            pytest.mark.dependency("test_2::test_two"),
        ]
        def test_three():
            assert True
        """,
    )
    result = pytester.runpytest(*hardpy_opts)
    result.assert_outcomes(passed=1, failed=1, skipped=1)


def test_four_dependencies_with_module_level(
    pytester: Pytester, hardpy_opts: list[str],
):
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

        def test_one():
            assert True
        """,
    )
    pytester.makepyfile(
        test_3="""
        import pytest

        pytestmark = [
            pytest.mark.dependency("test_1::test_one"),
            pytest.mark.dependency("test_2::test_one"),
            pytest.mark.dependency("test_3::test_one"),
        ]

        def test_one():
            assert True
        """,
    )
    result = pytester.runpytest(*hardpy_opts)
    result.assert_outcomes(passed=1, failed=1, skipped=1)


def test_multiple_tests_dependencies(
    pytester: Pytester,
    hardpy_opts: list[str],
):
    pytester.makepyfile(
        test_1="""
        import pytest

        def test_one():
            assert True

        def test_two():
            assert True

        def test_three():
            assert False

        @pytest.mark.dependency("test_1::test_one")
        @pytest.mark.dependency("test_1::test_two")
        @pytest.mark.dependency("test_1::test_three")
        def test_four():
            assert True
    """,
    )
    result = pytester.runpytest(*hardpy_opts)
    result.assert_outcomes(passed=2, failed=1, skipped=1)
