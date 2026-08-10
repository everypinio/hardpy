# Copyright (c) 2024 Everypin
# GNU General Public License v3.0 (see LICENSE or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import annotations

import re
from logging import getLogger
from pathlib import PurePosixPath
from typing import TYPE_CHECKING, NamedTuple

from jig.pytest_jig.utils.const import Group

if TYPE_CHECKING:
    from pytest import Item, Mark


def module_id_from_nodeid(nodeid: str) -> str:
    """Derive the module id from a pytest nodeid.

    The module id is the module path relative to the tests root, without the
    ``.py`` suffix. Forward slashes are preserved so modules in different
    directories keep distinct identities.

    Args:
        nodeid (str): pytest nodeid (module path, optionally followed by ``::``)

    Returns:
        str: module id

    Raises:
        ValueError: if a directory or file segment contains a ``.`` other than
            the ``.py`` suffix (dots collide with nested database key paths)
    """
    module_path = nodeid.partition("::")[0].removesuffix(".py")
    if not module_path:
        msg = f"Unable to derive module id from nodeid: {nodeid}"
        raise ValueError(msg)
    for part in PurePosixPath(module_path).parts:
        if "." in part:
            msg = (
                f"Module path '{module_path}' contains a '.' which is not "
                "allowed in directory or module names (conflicts with "
                "database key paths)."
            )
            raise ValueError(msg)
    return module_path


class TestDependencyInfo(NamedTuple):
    """Test info."""

    def __repr__(self) -> str:
        return f"Dependency: {self.module_id}::{self.case_id}"

    module_id: str
    case_id: str | None


class NodeInfo:
    """Test node info."""

    def __init__(self, item: Item) -> None:
        self._item = item
        self._log = getLogger(__name__)

        self._case_name = self._get_human_name(
            item.own_markers,
            "case_name",
        )
        self._module_name = self._get_human_name(
            item.parent.own_markers,  # type: ignore
            "module_name",
        )

        self._dependency = self._get_dependency_info(
            item.own_markers + item.parent.own_markers,  # type: ignore
        )

        self._attempt = self._get_attempt(item.own_markers)

        self._critical = self._get_critical(item.own_markers + item.parent.own_markers)

        self._module_group = self._get_group(item.parent.own_markers, "module_group")
        self._case_group = self._get_group(item.own_markers, "case_group")

        self._module_id = module_id_from_nodeid(item.parent.nodeid)  # type: ignore
        self._case_id = item.name
        self._section = self._get_section(item)

    @property
    def module_id(self) -> str:
        """Get module id.

        Returns:
            str: module id
        """
        return self._module_id

    @property
    def case_id(self) -> str:
        """Get case id.

        Returns:
            str: case id
        """
        return self._case_id

    @property
    def module_name(self) -> str:
        """Get module name.

        Returns:
            str: module name
        """
        return self._module_name

    @property
    def case_name(self) -> str:
        """Get case name.

        Returns:
            str: case name
        """
        return self._case_name

    @property
    def dependency(self) -> list[TestDependencyInfo] | None:
        """Get dependency information.

        Returns:
            list[TestDependencyInfo] | None: Dependency information
        """
        return self._dependency

    @property
    def attempt(self) -> int:
        """Get attempt.

        Returns:
            int: attempt number
        """
        return self._attempt

    @property
    def critical(self) -> bool:
        """Get critical status.

        Returns:
            bool: critical status
        """
        return self._critical

    @property
    def module_group(self) -> Group:
        """Get module group.

        Returns:
            Group: module group
        """
        return self._module_group

    @property
    def case_group(self) -> Group:
        """Get case group.

        Returns:
            Group: case group
        """
        return self._case_group

    @property
    def section(self) -> list[str]:
        """Get module section path.

        Returns:
            list[str]: ordered section names; empty when the module is at the
            tests root and no ``module_section`` marker is set
        """
        return self._section

    def _get_human_name(self, markers: list[Mark], marker_name: str) -> str:
        """Get human name from markers.

        Args:
            markers (list[Mark]): item markers list
            marker_name (str): marker name

        Returns:
            str: human name by user
        """
        for marker in markers:
            if marker.name == marker_name and marker.args:
                return marker.args[0]
        return ""

    def _get_human_names(self, markers: list[Mark], marker_name: str) -> list[str]:
        """Get human names from markers.

        Args:
            markers (list[Mark]): item markers list
            marker_name (str): marker name

        Returns:
            list[str]: human names by user
        """
        names = []
        for marker in markers:
            if marker.name == marker_name and marker.args:
                names.append(marker.args[0])  # noqa: PERF401
        return names

    def _get_dependency_info(
        self,
        markers: list[Mark],
    ) -> list[TestDependencyInfo] | None:
        """Extract and parse dependency information.

        Args:
            markers (list[Mark]): item markers list
            marker_name (str): marker name

        Returns:
            list[TestDependencyInfo] | None: Dependency information
        """
        dependency_value = self._get_human_names(markers, "dependency")
        dependencies = []
        for dependency in dependency_value:
            dependency_data = re.search(r"([\w./-]+)::(\w+)", dependency)
            if dependency_data:
                dependencies.append(TestDependencyInfo(*dependency_data.groups()))
            elif re.search(r"^[\w./-]+$", dependency):
                dependencies.append(TestDependencyInfo(dependency, None))
            elif not dependency:
                continue
            else:
                error_msg = f"Invalid dependency format: {dependency}"
                raise ValueError(error_msg)
        return dependencies if dependencies else None

    def _get_attempt(self, markers: list[Mark]) -> int:
        """Get the number of attempts.

        Args:
            markers (list[Mark]): item markers list

        Returns:
            int: number of attempts
        """
        attempt: int = 1
        for marker in markers:
            if marker.name == "attempt" and marker.args:
                attempt = marker.args[0]
        if not isinstance(attempt, int) or attempt < 1:
            msg = "The 'attempt' marker value must be a positive integer."
            raise ValueError(msg)
        return attempt

    def _get_critical(self, markers: list[Mark]) -> bool:
        """Check if test or module is marked as critical.

        Args:
            markers (list[Mark]): item markers list

        Returns:
            bool: True if test or module is critical, False otherwise
        """
        return any(marker.name == "critical" for marker in markers)

    def _get_group(
        self,
        markers: list[Mark],
        marker_name: str,
    ) -> Group:
        """Get group from markers or use default.

        Args:
            markers (list[Mark]): item markers list
            marker_name (str): marker name
        Returns:
            Group: group from marker or default (Group.MAIN)
        """
        for marker in markers:
            if marker.name == marker_name and marker.args:
                arg = marker.args[0]

                if isinstance(arg, Group):
                    return arg
                if isinstance(arg, str):
                    valid_groups = {group.value for group in Group}
                    if arg not in valid_groups:
                        msg = f"Invalid group '{arg}'. Valid groups are: {', '.join(valid_groups)}"  # noqa: E501
                        raise ValueError(msg)
                    return Group(arg)
                msg = f"Group marker argument must be either string or Group enum, got {type(arg)}"  # noqa: E501
                raise ValueError(msg)

        return Group.MAIN

    def _get_section(self, item: Item) -> list[str]:
        """Resolve the module section path.

        Precedence: ``module_section`` marker on the module wins; otherwise the
        directory path of the module relative to the tests root.

        Args:
            item (Item): pytest test item

        Returns:
            list[str]: ordered section names

        Raises:
            ValueError: if the marker arguments are empty or not strings
        """
        parent_markers = item.parent.own_markers if item.parent is not None else []
        for marker in parent_markers:
            if marker.name != "module_section":
                continue
            return self._parse_section_marker_args(marker.args)

        if item.parent is None:
            return []
        module_path = PurePosixPath(module_id_from_nodeid(item.parent.nodeid))
        return list(module_path.parts[:-1])

    def _parse_section_marker_args(self, args: tuple) -> list[str]:
        """Parse ``module_section`` marker arguments into a section path.

        Accepts either varargs (``"Autofocus", "Fine"``) or a single
        slash-separated string (``"Autofocus/Fine"``).

        Args:
            args (tuple): marker arguments

        Returns:
            list[str]: ordered section names

        Raises:
            ValueError: if args are empty or contain a non-string / empty part
        """
        if not args:
            msg = "module_section marker requires at least one argument"
            raise ValueError(msg)

        if len(args) == 1 and isinstance(args[0], str) and "/" in args[0]:
            parts = [part for part in args[0].split("/") if part != ""]
        else:
            parts = list(args)

        if not parts:
            msg = "module_section marker produced an empty section path"
            raise ValueError(msg)

        for part in parts:
            if not isinstance(part, str):
                msg = (
                    "module_section marker arguments must be strings, "
                    f"got {type(part)}"
                )
                raise ValueError(msg)
            if not part:
                msg = "module_section marker arguments must not be empty"
                raise ValueError(msg)
            if "." in part:
                msg = (
                    f"module_section part '{part}' must not contain '.' "
                    "(conflicts with database key paths)"
                )
                raise ValueError(msg)
        return parts
