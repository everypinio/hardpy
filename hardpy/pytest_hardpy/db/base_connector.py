# Copyright (c) 2024 Everypin
# GNU General Public License v3.0 (see LICENSE or https://www.gnu.org/licenses/gpl-3.0.txt)

from pycouchdb.client import Database
from pycouchdb.exceptions import Conflict, GenericError
from requests.exceptions import ConnectionError  # noqa: A004

from hardpy.pytest_hardpy.db.base_server import BaseServer


class BaseConnector(BaseServer):
    """Base class for CouchDB connector."""

    def __init__(self, db_name: str) -> None:
        super().__init__()
        self._db_name = db_name
        self._db = self._init_db()
        self._doc_id = "current"

    def _init_db(self) -> Database:
        try:
            return self._db_srv.create(self._db_name)  # type: ignore
        except Conflict:
            # database is already created
            return self._db_srv.database(self._db_name)
        except GenericError as exc:
            msg = f"Error initializing database {exc}"
            raise RuntimeError(msg) from exc
        except ConnectionError as exc:
            msg = f"Error initializing database: {exc}"
            raise RuntimeError(msg) from exc
