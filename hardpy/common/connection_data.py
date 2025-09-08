# Copyright (c) 2025 Everypin
# GNU General Public License v3.0 (see LICENSE or https://www.gnu.org/licenses/gpl-3.0.txt)

from hardpy.common.singleton import SingletonMeta


class ConnectionData(metaclass=SingletonMeta):
    """Connection data storage."""

    def __init__(self) -> None:
        self.database_url: str = "http://dev:dev@localhost:5984/"
        self.database_doc_id: str = "current"
        self.sc_address: str = ""
        self.sc_connection_only: bool = False
