# Copyright (c) 2024 Everypin
# GNU General Public License v3.0 (see LICENSE or https://www.gnu.org/licenses/gpl-3.0.txt)

from socket import gethostname

from hardpy.pytest_hardpy.utils.singleton import SingletonMeta


class ConnectionData(metaclass=SingletonMeta):
    """Connection data storage."""

    def __init__(self) -> None:
        self.database_url: str = "http://dev:dev@localhost:5984/"
        self.socket_host: str = gethostname()
        self.socket_port: int = 6525
        self.sc_address: str = ""
        self.sc_connection_only: bool = False
