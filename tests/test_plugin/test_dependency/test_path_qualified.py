from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from pytest import Pytester


def test_path_qualified_dependency_passed(pytester: Pytester, jig_opts: list):
    first = pytester.path / "autofocus"
    first.mkdir()
    (first / "test_1.py").write_text(
        """
def test_peak():
    assert True
""",
        encoding="utf-8",
    )
    (pytester.path / "test_2.py").write_text(
        """
import pytest

@pytest.mark.dependency("autofocus/test_1::test_peak")
def test_follow_up():
    assert True
""",
        encoding="utf-8",
    )
    result = pytester.runpytest(*jig_opts)
    result.assert_outcomes(passed=2)


def test_path_qualified_dependency_failed(pytester: Pytester, jig_opts: list):
    first = pytester.path / "autofocus"
    first.mkdir()
    (first / "test_1.py").write_text(
        """
def test_peak():
    assert False
""",
        encoding="utf-8",
    )
    (pytester.path / "test_2.py").write_text(
        """
import pytest

@pytest.mark.dependency("autofocus/test_1::test_peak")
def test_follow_up():
    assert True
""",
        encoding="utf-8",
    )
    result = pytester.runpytest(*jig_opts)
    result.assert_outcomes(failed=1, skipped=1)
