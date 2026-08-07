from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from pytest import Pytester

func_test_header = """
        import pytest

        import jig
        from jig.pytest_jig.utils import NodeInfo
        """


def test_fill_error_code(pytester: Pytester, jig_opts: list[str]):
    pytester.makepyfile(
        f"""
        {func_test_header}
        def test_fill_error_code():
            report = jig.get_current_report()
            error_code = report.error_code
            assert error_code == None, "The error_code is not empty."

            assert False, jig.ErrorCode(1, "a")

        def test_error_code_exist(request):
            report = jig.get_current_report()
            error_code = report.error_code
            assert error_code == 1, "The error_code must be 1."

            node = NodeInfo(request.node)
            module_id = node.module_id

            case_id = "test_fill_error_code"
            assertion_msg_1 = report.modules[module_id].cases[case_id].assertion_msg
            assert "AssertionError: a" in assertion_msg_1
    """,
    )
    result = pytester.runpytest(*jig_opts)
    result.assert_outcomes(passed=1, failed=1)


def test_duplicate_error_code(pytester: Pytester, jig_opts: list[str]):
    pytester.makepyfile(
        f"""
        {func_test_header}
        def test_error_code(request):
            assert False, jig.ErrorCode(1)

        def test_duplicate_error_code():
            assert False, jig.ErrorCode(2)

        def test_check_error_code():
            report = jig.get_current_report()
            error_code = report.error_code
            assert error_code == 1, "The error_code must be 1."
    """,
    )
    result = pytester.runpytest(*jig_opts)
    result.assert_outcomes(passed=1, failed=2)


def test_negative_error_code(pytester: Pytester, jig_opts: list[str]):
    pytester.makepyfile(
        f"""
        {func_test_header}
        def test_negative_error_code():
            with pytest.raises(ValueError):
                jig.ErrorCode(-1)
    """,
    )
    result = pytester.runpytest(*jig_opts)
    result.assert_outcomes(passed=1)
