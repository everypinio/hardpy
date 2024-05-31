# Copyright (c) 2024 Everypin
# GNU General Public License v3.0 (see LICENSE or https://www.gnu.org/licenses/gpl-3.0.txt)

import re
from logging import getLogger
from pathlib import Path
from typing import NamedTuple

from pytest import Item, Mark


class TestDependencyInfo(NamedTuple):
    """Test info."""

    module_id: str
    case_id: str


class NodeInfo(object):
    """Test node info."""

    def __init__(self, item: Item):
        self._item = item
        self._log = getLogger(__name__)

        self._case_name = self._get_human_name(
            item.own_markers,
            "case_name",
        )
        self._module_name = self._get_human_name(
            item.parent.own_markers,
            "module_name",
        )
        self._case_dependency = self._get_human_name(
            item.own_markers,
            "case_dependency",
        )

        self._module_dependency = self._get_human_name(
            item.parent.own_markers,
            "module_dependency",
        )

        self._case_dependency_info = self._get_dependency_info(
            item.own_markers, "case_dependency"
        )
        self._module_dependency_info = self._get_dependency_info(
            item.parent.own_markers, "module_dependency"
        )

        self._module_id = Path(item.parent.nodeid).stem
        self._case_id = item.name

    @property
    def module_id(self):
        """Get module id.

        Returns:
            str: module id
        """
        return self._module_id

    @property
    def case_id(self):
        """Get case id.

        Returns:
            str: case id
        """
        return self._case_id

    @property
    def module_name(self):
        """Get module name.

        Returns:
            str: module name
        """
        return self._module_name

    @property
    def case_name(self):
        """Get case name.

        Returns:
            str: case name
        """
        return self._case_name

    @property
    def case_dependency(self):
        """Get case dependency info.

        Returns:
            TestDependencyInfo | str: Parsed dependency information.
        """
        return self._case_dependency_info

    @property
    def module_dependency(self):
        """Get module dependency info.

        Returns:
            TestDependencyInfo | str: Parsed dependency information.
        """
        return self._module_dependency_info

    def _get_human_name(self, markers: list[Mark], marker_name: str) -> str:
        """Get human name from markers.

        Args:
            markers (list[Mark]): item markers list
            marker_name (str): marker name

        Returns:
            str: human name by user
        """
        for marker in markers:
            if marker.name == marker_name:
                if marker.args:
                    return marker.args[0]

        return ""

    def _get_dependency_info(
        self, markers: list[Mark], marker_name: str
    ) -> TestDependencyInfo | str:
        """Extract and parse dependency information.

        Args:
            markers (list[Mark]): item markers list
            marker_name (str): marker name

        Returns:
            TestDependencyInfo | str | None: Parsed dependency information.
        """
        dependency_value = self._get_human_name(markers, marker_name)
        data = re.search(r"(\w+)::(\w+)", dependency_value)
        if data:
            dependency_module_id, dependency_case_id = data.groups()
            return TestDependencyInfo(
                module_id=dependency_module_id, case_id=dependency_case_id
            )
        elif re.search(r"^\w+$", dependency_value):
            return dependency_value
        return dependency_value
