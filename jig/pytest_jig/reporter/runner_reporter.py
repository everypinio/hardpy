# Copyright (c) 2024 Everypin
# GNU General Public License v3.0 (see LICENSE or https://www.gnu.org/licenses/gpl-3.0.txt)

from logging import getLogger
from typing import Any

from jig.common.singleton import SingletonMeta
from jig.pytest_jig.reporter.base import BaseReporter


class RunnerReporter(BaseReporter, metaclass=SingletonMeta):
    """Reporter for using in direct call from test runner with Jig plugin."""

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
