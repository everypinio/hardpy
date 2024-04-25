# Copyright (c) 2024 Everypin
# GNU General Public License v3.0 (see LICENSE or https://www.gnu.org/licenses/gpl-3.0.txt)

from logging import getLogger

from hardpy.pytest_hardpy.db import StateStore, RunStore


class BaseReporter(object):
    """Base class for test reporter."""

    def __init__(self):
        self._statestore = StateStore()
        self._runstore = RunStore()
        self._log = getLogger(__name__)

    def update_doc(self, key: str, value, is_statestore=True, is_runstore=True):
        """Update document in the database.

        Update document without database by key and value.

        Args:
            key (str): document key
            value: document value
            is_statestore (bool, optional): indicates whether data should
                                             be written to StateStore. Defaults to True.
            is_runstore (bool, optional): indicates whether data should
                                            be written to RunStore. Defaults to True.
        """
        if is_statestore:
            self._statestore.update_doc(key, value)
        if is_runstore:
            self._runstore.update_doc(key, value)

    def update_db(self):
        """Update database by current document."""
        self._statestore.update_db()
        self._runstore.update_db()

    def set_db_value(self, key: str, value, is_statestore=True, is_runstore=True):
        """Set value to database.

        Args:
            key (str): database key
            value: database value
            is_statestore (bool, optional): indicates whether data should
                                             be written to StateStore. Defaults to True.
            is_runstore (bool, optional): indicates whether data should
                                            be written to RunStore. Defaults to True.
        """
        if is_statestore:
            self._statestore.set_value(key, value)
        if is_runstore:
            self._runstore.set_value(key, value)

    def generate_key(self, *args) -> str:
        """Generate key for database.

        Args:
            args: list of database keys

        Returns:
            str: database key
        """
        return ".".join(args)
