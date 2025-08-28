from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from pytest import Pytester


def test_enum_groups(pytester: Pytester, hardpy_opts: list[str]):
    pytester.makepyfile(
        """
        import pytest
        from hardpy import get_current_report
        from hardpy.pytest_hardpy.utils import NodeInfo
        from hardpy.pytest_hardpy.utils.const import Group

        pytestmark = pytest.mark.module_group(Group.SETUP)

        @pytest.mark.case_group(Group.TEARDOWN)
        def test_case(request):
            node = NodeInfo(request.node)
            report = get_current_report()

            module_group = report.modules[node.module_id].group
            assert module_group == Group.SETUP.value

            case_group = report.modules[node.module_id].cases[node.case_id].group
            assert case_group == Group.TEARDOWN.value
        """,
    )
    result = pytester.runpytest(*hardpy_opts)
    result.assert_outcomes(passed=1)


def test_string_groups(pytester: Pytester, hardpy_opts: list[str]):
    pytester.makepyfile(
        """
        import pytest
        from hardpy import get_current_report
        from hardpy.pytest_hardpy.utils import NodeInfo

        pytestmark = pytest.mark.module_group("setup")

        @pytest.mark.case_group("teardown")
        def test_case(request):
            node = NodeInfo(request.node)
            report = get_current_report()

            module_group = report.modules[node.module_id].group
            assert module_group == "setup"

            case_group = report.modules[node.module_id].cases[node.case_id].group
            assert case_group == "teardown"
        """,
    )
    result = pytester.runpytest(*hardpy_opts)
    result.assert_outcomes(passed=1)


def test_default_groups(pytester: Pytester, hardpy_opts: list[str]):
    pytester.makepyfile(
        """
        import pytest
        from hardpy import get_current_report
        from hardpy.pytest_hardpy.utils import NodeInfo
        from hardpy.pytest_hardpy.utils.const import Group

        def test_case(request):
            node = NodeInfo(request.node)
            report = get_current_report()

            module_group = report.modules[node.module_id].group
            assert module_group == Group.MAIN.value

            case_group = report.modules[node.module_id].cases[node.case_id].group
            assert case_group == Group.MAIN.value
        """,
    )
    result = pytester.runpytest(*hardpy_opts)
    result.assert_outcomes(passed=1)


def test_invalid_groups(pytester: Pytester, hardpy_opts: list[str]):
    pytester.makepyfile(
        """
        import pytest

        pytestmark = pytest.mark.module_group("invalid_group")

        @pytest.mark.case_group("wrong_group")
        def test_case(request):
            pass
        """,
    )
    result = pytester.runpytest(*hardpy_opts)
    output = result.stdout.str()
    assert "invalid_group" in output
    assert "Invalid group" in output or "Error creating NodeInfo" in output
    assert result.ret != 0


def test_empty_groups(pytester: Pytester, hardpy_opts: list[str]):
    pytester.makepyfile(
        """
        import pytest

        pytestmark = pytest.mark.module_group("")

        @pytest.mark.case_group("")
        def test_case(request):
            pass
        """,
    )
    result = pytester.runpytest(*hardpy_opts)
    output = result.stdout.str()
    assert "empty" in output or "''" in output
    assert "Invalid group" in output or "Error creating NodeInfo" in output
    assert result.ret != 0
