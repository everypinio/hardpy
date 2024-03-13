# Copyright (c) 2024 Everypin
# GNU General Public License v3.0 (see LICENSE or https://www.gnu.org/licenses/gpl-3.0.txt)

from hardpy.pytest_hardpy.utils.singleton import Singleton
from pathlib import Path


class ConfigData(Singleton):
    """Web connection data storage."""

    def __init__(self):
        if not self._initialized:
            self.db_host: str = "localhost"
            self.db_user: str = "dev"
            self.db_pswd: str = "dev"
            self.db_port: int = 5984
            self.web_host: str = "0.0.0.0"
            self.web_port: int = 8000
            self.tests_dir = Path.cwd()
            self._initialized = True

    @property
    def connection_string(self) -> str:
        """Get couchdb connection string.

        Returns:
            str: couchdb connection string
        """
        credentials = f"{self.db_user}:{self.db_pswd}"
        uri = f"{self.db_host}:{str(self.db_port)}"  # noqa: WPS237
        return f"http://{credentials}@{uri}/"
