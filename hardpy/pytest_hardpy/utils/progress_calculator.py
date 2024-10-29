# Copyright (c) 2024 Everypin
# GNU General Public License v3.0 (see LICENSE or https://www.gnu.org/licenses/gpl-3.0.txt)

from logging import getLogger


class ProgressCalculator:
    """Test run progress calculator."""

    def __init__(self) -> None:
        self._progress_nodeids: set[str] = set()
        self._tests_amount: int = 1
        self._log = getLogger(__name__)

    def set_test_amount(self, amount: int) -> None:
        """Set test amount.

        Raises:
            ValueError: if test amount is less than 0

        Args:
            amount (int): test amount
        """
        if amount <= 0:
            msg = "Test amount must be greater than 0."
            raise ValueError(msg)
        self._tests_amount = amount

    def calculate(self, nodeid: str) -> int:
        """Calculate test progress.

        Args:
            nodeid (str): current node id

        Returns:
            int: test progress in percent
        """
        self._progress_nodeids.add(nodeid)
        return len(self._progress_nodeids) * 100 // self._tests_amount
