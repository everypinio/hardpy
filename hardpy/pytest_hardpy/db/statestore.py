# Copyright (c) 2024 Everypin
# GNU General Public License v3.0 (see LICENSE or https://www.gnu.org/licenses/gpl-3.0.txt)

from logging import getLogger

from hardpy.common.singleton import SingletonMeta
from hardpy.pytest_hardpy.db.base_store import BaseStore
from hardpy.pytest_hardpy.db.schema import ResultStateStore


class StateStore(BaseStore, metaclass=SingletonMeta):
    """HardPy state storage interface for CouchDB."""

    def __init__(self) -> None:
        super().__init__("statestore")
        self._log = getLogger(__name__)
        self._schema = ResultStateStore
