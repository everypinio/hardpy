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


def test_critical_case_with_dependency_passed(pytester: Pytester, hardpy_opts: list):
    """Critical test with dependency that passed."""
    pytester.makepyfile(
        test_1="""
        import pytest

        def test_a():
            assert True

        @pytest.mark.critical
        @pytest.mark.dependency("test_1::test_a")
        def test_b():
            assert True
    """,
    )
    result = pytester.runpytest(*hardpy_opts)
    result.assert_outcomes(passed=2)


def test_critical_case_with_dependency_failed(pytester: Pytester, hardpy_opts: list):
    """Critical test with dependency that failed."""
    pytester.makepyfile(
        test_1="""
        import pytest

        def test_a():
            assert False

        @pytest.mark.critical
        @pytest.mark.dependency("test_1::test_a")
        def test_b():
            assert True
    """,
    )
    result = pytester.runpytest(*hardpy_opts)
    result.assert_outcomes(failed=1, skipped=1)


def test_critical_case_with_skipped_dependency(pytester: Pytester, hardpy_opts: list):
    """Critical test with dependency that was skipped."""
    pytester.makepyfile(
        test_1="""
        import pytest

        def test_a():
            pytest.skip()

        @pytest.mark.critical
        @pytest.mark.dependency("test_1::test_a")
        def test_b():
            assert True
    """,
    )
    result = pytester.runpytest(*hardpy_opts)
    result.assert_outcomes(skipped=2)


def test_first_case_critical_failed(pytester: Pytester, hardpy_opts: list):
    """First test case is critical and failed - check timing."""
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


def test_middle_case_critical_failed(pytester: Pytester, hardpy_opts: list):
    """Middle test case is critical and failed - check timing."""
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


def test_last_case_critical_failed(pytester: Pytester, hardpy_opts: list):
    """Last test case is critical and failed - check timing."""
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


def test_critical_module_with_dependency_passed(pytester: Pytester, hardpy_opts: list):
    """Critical module with dependency that passed."""
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

        pytestmark = [
            pytest.mark.critical,
            pytest.mark.dependency("test_1"),
        ]

        def test_b():
            assert True
    """,
    )
    result = pytester.runpytest(*hardpy_opts)
    result.assert_outcomes(passed=2)


def test_critical_module_with_dependency_failed(pytester: Pytester, hardpy_opts: list):
    """Critical module with dependency that failed."""
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

        pytestmark = [
            pytest.mark.critical,
            pytest.mark.dependency("test_1"),
        ]

        def test_b():
            assert True
    """,
    )
    result = pytester.runpytest(*hardpy_opts)
    result.assert_outcomes(failed=1, skipped=1)


def test_first_module_critical_failed(pytester: Pytester, hardpy_opts: list):
    """First module is critical and failed - check timing."""
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


def test_middle_module_critical_failed(pytester: Pytester, hardpy_opts: list):
    """Middle module is critical and failed - check timing."""
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
    """,
    )
    result = pytester.runpytest(*hardpy_opts)
    result.assert_outcomes(passed=1, failed=1, skipped=1)


def test_last_module_critical_failed(pytester: Pytester, hardpy_opts: list):
    """Last module is critical and failed - check timing."""
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
    result = pytester.runpytest(*hardpy_opts)
    result.assert_outcomes(skipped=1)
