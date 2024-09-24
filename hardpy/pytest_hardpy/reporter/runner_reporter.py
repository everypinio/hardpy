# Copyright (c) 2024 Everypin
# GNU General Public License v3.0 (see LICENSE or https://www.gnu.org/licenses/gpl-3.0.txt)

from logging import getLogger
from typing import Any

from hardpy.pytest_hardpy.reporter.base import BaseReporter
from hardpy.pytest_hardpy.utils import SingletonMeta


class RunnerReporter(BaseReporter, metaclass=SingletonMeta):
    """Reporter for using in direct call from test runner with HardPy plugin."""

    def __init__(self) -> None:
        super().__init__()
        self._log = getLogger(__name__)

    def get_field(self, key: str) -> Any:  # noqa: ANN401
        """Get field from the statestore.

        Args:
            key (str): field name

        Returns:
            Any: field value
        """
        return self._statestore.get_field(key)
