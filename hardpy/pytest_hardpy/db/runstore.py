# Copyright (c) 2024 Everypin
# GNU General Public License v3.0 (see LICENSE or https://www.gnu.org/licenses/gpl-3.0.txt)

from logging import getLogger

from pycouchdb.exceptions import Conflict, NotFound

from hardpy.pytest_hardpy.db.base_store import BaseStore
from hardpy.pytest_hardpy.db.schema import ResultRunStore
from hardpy.pytest_hardpy.utils import SingletonMeta


class RunStore(BaseStore, metaclass=SingletonMeta):
    """HardPy run storage interface for CouchDB.

    Save state and case artifact.
    """

    def __init__(self) -> None:
        super().__init__("runstore")
        self._log = getLogger(__name__)
        try:
            # Clear the runstore database before each launch
            self._db.delete(self._doc_id)
        except (Conflict, NotFound):
            self._log.debug("Runstore database will be created for the first time")
        self._doc: dict = self._init_doc()
        self._schema = ResultRunStore
