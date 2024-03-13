# Copyright (c) 2024 Everypin
# GNU General Public License v3.0 (see LICENSE or https://www.gnu.org/licenses/gpl-3.0.txt)

from logging import getLogger
from typing import Any

from hardpy.pytest_hardpy.reporter.base import BaseReporter
from hardpy.pytest_hardpy.utils import Singleton


class RunnerReporter(Singleton, BaseReporter):
    """Reporter for using in direct call from test runner with HardPy plugin."""

    def __init__(self):
        if not self._initialized:
            super().__init__()
            self._log = getLogger(__name__)
            self._initialized = True

    def get_field(self, key: str) -> Any:
        """Get field from the statestore.

        Args:
            key (str): field name

        Returns:
            Any: field value
        """
        return self._statestore.get_field(key)
