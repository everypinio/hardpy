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


def test_critical_case_with_skip(pytester: Pytester, hardpy_opts: list):
    """Critical test case with skip - check timing."""
    pytester.makeconftest(
        f"""
        {import_header}

        def finish_executing():
            report = hardpy.get_current_report()

            module = report.modules["test_1"]
            assert module.stop_time >= module.start_time

            case = module.cases["test_a"]
            assert case.stop_time >= case.start_time

        {conftest_actions_after}
    """,
    )
    pytester.makepyfile(
        test_1="""
        import pytest

        @pytest.mark.critical
        def test_a():
            pytest.skip()
    """,
    )
    result = pytester.runpytest(*hardpy_opts)
    result.assert_outcomes(skipped=1)


def test_first_of_two_cases_critical_passed(pytester: Pytester, hardpy_opts: list):
    """First of two test cases is critical and passed - check timing."""
    pytester.makeconftest(
        f"""
        {import_header}

        def finish_executing():
            report = hardpy.get_current_report()

            module = report.modules["test_1"]
            assert module.stop_time >= module.start_time

            case_a = module.cases["test_a"]
            assert case_a.stop_time >= case_a.start_time

            case_b = module.cases["test_b"]
            assert case_b.stop_time >= case_b.start_time

        {conftest_actions_after}
    """,
    )
    pytester.makepyfile(
        test_1="""
        import pytest

        @pytest.mark.critical
        def test_a():
            assert True

        def test_b():
            assert True
    """,
    )
    result = pytester.runpytest(*hardpy_opts)
    result.assert_outcomes(passed=2)


def test_first_of_two_cases_critical_failed(pytester: Pytester, hardpy_opts: list):
    """First of two test cases is critical and failed - check timing."""
    pytester.makeconftest(
        f"""
        {import_header}

        def finish_executing():
            report = hardpy.get_current_report()

            module = report.modules["test_1"]
            assert module.stop_time >= module.start_time

            case_a = module.cases["test_a"]
            assert case_a.stop_time >= case_a.start_time

            case_b = module.cases["test_b"]
            assert case_b.stop_time is None
            assert case_b.start_time is None

        {conftest_actions_after}
    """,
    )
    pytester.makepyfile(
        test_1="""
        import pytest

        @pytest.mark.critical
        def test_a():
            assert False

        def test_b():
            assert True
    """,
    )
    result = pytester.runpytest(*hardpy_opts)
    result.assert_outcomes(failed=1, skipped=1)


def test_second_of_two_cases_critical_passed(pytester: Pytester, hardpy_opts: list):
    """Second of two test cases is critical and passed - check timing."""
    pytester.makeconftest(
        f"""
        {import_header}

        def finish_executing():
            report = hardpy.get_current_report()

            module = report.modules["test_1"]
            assert module.stop_time >= module.start_time

            case_a = module.cases["test_a"]
            assert case_a.stop_time >= case_a.start_time

            case_b = module.cases["test_b"]
            assert case_b.stop_time >= case_b.start_time

        {conftest_actions_after}
    """,
    )
    pytester.makepyfile(
        test_1="""
        import pytest

        def test_a():
            assert True

        @pytest.mark.critical
        def test_b():
            assert True
    """,
    )
    result = pytester.runpytest(*hardpy_opts)
    result.assert_outcomes(passed=2)


def test_second_of_two_cases_critical_failed(pytester: Pytester, hardpy_opts: list):
    """Second of two test cases is critical and failed - check timing."""
    pytester.makeconftest(
        f"""
        {import_header}

        def finish_executing():
            report = hardpy.get_current_report()

            module = report.modules["test_1"]
            assert module.stop_time >= module.start_time

            case_a = module.cases["test_a"]
            assert case_a.stop_time >= case_a.start_time

            case_b = module.cases["test_b"]
            assert case_b.stop_time >= case_b.start_time

        {conftest_actions_after}
    """,
    )
    pytester.makepyfile(
        test_1="""
        import pytest

        def test_a():
            assert True

        @pytest.mark.critical
        def test_b():
            assert False
    """,
    )
    result = pytester.runpytest(*hardpy_opts)
    result.assert_outcomes(passed=1, failed=1)


def test_second_of_three_cases_critical_passed(pytester: Pytester, hardpy_opts: list):
    """Second of three test cases is critical and passed - check timing."""
    pytester.makeconftest(
        f"""
        {import_header}

        def finish_executing():
            report = hardpy.get_current_report()

            module = report.modules["test_1"]
            assert module.stop_time >= module.start_time

            case_a = module.cases["test_a"]
            assert case_a.stop_time >= case_a.start_time

            case_b = module.cases["test_b"]
            assert case_b.stop_time >= case_b.start_time

            case_c = module.cases["test_c"]
            assert case_c.stop_time >= case_c.start_time

        {conftest_actions_after}
    """,
    )
    pytester.makepyfile(
        test_1="""
        import pytest

        def test_a():
            assert True

        @pytest.mark.critical
        def test_b():
            assert True

        def test_c():
            assert True
    """,
    )
    result = pytester.runpytest(*hardpy_opts)
    result.assert_outcomes(passed=3)


def test_second_of_three_cases_critical_failed(pytester: Pytester, hardpy_opts: list):
    """Second of three test cases is critical and failed - check timing."""
    pytester.makeconftest(
        f"""
        {import_header}

        def finish_executing():
            report = hardpy.get_current_report()

            module = report.modules["test_1"]
            assert module.stop_time >= module.start_time

            case_a = module.cases["test_a"]
            assert case_a.stop_time >= case_a.start_time

            case_b = module.cases["test_b"]
            assert case_b.stop_time >= case_b.start_time

            case_c = module.cases["test_c"]
            assert case_c.stop_time is None
            assert case_c.start_time is None

        {conftest_actions_after}
    """,
    )
    pytester.makepyfile(
        test_1="""
        import pytest

        def test_a():
            assert True

        @pytest.mark.critical
        def test_b():
            assert False

        def test_c():
            assert True
    """,
    )
    result = pytester.runpytest(*hardpy_opts)
    result.assert_outcomes(passed=1, failed=1, skipped=1)


def test_critical_module_with_skip(pytester: Pytester, hardpy_opts: list):
    """Critical module with skip - check timing."""
    pytester.makeconftest(
        f"""
        {import_header}

        def finish_executing():
            report = hardpy.get_current_report()

            module = report.modules["test_1"]
            assert module.stop_time >= module.start_time

            case = module.cases["test_a"]
            assert case.stop_time >= case.start_time

        {conftest_actions_after}
    """,
    )
    pytester.makepyfile(
        test_1="""
        import pytest

        pytestmark = pytest.mark.critical

        def test_a():
            pytest.skip()
    """,
    )
    pytester.makepyfile(
        test_2="""
        import pytest

        def test_b():
            assert True
    """,
    )
    result = pytester.runpytest(*hardpy_opts)
    result.assert_outcomes(skipped=2)


def test_first_of_two_modules_critical_passed(pytester: Pytester, hardpy_opts: list):
    """First of two modules is critical and passed - check timing."""
    pytester.makeconftest(
        f"""
        {import_header}

        def finish_executing():
            report = hardpy.get_current_report()

            module1 = report.modules["test_1"]
            assert module1.stop_time >= module1.start_time

            module2 = report.modules["test_2"]
            assert module2.stop_time >= module2.start_time

        {conftest_actions_after}
    """,
    )
    pytester.makepyfile(
        test_1="""
        import pytest

        pytestmark = pytest.mark.critical

        def test_a():
            assert True
    """,
    )
    pytester.makepyfile(
        test_2="""
        import pytest

        def test_b():
            assert True
    """,
    )
    result = pytester.runpytest(*hardpy_opts)
    result.assert_outcomes(passed=2)


def test_first_of_two_modules_critical_failed(pytester: Pytester, hardpy_opts: list):
    """First of two modules is critical and failed - check timing."""
    pytester.makeconftest(
        f"""
        {import_header}

        def finish_executing():
            report = hardpy.get_current_report()

            module1 = report.modules["test_1"]
            assert module1.stop_time >= module1.start_time

            module2 = report.modules["test_2"]
            assert module2.stop_time >= module2.start_time

        {conftest_actions_after}
    """,
    )
    pytester.makepyfile(
        test_1="""
        import pytest

        pytestmark = pytest.mark.critical

        def test_a():
            assert False
    """,
    )
    pytester.makepyfile(
        test_2="""
        import pytest

        def test_b():
            assert True
    """,
    )
    result = pytester.runpytest(*hardpy_opts)
    result.assert_outcomes(failed=1, skipped=1)


def test_second_of_two_modules_critical_passed(pytester: Pytester, hardpy_opts: list):
    """Second of two modules is critical and passed - check timing."""
    pytester.makeconftest(
        f"""
        {import_header}

        def finish_executing():
            report = hardpy.get_current_report()

            module1 = report.modules["test_1"]
            assert module1.stop_time >= module1.start_time

            module2 = report.modules["test_2"]
            assert module2.stop_time >= module2.start_time

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
    pytester.makepyfile(
        test_2="""
        import pytest

        pytestmark = pytest.mark.critical

        def test_b():
            assert True
    """,
    )
    result = pytester.runpytest(*hardpy_opts)
    result.assert_outcomes(passed=2)


def test_second_of_two_modules_critical_failed(pytester: Pytester, hardpy_opts: list):
    """Second of two modules is critical and failed - check timing."""
    pytester.makeconftest(
        f"""
        {import_header}

        def finish_executing():
            report = hardpy.get_current_report()

            module1 = report.modules["test_1"]
            assert module1.stop_time >= module1.start_time

            module2 = report.modules["test_2"]
            assert module2.stop_time >= module2.start_time

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
    pytester.makepyfile(
        test_2="""
        import pytest

        pytestmark = pytest.mark.critical

        def test_b():
            assert False
    """,
    )
    result = pytester.runpytest(*hardpy_opts)
    result.assert_outcomes(passed=1, failed=1)


def test_second_of_three_modules_critical_passed(pytester: Pytester, hardpy_opts: list):
    """Second of three modules is critical and passed - check timing."""
    pytester.makeconftest(
        f"""
        {import_header}

        def finish_executing():
            report = hardpy.get_current_report()

            module1 = report.modules["test_1"]
            assert module1.stop_time >= module1.start_time

            module2 = report.modules["test_2"]
            assert module2.stop_time >= module2.start_time

            module3 = report.modules["test_3"]
            assert module3.stop_time >= module3.start_time

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
    pytester.makepyfile(
        test_2="""
        import pytest

        pytestmark = pytest.mark.critical

        def test_b():
            assert True
    """,
    )
    pytester.makepyfile(
        test_3="""
        import pytest

        def test_c():
            assert True
    """,
    )
    result = pytester.runpytest(*hardpy_opts)
    result.assert_outcomes(passed=3)


def test_second_of_four_modules_critical_failed(pytester: Pytester, hardpy_opts: list):
    """Second of three modules is critical and failed - check timing."""
    pytester.makeconftest(
        f"""
        {import_header}

        def finish_executing():
            report = hardpy.get_current_report()

            module1 = report.modules["test_1"]
            assert module1.stop_time >= module1.start_time

            module2 = report.modules["test_2"]
            assert module2.stop_time >= module2.start_time

            module3 = report.modules["test_3"]
            assert module3.stop_time >= module3.start_time


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
    pytester.makepyfile(
        test_2="""
        import pytest

        pytestmark = pytest.mark.critical

        def test_b():
            assert False
    """,
    )
    pytester.makepyfile(
        test_3="""
        import pytest

        def test_c():
            assert True

        def test_d():
            assert True
    """,
    )
    result = pytester.runpytest(*hardpy_opts)
    result.assert_outcomes(passed=1, failed=1, skipped=2)
