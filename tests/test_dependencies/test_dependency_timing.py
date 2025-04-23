from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from pytest import Pytester

status_test_header = """
        import pytest
        """


def test_module_stop_time_first_case_skip(pytester: Pytester, hardpy_opts: list[str]):
    """Check module stop time.

    PR-129: https://github.com/everypinio/hardpy/pull/129
    """
    pytester.makeconftest(
        """
        import pytest
        import hardpy

        def finish_executing():
            report = hardpy.get_current_report()

            module_stop_time = report.modules["test_1"].stop_time
            module_start_time = report.modules["test_1"].start_time

            assert module_stop_time >= module_start_time

            case_2_stop_time = report.modules["test_1"].cases["test_two"].stop_time
            case_2_start_time = report.modules["test_1"].cases["test_two"].start_time

            assert case_2_stop_time is None
            assert case_2_start_time is None

        @pytest.fixture(scope="session", autouse=True)
        def actions_after(post_run_functions: list):
            post_run_functions.append(finish_executing)
            yield
    """,
    )
    pytester.makepyfile(
        test_1="""
        import pytest

        def test_one():
            assert False

        @pytest.mark.dependency("test_1::test_one")
        def test_two():
            assert True
    """,
    )

    result = pytester.runpytest(*hardpy_opts)
    result.assert_outcomes(passed=0, failed=1, skipped=1)


def test_first_case_skip_third_case_pass(pytester: Pytester, hardpy_opts: list[str]):
    """Check module stop time.

    PR-129: https://github.com/everypinio/hardpy/pull/129
    """
    pytester.makeconftest(
        """
        import pytest
        import hardpy

        def finish_executing():
            report = hardpy.get_current_report()

            module_stop_time = report.modules["test_1"].stop_time
            module_start_time = report.modules["test_1"].start_time

            assert module_stop_time >= module_start_time

            case_2_stop_time = report.modules["test_1"].cases["test_two"].stop_time
            case_2_start_time = report.modules["test_1"].cases["test_two"].start_time

            assert case_2_stop_time is None
            assert case_2_start_time is None

            case_3_stop_time = report.modules["test_1"].cases["test_three"].stop_time
            case_3_start_time = report.modules["test_1"].cases["test_three"].start_time

            assert case_3_stop_time >= case_3_start_time

        @pytest.fixture(scope="session", autouse=True)
        def actions_after(post_run_functions: list):
            post_run_functions.append(finish_executing)
            yield
    """,
    )
    pytester.makepyfile(
        test_1="""
        import pytest

        def test_one():
            assert False

        @pytest.mark.dependency("test_1::test_one")
        def test_two():
            assert True

        def test_three():
            assert True
    """,
    )

    result = pytester.runpytest(*hardpy_opts)
    result.assert_outcomes(passed=1, failed=1, skipped=1)


def test_last_case_skip_from_2_file(pytester: Pytester, hardpy_opts: list[str]):
    """Check module stop time.

    PR-129: https://github.com/everypinio/hardpy/pull/129
    """
    pytester.makeconftest(
        """
        import pytest
        import hardpy

        def finish_executing():
            report = hardpy.get_current_report()

            module_1_stop_time = report.modules["test_1"].stop_time
            module_1_start_time = report.modules["test_1"].start_time

            assert module_1_stop_time >= module_1_start_time

            module_2_stop_time = report.modules["test_2"].stop_time
            module_2_start_time = report.modules["test_2"].start_time

            assert module_2_stop_time >= module_2_start_time

            case_2_stop_time = report.modules["test_2"].cases["test_two"].stop_time
            case_2_start_time = report.modules["test_2"].cases["test_two"].start_time

            assert case_2_stop_time is None
            assert case_2_start_time is None

        @pytest.fixture(scope="session", autouse=True)
        def actions_after(post_run_functions: list):
            post_run_functions.append(finish_executing)
            yield
    """,
    )
    pytester.makepyfile(
        test_1="""
        import pytest

        def test_one():
            assert False
    """,
    )
    pytester.makepyfile(
        test_2="""
        import pytest

        @pytest.mark.dependency("test_1::test_one")
        def test_two():
            assert True
    """,
    )

    result = pytester.runpytest(*hardpy_opts)
    result.assert_outcomes(passed=0, failed=1, skipped=1)


def test_penultimate_case_skip_from_second_file(
    pytester: Pytester,
    hardpy_opts: list[str],
):
    """Check module stop time.

    PR-129: https://github.com/everypinio/hardpy/pull/129
    """
    pytester.makeconftest(
        """
        import pytest
        import hardpy

        def finish_executing():
            report = hardpy.get_current_report()

            module_1_stop_time = report.modules["test_1"].stop_time
            module_1_start_time = report.modules["test_1"].start_time

            assert module_1_stop_time >= module_1_start_time

            module_2_stop_time = report.modules["test_2"].stop_time
            module_2_start_time = report.modules["test_2"].start_time

            assert module_2_stop_time >= module_2_start_time

            case_2_stop_time = report.modules["test_2"].cases["test_two"].stop_time
            case_2_start_time = report.modules["test_2"].cases["test_two"].start_time

            assert case_2_stop_time is None
            assert case_2_start_time is None

            case_3_stop_time = report.modules["test_2"].cases["test_three"].stop_time
            case_3_start_time = report.modules["test_2"].cases["test_three"].start_time

            assert case_3_stop_time >= case_3_start_time

        @pytest.fixture(scope="session", autouse=True)
        def actions_after(post_run_functions: list):
            post_run_functions.append(finish_executing)
            yield
    """,
    )
    pytester.makepyfile(
        test_1="""
        import pytest

        def test_one():
            assert False
    """,
    )
    pytester.makepyfile(
        test_2="""
        import pytest

        @pytest.mark.dependency("test_1::test_one")
        def test_two():
            assert True

        def test_three():
            assert True
    """,
    )

    result = pytester.runpytest(*hardpy_opts)
    result.assert_outcomes(passed=1, failed=1, skipped=1)


def test_first_case_user_skip(pytester: Pytester, hardpy_opts: list[str]):
    """Check stop_time in test skipped by user.

    PR-129: https://github.com/everypinio/hardpy/pull/129
    """
    pytester.makeconftest(
        """
        import pytest
        import hardpy

        def finish_executing():
            report = hardpy.get_current_report()

            module_stop_time = report.modules["test_1"].stop_time
            module_start_time = report.modules["test_1"].start_time

            assert module_stop_time >= module_start_time

            case_1_stop_time = report.modules["test_1"].cases["test_one"].stop_time
            case_1_start_time = report.modules["test_1"].cases["test_one"].start_time

            assert case_1_stop_time >= case_1_start_time

            case_2_stop_time = report.modules["test_1"].cases["test_two"].stop_time
            case_2_start_time = report.modules["test_1"].cases["test_two"].start_time

            assert case_2_stop_time is None
            assert case_2_start_time is None

        @pytest.fixture(scope="session", autouse=True)
        def actions_after(post_run_functions: list):
            post_run_functions.append(finish_executing)
            yield
    """,
    )
    pytester.makepyfile(
        test_1="""
        import pytest

        def test_one():
            pytest.skip()

        @pytest.mark.dependency("test_1::test_one")
        def test_two():
            assert True
    """,
    )

    result = pytester.runpytest(*hardpy_opts)
    result.assert_outcomes(passed=0, failed=0, skipped=2)
