# Copyright (c) 2024 Everypin
# GNU General Public License v3.0 (see LICENSE or https://www.gnu.org/licenses/gpl-3.0.txt)

from pycouchdb import Server as DbServer

from hardpy.pytest_hardpy.utils import ConnectionData


class BaseServer:
    """Base class for CouchDB server."""

    def __init__(self) -> None:
        con_data = ConnectionData()
        self._db_srv = DbServer(con_data.database_url)
