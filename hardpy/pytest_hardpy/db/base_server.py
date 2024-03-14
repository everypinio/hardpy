# Copyright (c) 2024 Everypin
# GNU General Public License v3.0 (see LICENSE or https://www.gnu.org/licenses/gpl-3.0.txt)

from pycouchdb import Server as DbServer

from hardpy.pytest_hardpy.utils import ConfigData


class BaseServer(object):
    """Base class for CouchDB server."""

    def __init__(self):
        config = ConfigData()
        self._db_srv = DbServer(config.connection_string)
