# Copyright (c) 2024 Everypin
# GNU General Public License v3.0 (see LICENSE or https://www.gnu.org/licenses/gpl-3.0.txt)

import re
from logging import getLogger
from pathlib import Path

from pytest import Item, Mark


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
        self._module_id = Path(item.parent.nodeid).stem
        self._case_id = item.name

    @property
    def module_id(self):
        return self._module_id

    @property
    def case_id(self):
        return self._case_id

    @property
    def module_name(self):
        return self._module_name

    @property
    def case_name(self):
        return self._case_name

    @property
    def case_dependency(self):
        try:
            data = re.search(r"(\w+)::(.+)", self._case_dependency)
            if data:
                dependency_module_id, dependency_case_id = data.groups()
                return dependency_module_id, dependency_case_id
        except AttributeError:
            self._log.error("Incorrect dependency!")

    @property
    def module_dependency(self):
        try:
            data = re.search(r"(\w+)::(.+)", self._module_dependency)
            if data:
                module_id, case_id = data.groups()
                return module_id, case_id
        except AttributeError:
            self._log.error("Incorrect dependency!")

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
