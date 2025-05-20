from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from pytest import Pytester

status_test_header = """
        import pytest
        """


def test_critical_with_attempt_passed_on_retry(
    pytester: Pytester,
    hardpy_opts: list[str],
):
    """Critical test with attempt marker that passes on a retry."""
    pytester.makepyfile(
        test_file="""
        import pytest

        attempt_count = 0

        @pytest.mark.critical
        @pytest.mark.attempt(3)
        def test_retry_pass():
            global attempt_count
            attempt_count += 1
            if attempt_count < 2:
                assert False
            assert True
        """,
        test_file2="""
        def test_two():
            assert True
        """,
    )
    result = pytester.runpytest(*hardpy_opts)
    # Should pass because it eventually succeeds
    result.assert_outcomes(passed=2)


def test_critical_with_attempt_all_failed(pytester: Pytester, hardpy_opts: list[str]):
    """Critical test with attempt marker that fails all attempts."""
    pytester.makepyfile(
        test_file1="""
        import pytest

        @pytest.mark.critical
        @pytest.mark.attempt(3)
        def test_one():
            assert False

        """,
        test_file2="""
        def test_three():
            assert True
        """,
    )
    result = pytester.runpytest(*hardpy_opts)
    # Should fail (only one failure reported despite multiple attempts)
    result.assert_outcomes(failed=1, skipped=1)


def test_critical_with_attempt_dependency(pytester: Pytester, hardpy_opts: list[str]):
    """Test dependency behavior with critical test that has attempt marker."""
    pytester.makepyfile(
        test_file1="""
        import pytest

        attempt_count = 0

        @pytest.mark.critical
        @pytest.mark.attempt(3)
        def test_one():
            global attempt_count
            attempt_count += 1
            if attempt_count < 2:
                assert False
            assert True

        @pytest.mark.dependency("test_file1::test_one")
        def test_two():
            assert True
        """,
        test_file2="""
        def test_three():
            assert True
        """,
    )
    result = pytester.runpytest(*hardpy_opts)
    # First test passes after retries, dependencies should run
    result.assert_outcomes(passed=3)
