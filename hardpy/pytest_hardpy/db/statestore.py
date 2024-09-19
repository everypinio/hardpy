# Copyright (c) 2024 Everypin
# GNU General Public License v3.0 (see LICENSE or https://www.gnu.org/licenses/gpl-3.0.txt)

from logging import getLogger

from pycouchdb.exceptions import Conflict, NotFound

from hardpy.pytest_hardpy.db.base_store import BaseStore
from hardpy.pytest_hardpy.db import ResultStateStore
from hardpy.pytest_hardpy.utils import Singleton


class StateStore(Singleton, BaseStore):
    """HardPy state storage interface for CouchDB."""

    def __init__(self):
        if not self._initialized:
            super().__init__("statestore")
            self._log = getLogger(__name__)
            self._schema = ResultStateStore
            self._initialized = True

    def clear(self):
        """Clear database."""
        try:
            # Clear the statestore database before each launch
            self._db.delete(self._doc_id)
        except (Conflict, NotFound):
            self._log.debug("Statestore database will be created for the first time")
        self._doc: dict = self._init_doc()
