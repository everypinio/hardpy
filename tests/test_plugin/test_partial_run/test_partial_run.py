from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from pytest import Pytester

module_a = """
    def test_a():
        assert True
"""


def test_kept_state_of_the_modules_left_out(
    pytester: Pytester,
    jig_opts: list[str],
    jig_opts_repeat: list[str],
):
    pytester.makepyfile(
        test_module_a=module_a,
        test_module_b="""
        def test_b():
            assert True
    """,
    )
    result = pytester.runpytest(*jig_opts)
    result.assert_outcomes(passed=2)

    pytester.makepyfile(
        test_module_b="""
        from jig import get_current_report
        from jig.pytest_jig.reporter import RunnerReporter
        from jig.pytest_jig.utils.const import TestStatus as Status

        def test_b():
            state = RunnerReporter().get_field("modules")
            assert (
                state["test_module_a"]["cases"]["test_a"]["status"]
                == Status.PASSED
            ), "The module left out of the partial run lost its result."

            report = get_current_report()
            assert list(report.modules) == ["test_module_b"], (
                "The partial run report must only cover the tests it runs."
            )
    """,
    )
    result = pytester.runpytest(
        *jig_opts_repeat,
        "--jig-partial-run",
        "test_module_b.py",
    )
    result.assert_outcomes(passed=1)


def test_kept_state_of_the_modules_left_out_of_a_failing_run(
    pytester: Pytester,
    jig_opts: list[str],
    jig_opts_repeat: list[str],
):
    pytester.makepyfile(
        test_module_a=module_a,
        test_module_b="""
        def test_b():
            assert True
    """,
    )
    result = pytester.runpytest(*jig_opts)
    result.assert_outcomes(passed=2)

    pytester.makepyfile(
        test_module_b="""
        def test_b():
            assert False
    """,
    )
    result = pytester.runpytest(
        *jig_opts_repeat,
        "--jig-partial-run",
        "test_module_b.py",
    )
    result.assert_outcomes(failed=1)

    pytester.makepyfile(
        test_module_c="""
        from jig.pytest_jig.reporter import RunnerReporter
        from jig.pytest_jig.utils.const import TestStatus as Status

        def test_c():
            state = RunnerReporter().get_field("modules")
            assert (
                state["test_module_a"]["cases"]["test_a"]["status"]
                == Status.PASSED
            ), "The module left out of the partial run lost its result."
            assert (
                state["test_module_b"]["cases"]["test_b"]["status"]
                == Status.FAILED
            ), "The failed module of the previous partial run lost its result."
    """,
    )
    result = pytester.runpytest(
        *jig_opts_repeat,
        "--jig-partial-run",
        "test_module_c.py",
    )
    result.assert_outcomes(passed=1)
