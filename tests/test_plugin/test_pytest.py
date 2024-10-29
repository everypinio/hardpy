from pytest import Pytester


def test_correct_db_url(pytester: Pytester):
    pytester.makepyfile(
        """
        import pytest

        def test_passed():
            assert True
    """,
    )
    result = pytester.runpytest("--hardpy-pt")
    result.assert_outcomes(passed=1)
