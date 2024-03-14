# Copyright (c) 2024 Everypin
# GNU General Public License v3.0 (see LICENSE or https://www.gnu.org/licenses/gpl-3.0.txt)

from dataclasses import dataclass


@dataclass
class CouchdbConfig:  # noqa: WPS306
    """CouchDB loader config."""

    db_name: str = "report"
    user: str = "dev"
    password: str = "dev"
    host: str = "localhost"
    port: int = 5984

    @property
    def connection_string(self) -> str:
        """Get couchdb connection string."""
        credentials = f"{self.user}:{self.password}"
        uri = f"{self.host}:{str(self.port)}"
        return f"http://{credentials}@{uri}/"
