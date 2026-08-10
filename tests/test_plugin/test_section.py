from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from pytest import Pytester


def test_directory_section(pytester: Pytester, jig_opts: list[str]):
    section_dir = pytester.path / "autofocus"
    section_dir.mkdir()
    (section_dir / "test_1.py").write_text(
        """
import pytest
from jig import get_current_report
from jig.pytest_jig.utils import NodeInfo

def test_case(request):
    node = NodeInfo(request.node)
    report = get_current_report()
    assert node.module_id == "autofocus/test_1"
    assert node.section == ["autofocus"]
    assert report.modules[node.module_id].section == ["autofocus"]
""",
        encoding="utf-8",
    )
    result = pytester.runpytest(*jig_opts)
    result.assert_outcomes(passed=1)


def test_nested_directory_section(pytester: Pytester, jig_opts: list[str]):
    nested = pytester.path / "autofocus" / "fine"
    nested.mkdir(parents=True)
    (nested / "test_1.py").write_text(
        """
from jig import get_current_report
from jig.pytest_jig.utils import NodeInfo

def test_case(request):
    node = NodeInfo(request.node)
    report = get_current_report()
    assert node.module_id == "autofocus/fine/test_1"
    assert node.section == ["autofocus", "fine"]
    assert report.modules[node.module_id].section == ["autofocus", "fine"]
""",
        encoding="utf-8",
    )
    result = pytester.runpytest(*jig_opts)
    result.assert_outcomes(passed=1)


def test_module_section_marker_override(pytester: Pytester, jig_opts: list[str]):
    pytester.makepyfile(
        """
        import pytest
        from jig import get_current_report
        from jig.pytest_jig.utils import NodeInfo

        pytestmark = pytest.mark.module_section("Alignment")

        def test_case(request):
            node = NodeInfo(request.node)
            report = get_current_report()
            assert node.section == ["Alignment"]
            assert report.modules[node.module_id].section == ["Alignment"]
        """,
    )
    result = pytester.runpytest(*jig_opts)
    result.assert_outcomes(passed=1)


def test_module_section_marker_nested_args(pytester: Pytester, jig_opts: list[str]):
    pytester.makepyfile(
        """
        import pytest
        from jig import get_current_report
        from jig.pytest_jig.utils import NodeInfo

        pytestmark = pytest.mark.module_section("Autofocus", "Fine")

        def test_case(request):
            node = NodeInfo(request.node)
            report = get_current_report()
            assert node.section == ["Autofocus", "Fine"]
            assert report.modules[node.module_id].section == ["Autofocus", "Fine"]
        """,
    )
    result = pytester.runpytest(*jig_opts)
    result.assert_outcomes(passed=1)


def test_module_section_marker_slash_string(pytester: Pytester, jig_opts: list[str]):
    pytester.makepyfile(
        """
        import pytest
        from jig import get_current_report
        from jig.pytest_jig.utils import NodeInfo

        pytestmark = pytest.mark.module_section("Autofocus/Fine")

        def test_case(request):
            node = NodeInfo(request.node)
            report = get_current_report()
            assert node.section == ["Autofocus", "Fine"]
            assert report.modules[node.module_id].section == ["Autofocus", "Fine"]
        """,
    )
    result = pytester.runpytest(*jig_opts)
    result.assert_outcomes(passed=1)


def test_root_modules_have_empty_section(pytester: Pytester, jig_opts: list[str]):
    pytester.makepyfile(
        """
        from jig import get_current_report
        from jig.pytest_jig.utils import NodeInfo

        def test_case(request):
            node = NodeInfo(request.node)
            report = get_current_report()
            assert node.section == []
            assert report.modules[node.module_id].section == []
        """,
    )
    result = pytester.runpytest(*jig_opts)
    result.assert_outcomes(passed=1)


def test_invalid_module_section_marker(pytester: Pytester, jig_opts: list[str]):
    pytester.makepyfile(
        """
        import pytest

        pytestmark = pytest.mark.module_section("")

        def test_case():
            pass
        """,
    )
    result = pytester.runpytest(*jig_opts)
    output = result.stdout.str()
    assert "module_section" in output or "Error creating NodeInfo" in output
    assert result.ret != 0


def test_same_basename_modules_do_not_collide(
    pytester: Pytester,
    jig_opts: list[str],
):
    first = pytester.path / "autofocus"
    second = pytester.path / "alignment"
    first.mkdir()
    second.mkdir()
    (first / "test_1.py").write_text(
        """
def test_case():
    assert True
""",
        encoding="utf-8",
    )
    (second / "test_1.py").write_text(
        """
from jig import get_current_report

def test_case():
    report = get_current_report()
    assert "autofocus/test_1" in report.modules
    assert "alignment/test_1" in report.modules
    assert report.modules["autofocus/test_1"].section == ["autofocus"]
    assert report.modules["alignment/test_1"].section == ["alignment"]
""",
        encoding="utf-8",
    )
    result = pytester.runpytest("--import-mode=importlib", *jig_opts)
    result.assert_outcomes(passed=2)
