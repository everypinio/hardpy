from pytest import Pytester


def test_clearing_user(
    pytester: Pytester,
    jig_opts: list[str],
    jig_opts_repeat: list[str],
):
    pytester.makepyfile(
        """
        import pytest
        import jig

        def test_passed():
            report = jig.get_current_report()
            user = report.user
            assert user is None, "User name is not empty before start."

            name = "test_user"
            jig.set_user_name(name)
    """,
    )
    result = pytester.runpytest(*jig_opts)
    result.assert_outcomes(passed=1)

    result = pytester.runpytest(*jig_opts_repeat)
    result.assert_outcomes(passed=1)


def test_clearing_batch_sn(
    pytester: Pytester,
    jig_opts: list[str],
    jig_opts_repeat: list[str],
):
    pytester.makepyfile(
        """
        import pytest
        import jig

        def test_passed():
            report = jig.get_current_report()
            batch_sn = report.batch_serial_number
            assert batch_sn is None, "Batch serial number is not empty before start."

            batch_sn = "111"
            jig.set_batch_serial_number(batch_sn)
    """,
    )
    result = pytester.runpytest(*jig_opts)
    result.assert_outcomes(passed=1)

    result = pytester.runpytest(*jig_opts_repeat)
    result.assert_outcomes(passed=1)


def test_clearing_run_artifact(
    pytester: Pytester,
    jig_opts: list[str],
    jig_opts_repeat: list[str],
):
    pytester.makepyfile(
        """
        import pytest
        import jig

        def test_passed():
            report = jig.get_current_report()
            artifact = report.artifact
            assert artifact == dict(), "Test run artifact is not empty before start."

            artifact_data = {"data_str": "456DATA"}
            jig.set_run_artifact(artifact_data)
    """,
    )
    result = pytester.runpytest(*jig_opts)
    result.assert_outcomes(passed=1)

    result = pytester.runpytest(*jig_opts_repeat)
    result.assert_outcomes(passed=1)


def test_clearing_error_code_and_caused_dut_failure(
    pytester: Pytester,
    jig_opts: list[str],
    jig_opts_repeat: list[str],
):
    pytester.makepyfile(
        """
        import pytest
        import jig

        def test_passed():
            report = jig.get_current_report()
            error_code = report.error_code
            assert error_code is None, "Error code is not empty before start."
            caused_dut_failure_id = report.caused_dut_failure_id
            assert caused_dut_failure_id is None, "Caused DUT failure id is not empty before start."

        def test_failed():
            assert False, jig.ErrorCode(1)
    """,  # noqa: E501
    )
    result = pytester.runpytest(*jig_opts)
    result.assert_outcomes(passed=1, failed=1)

    result = pytester.runpytest(*jig_opts_repeat)
    result.assert_outcomes(passed=1, failed=1)
