# Copyright (c) 2026 Everypin
# GNU General Public License v3.0 (see LICENSE or https://www.gnu.org/licenses/gpl-3.0.txt)
"""Name of what a test run executes."""

from __future__ import annotations

from jig.pytest_jig.utils.const import RunScope


def resolve_run_name(requested: str | None, scope: RunScope) -> str:
    """Resolve the name describing what a run executes.

    The operator panel knows what the operator asked for, a section path or a
    module path, and requests that name. A run started without a requested name,
    from the command line, is described by its scope.

    Args:
        requested (str | None): name requested by the caller, if any
        scope (RunScope): scope of the pytest invocation

    Returns:
        str: name of what the run executes
    """
    return requested or scope.value
