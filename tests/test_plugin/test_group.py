from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from pytest import Pytester

group_test_header = """
    import pytest

    from hardpy import get_current_report
    from hardpy.pytest_hardpy.utils import NodeInfo
    from hardpy.pytest_hardpy.utils.const import Group

    module_group = Group.SETUP
    case_group = Group.TEARDOWN
    pytestmark = pytest.mark.module_group(module_group)
    """

test_default_header = """
    import pytest

    from hardpy import get_current_report
    from hardpy.pytest_hardpy.utils import NodeInfo
    from hardpy.pytest_hardpy.utils.const import Group
    """

group_test_header_with_string = """
    import pytest

    from hardpy import get_current_report
    from hardpy.pytest_hardpy.utils import NodeInfo

    module_group = "setup"
    case_group = "teardown"
    pytestmark = pytest.mark.module_group(module_group)
    """

group_test_header_with_incorrect_data = """
    import pytest

    from hardpy import get_current_report
    from hardpy.pytest_hardpy.utils import NodeInfo

    module_group = "invalid_group"
    case_group = "wrong_group"
    pytestmark = pytest.mark.module_group(module_group)
    """


def test_module_group(pytester: Pytester, hardpy_opts: list[str]):
    pytester.makepyfile(
        f"""
        {group_test_header}
        @pytest.mark.case_group(case_group)
        def test_written_module_group(request):
            node = NodeInfo(request.node)
            report = get_current_report()
            read_module_group = report.modules[node.module_id].group
            assert module_group.value == read_module_group
    """,
    )
    result = pytester.runpytest(*hardpy_opts)
    result.assert_outcomes(passed=1)


def test_case_group(pytester: Pytester, hardpy_opts: list[str]):
    pytester.makepyfile(
        f"""
        {group_test_header}
        @pytest.mark.case_group(case_group)
        def test_written_case_group(request):
            node = NodeInfo(request.node)
            report = get_current_report()
            group = report.modules[node.module_id].cases[node.case_id].group
            assert case_group.value == group
    """,
    )
    result = pytester.runpytest(*hardpy_opts)
    result.assert_outcomes(passed=1)


def test_group_with_string_values(pytester: Pytester, hardpy_opts: list[str]):
    pytester.makepyfile(
        f"""
        {group_test_header_with_string}
        @pytest.mark.case_group(case_group)
        def test_group_with_string_values(request):
            node = NodeInfo(request.node)
            report = get_current_report()
            module_group_value = report.modules[node.module_id].group
            case_group_value = report.modules[node.module_id].cases[node.case_id].group
            assert module_group == module_group_value
            assert case_group == case_group_value
    """,
    )
    result = pytester.runpytest(*hardpy_opts)
    result.assert_outcomes(passed=1)


def test_default_case_group(pytester: Pytester, hardpy_opts: list[str]):
    pytester.makepyfile(
        f"""
        {test_default_header}
        def test_check_default_case_group(request):
            node = NodeInfo(request.node)
            report = get_current_report()
            group = report.modules[node.module_id].cases[node.case_id].group
            assert group == Group.MAIN.value
    """,
    )
    result = pytester.runpytest(*hardpy_opts)
    result.assert_outcomes(passed=1)


def test_default_module_group(pytester: Pytester, hardpy_opts: list[str]):
    pytester.makepyfile(
        f"""
        {test_default_header}
        def test_check_default_module_group(request):
            node = NodeInfo(request.node)
            report = get_current_report()
            read_module_group = report.modules[node.module_id].group
            assert read_module_group == Group.MAIN.value
    """,
    )
    result = pytester.runpytest(*hardpy_opts)
    result.assert_outcomes(passed=1)


def test_incorrect_group_markers(pytester: Pytester, hardpy_opts: list[str]):
    pytester.makepyfile(
        f"""
        {group_test_header_with_incorrect_data}
        @pytest.mark.case_group(case_group)
        def test_incorrect_group_markers(request):
            node = NodeInfo(request.node)
    """,
    )
    result = pytester.runpytest(*hardpy_opts)
    # Should fail because of invalid group values
    result.assert_outcomes(failed=1)
