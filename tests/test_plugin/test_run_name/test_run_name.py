from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from pytest import Pytester

read_run_name = """
    from jig import get_current_report
    from jig.pytest_jig.reporter import RunnerReporter

    def test_a():
        assert RunnerReporter().get_field("run_name") == "{expected}"
        assert get_current_report() is not None, (
            "The run name must stay out of the report document."
        )
"""


def test_full_run_is_named_after_its_scope(
    pytester: Pytester,
    jig_opts: list[str],
):
    pytester.makepyfile(test_module_a=read_run_name.format(expected="full"))

    result = pytester.runpytest(*jig_opts)

    result.assert_outcomes(passed=1)


def test_partial_run_without_a_name_is_named_after_its_scope(
    pytester: Pytester,
    jig_opts: list[str],
):
    pytester.makepyfile(test_module_a=read_run_name.format(expected="partial"))

    result = pytester.runpytest(
        *jig_opts,
        "--jig-partial-run",
        "test_module_a.py",
    )

    result.assert_outcomes(passed=1)


def test_run_keeps_the_name_of_what_the_operator_started(
    pytester: Pytester,
    jig_opts: list[str],
):
    pytester.makepyfile(test_module_a=read_run_name.format(expected="prompts"))

    result = pytester.runpytest(
        *jig_opts,
        "--jig-partial-run",
        "--jig-run-name",
        "prompts",
        "test_module_a.py",
    )

    result.assert_outcomes(passed=1)


def test_run_name_of_a_new_run_replaces_the_previous_one(
    pytester: Pytester,
    jig_opts: list[str],
    jig_opts_repeat: list[str],
):
    pytester.makepyfile(test_module_a=read_run_name.format(expected="prompts"))
    result = pytester.runpytest(
        *jig_opts,
        "--jig-partial-run",
        "--jig-run-name",
        "prompts",
        "test_module_a.py",
    )
    result.assert_outcomes(passed=1)

    pytester.makepyfile(test_module_a=read_run_name.format(expected="full"))

    result = pytester.runpytest(*jig_opts_repeat)

    result.assert_outcomes(passed=1)
