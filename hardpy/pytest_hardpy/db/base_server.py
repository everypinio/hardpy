# Copyright (c) 2024 Everypin
# GNU General Public License v3.0 (see LICENSE or https://www.gnu.org/licenses/gpl-3.0.txt)

from os import getcwd
from pathlib import Path

from pycouchdb import Server as DbServer

from hardpy.config import ConfigManager


class BaseServer:
    """Base class for CouchDB server."""

    def __init__(self):
        config = ConfigManager().read_config(Path(getcwd()))
        if config:
            self._db_srv = DbServer(config.database.connection_url())
        else:
            raise FileNotFoundError("The hardpy.toml file is not found")
