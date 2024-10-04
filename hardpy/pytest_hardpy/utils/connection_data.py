# Copyright (c) 2024 Everypin
# GNU General Public License v3.0 (see LICENSE or https://www.gnu.org/licenses/gpl-3.0.txt)

from socket import gethostname

from hardpy.pytest_hardpy.utils.singleton import Singleton


class ConnectionData(Singleton):
    """Connection data storage."""

    def __init__(self):
        if not self._initialized:
            self.database_url: str = "http://dev:dev@localhost:5984/"
            self.socket_host: str = gethostname()
            self.socket_port: int = 6525
            self._initialized = True
