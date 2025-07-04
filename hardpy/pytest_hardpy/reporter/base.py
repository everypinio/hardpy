# Copyright (c) 2024 Everypin
# GNU General Public License v3.0 (see LICENSE or https://www.gnu.org/licenses/gpl-3.0.txt)

from logging import getLogger
from typing import Any

from hardpy.pytest_hardpy.db import (
    DatabaseField as DF,  # noqa: N817
    RunStore,
    StateStore,
)


class BaseReporter:
    """Base class for test reporter."""

    def __init__(self) -> None:
        self._statestore = StateStore()
        self._runstore = RunStore()
        self._log = getLogger(__name__)

    def set_doc_value(
        self,
        key: str,
        value: Any,  # noqa: ANN401
        runstore_only: bool = False,
        statestore_only: bool = False,
    ) -> None:
        """Set value to the document.

        Update a document without writing to the database.

        Args:
            key (str): document key
            value: document value
            runstore_only (bool, optional): indicates whether data should
                                             be written to RunStore. Defaults to True.
            statestore_only (bool, optional): indicates whether data should
                                            be written to StateStore. Defaults to True.

        Raises:
            ValueError: if both runstore_only and statestore_only are True
        """
        if runstore_only and statestore_only:
            msg = "Both runstore_only and statestore_only cannot be True"
            raise ValueError(msg)
        if runstore_only:
            self._runstore.update_doc_value(key, value)
            return
        if statestore_only:
            self._statestore.update_doc_value(key, value)
            return
        self._runstore.update_doc_value(key, value)
        self._statestore.update_doc_value(key, value)

    def set_alert(self, alert: str) -> None:
        """Set alert message.

        Args:
            alert (str): alert message
        """
        self.set_doc_value(DF.ALERT, alert, statestore_only=True)

    def update_db_by_doc(self) -> None:
        """Update database by current document."""
        self._statestore.update_db()
        self._runstore.update_db()

    def update_doc_by_db(self) -> None:
        """Update document by current database."""
        self._statestore.update_doc()
        self._runstore.update_doc()

    def generate_key(self, *args: Any) -> str:  # noqa: ANN401
        """Generate key for database.

        Args:
            args: list of database keys

        Returns:
            str: database key
        """
        return ".".join(args)

    def get_current_attempt(self, module_id: str, case_id: str) -> int:
        """Get current attempt.

        Returns:
            int: current attempt
        """
        key = self.generate_key(
            DF.MODULES,
            module_id,
            DF.CASES,
            case_id,
            DF.ATTEMPT,
        )
        return self._statestore.get_field(key)
