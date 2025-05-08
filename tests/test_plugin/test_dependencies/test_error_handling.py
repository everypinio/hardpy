from __future__ import annotations

from typing import TYPE_CHECKING

from pytest import ExitCode

if TYPE_CHECKING:
    from pytest import Pytester


def test_case_dependency_with_incorrect_data(
    pytester: Pytester,
    hardpy_opts: list[str],
):
    pytester.makepyfile(
        test_1="""
        import pytest
        @pytest.mark.dependency(":::")
        def test_one():
            assert True
    """,
    )
    result = pytester.runpytest(*hardpy_opts)
    assert result.ret == ExitCode.NO_TESTS_COLLECTED


def test_module_dependency_with_incorrect_data(
    pytester: Pytester,
    hardpy_opts: list[str],
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

        pytestmark = pytest.mark.dependency(":::")

        def test_one():
            assert True
    """,
    )
    result = pytester.runpytest(*hardpy_opts)
    assert result.ret == ExitCode.NO_TESTS_COLLECTED


def test_module_dependency_with_incorrect_case(
    pytester: Pytester,
    hardpy_opts: list[str],
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

        pytestmark = pytest.mark.dependency("test_1::fghdjshfj")

        def test_one():
            assert True
    """,
    )
    result = pytester.runpytest(*hardpy_opts)
    result.assert_outcomes(passed=2)


def test_case_dependency_with_incorrect_module_and_case(
    pytester: Pytester,
    hardpy_opts: list[str],
):
    pytester.makepyfile(
        test_1="""
        import pytest

        @pytest.mark.dependency("kuhfkhgf::qwqw")
        def test_one():
            assert True

        @pytest.mark.dependency("kuhfkhgf::qwqw")
        def test_two():
            assert False
    """,
    )
    result = pytester.runpytest(*hardpy_opts)
    result.assert_outcomes(passed=1, failed=1)


def test_case_dependency_with_incorrect_module(
    pytester: Pytester,
    hardpy_opts: list[str],
):
    pytester.makepyfile(
        test_1="""
        import pytest

        @pytest.mark.dependency("kuhfkhgf")
        def test_one():
            assert True

        @pytest.mark.dependency("kuhfkhgf")
        def test_two():
            assert False
    """,
    )
    result = pytester.runpytest(*hardpy_opts)
    result.assert_outcomes(passed=1, failed=1)


def test_module_dependency_with_incorrect_module_and_correct_case(
    pytester: Pytester,
    hardpy_opts: list[str],
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

        pytestmark = pytest.mark.dependency("asfddaa::test_one")

        def test_one():
            assert True
    """,
    )
    result = pytester.runpytest(*hardpy_opts)
    result.assert_outcomes(passed=2)
