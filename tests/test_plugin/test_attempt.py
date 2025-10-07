from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from pytest import Pytester

func_test_header = """
        import pytest

        import hardpy
        """


def test_attempt_success(pytester: Pytester, hardpy_opts: list):
    pytester.makepyfile(
        test_1=f"""{func_test_header}

        from hardpy.pytest_hardpy.utils.const import TestStatus

        @pytest.mark.attempt(2)
        def test_a():
            attempt = hardpy.get_current_attempt()
            if attempt == 2:
                return
            assert False

        def test_b():
            report = hardpy.get_current_report()
            case_a_status = report.modules["test_1"].cases["test_a"].status
            assert case_a_status == TestStatus.PASSED
    """,
    )
    result = pytester.runpytest(*hardpy_opts)
    result.assert_outcomes(passed=2)


def test_attempt_failed(pytester: Pytester, hardpy_opts: list):
    pytester.makepyfile(
        test_1=f"""{func_test_header}

        from hardpy.pytest_hardpy.utils.const import TestStatus

        @pytest.mark.attempt(2)
        def test_a():
            assert False

        def test_b():
            report = hardpy.get_current_report()
            case_a_status = report.modules["test_1"].cases["test_a"].status
            assert case_a_status == TestStatus.FAILED
    """,
    )
    result = pytester.runpytest(*hardpy_opts)
    result.assert_outcomes(passed=1, failed=1)


def test_critical_with_attempt_passed_on_retry(
    pytester: Pytester,
    hardpy_opts: list[str],
):
    """Critical test with attempt marker that passes on a retry."""
    pytester.makepyfile(
        test_1=f"""{func_test_header}

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
        test_2="""
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
        test_1=f"""{func_test_header}

        @pytest.mark.critical
        @pytest.mark.attempt(3)
        def test_one():
            assert False

        """,
        test_2="""
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
        test_1=f"""{func_test_header}

        attempt_count = 0

        @pytest.mark.critical
        @pytest.mark.attempt(3)
        def test_one():
            global attempt_count
            attempt_count += 1
            if attempt_count < 2:
                assert False
            assert True

        @pytest.mark.dependency("test_1::test_one")
        def test_two():
            assert True
        """,
        test_2="""
        def test_three():
            assert True
        """,
    )
    result = pytester.runpytest(*hardpy_opts)
    # First test passes after retries, dependencies should run
    result.assert_outcomes(passed=3)


def test_caused_dut_failure_id_second_with_attempt(
    pytester: Pytester,
    hardpy_opts: list,
):
    """Caused DUT failure id is not filled if there is a successful attempt."""
    pytester.makepyfile(
        test_1=f"""{func_test_header}

        @pytest.mark.attempt(2)
        def test_a():
            attempt = hardpy.get_current_attempt()
            if attempt == 2:
                return
            assert False

        def test_b():
            assert False
    """,
        test_2=f"""
        {func_test_header}

        @pytest.mark.attempt(2)
        def test_a():
            report = hardpy.get_current_report()

            caused_dut_failure_id = report.caused_dut_failure_id
            assert caused_dut_failure_id == "test_1::test_b"
    """,
    )
    result = pytester.runpytest(*hardpy_opts)
    result.assert_outcomes(passed=2, failed=1)


def test_error_code_empty_after_success_attempt(pytester: Pytester, hardpy_opts: list):
    pytester.makepyfile(
        f"""
        {func_test_header}
        @pytest.mark.attempt(2)
        def test_a():
            attempt = hardpy.get_current_attempt()
            if attempt == 2:
                return
            assert False, hardpy.ErrorCode(1)

        def test_b():
            report = hardpy.get_current_report()
            error_code = report.error_code
            assert error_code is None , "The error_code must be empty."
    """,
    )
    result = pytester.runpytest(*hardpy_opts)
    result.assert_outcomes(passed=2)


def test_success_attempt_after_error_code(pytester: Pytester, hardpy_opts: list):
    pytester.makepyfile(
        f"""
        {func_test_header}
        def test_a():
            assert False, hardpy.ErrorCode(1)

        @pytest.mark.attempt(2)
        def test_b():
            attempt = hardpy.get_current_attempt()
            if attempt == 2:
                return
            assert False, hardpy.ErrorCode(2)

        def test_c():
            report = hardpy.get_current_report()
            error_code = report.error_code
            assert error_code == 1 , "The error_code does not come from test_a."
    """,
    )
    result = pytester.runpytest(*hardpy_opts)
    result.assert_outcomes(passed=2, failed=1)


def test_different_error_code_some_attempt(pytester: Pytester, hardpy_opts: list):
    pytester.makepyfile(
        f"""{func_test_header}
        @pytest.mark.attempt(2)
        def test_1():
            attempt = hardpy.get_current_attempt()
            assert False, hardpy.ErrorCode(attempt)

        def test_2():
            assert False, hardpy.ErrorCode(3)

        def test_current_error_code():
            report = hardpy.get_current_report()
            assert report.error_code == 2
    """,
    )
    result = pytester.runpytest(*hardpy_opts)
    result.assert_outcomes(passed=1, failed=2)


def test_clear_case_data(pytester: Pytester, hardpy_opts: list):
    pytester.makepyfile(
        test_1=f"""{func_test_header}
        @pytest.mark.attempt(2)
        def test_a():
            report = hardpy.get_current_report()
            assert report.modules["test_1"].cases["test_a"].assertion_msg == None
            assert report.modules["test_1"].cases["test_a"].msg == None
            assert report.modules["test_1"].cases["test_a"].measurements == []
            assert report.modules["test_1"].cases["test_a"].chart == None
            assert report.modules["test_1"].cases["test_a"].artifact == {{}}

            hardpy.set_message("a")
            chart = hardpy.Chart(
                type=hardpy.ChartType.LINE,
                title="title",
                x_label="x_label",
                y_label="y_label",
                marker_name=["marker_name", None],
                x_data=[[1, 2], [1, 2]],
                y_data=[[3, 4], [3, 4]]
            )
            hardpy.set_case_chart(chart)
            meas = hardpy.NumericMeasurement(value=1)
            hardpy.set_case_measurement(meas)
            artifact_data = {{"data_str": "123DATA"}}
            hardpy.set_case_artifact(artifact_data)

            attempt = hardpy.get_current_attempt()
            if attempt == 2:
                return
            assert False, "Test failed"
    """,
    )
    result = pytester.runpytest(*hardpy_opts)
    result.assert_outcomes(passed=1)
