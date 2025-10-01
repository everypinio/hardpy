from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from pytest import Pytester


import_header = """
        import pytest
        import hardpy
"""

conftest_actions_after = """
        @pytest.fixture(scope="session", autouse=True)
        def actions_after(post_run_functions: list):
            post_run_functions.append(finish_executing)
            yield
"""


def test_caused_dut_failure_id_empty(pytester: Pytester, hardpy_opts: list):
    """Caused DUT failure id empty by default."""
    pytester.makeconftest(
        f"""
        {import_header}

        def finish_executing():
            report = hardpy.get_current_report()

            caused_dut_failure_id = report.caused_dut_failure_id
            assert caused_dut_failure_id is None

        {conftest_actions_after}
    """,
    )
    pytester.makepyfile(
        test_1="""
        import pytest

        def test_a():
            assert True
    """,
    )
    result = pytester.runpytest(*hardpy_opts)
    result.assert_outcomes(passed=1)


def test_caused_dut_failure_id_single(pytester: Pytester, hardpy_opts: list):
    """Caused DUT failure id is filled."""
    pytester.makeconftest(
        f"""
        {import_header}

        def finish_executing():
            report = hardpy.get_current_report()

            caused_dut_failure_id = report.caused_dut_failure_id
            assert caused_dut_failure_id == "test_1::test_a"

        {conftest_actions_after}
    """,
    )
    pytester.makepyfile(
        test_1="""
        import pytest

        def test_a():
            assert False
    """,
    )
    result = pytester.runpytest(*hardpy_opts)
    result.assert_outcomes(failed=1)


def test_caused_dut_failure_id_first(pytester: Pytester, hardpy_opts: list):
    """Caused DUT failure id is filled by first failure test."""
    pytester.makeconftest(
        f"""
        {import_header}

        def finish_executing():
            report = hardpy.get_current_report()

            caused_dut_failure_id = report.caused_dut_failure_id
            assert caused_dut_failure_id == "test_1::test_a"

        {conftest_actions_after}
    """,
    )
    pytester.makepyfile(
        test_1="""
        import pytest

        def test_a():
            assert False

        def test_b():
            assert False
    """,
    )
    result = pytester.runpytest(*hardpy_opts)
    result.assert_outcomes(failed=2)


def test_caused_dut_failure_skip(pytester: Pytester, hardpy_opts: list):
    """Caused DUT failure id is not filled by skipped test."""
    pytester.makeconftest(
        f"""
        {import_header}

        def finish_executing():
            report = hardpy.get_current_report()

            caused_dut_failure_id = report.caused_dut_failure_id
            assert caused_dut_failure_id == "test_1::test_b"

        {conftest_actions_after}
    """,
    )
    pytester.makepyfile(
        test_1="""
        import pytest

        def test_a():
            pytest.skip()

        def test_b():
            assert False
    """,
    )
    result = pytester.runpytest(*hardpy_opts)
    result.assert_outcomes(skipped=1, failed=1)
