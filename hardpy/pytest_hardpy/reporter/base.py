# Copyright (c) 2024 Everypin
# GNU General Public License v3.0 (see LICENSE or https://www.gnu.org/licenses/gpl-3.0.txt)

from logging import getLogger

from hardpy.pytest_hardpy.db import StateStore, RunStore


class BaseReporter:
    """Base class for test reporter."""

    def __init__(self):
        self._statestore = StateStore()
        self._runstore = RunStore()
        self._log = getLogger(__name__)

    def set_doc_value(
        self, key: str, value, runstore_only=False, statestore_only=False
    ):
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
            raise ValueError("Both runstore_only and statestore_only cannot be True")
        if runstore_only:
            self._runstore.update_doc(key, value)
            return
        if statestore_only:
            self._statestore.update_doc(key, value)
            return
        self._runstore.update_doc(key, value)
        self._statestore.update_doc(key, value)

    def update_db_by_doc(self):
        """Update database by current document."""
        self._statestore.update_db()
        self._runstore.update_db()

    def generate_key(self, *args) -> str:
        """Generate key for database.

        Args:
            args: list of database keys

        Returns:
            str: database key
        """
        return ".".join(args)
