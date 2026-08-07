# Copyright (c) 2024 Everypin
# GNU General Public License v3.0 (see LICENSE or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import annotations

import ast
import socket
from dataclasses import dataclass

import requests
from urllib3 import disable_warnings


@dataclass
class CouchdbConfig:
    """CouchDB loader config.

    If `connection_str` arg is not set, it will be created from other args.
    """

    db_name: str = "report"
    user: str = "dev"
    password: str = "dev"
    host: str = "localhost"
    port: int = 5984
    connection_str: str | None = None

    def __post_init__(self) -> None:
        """Disable urllib3 warnings.

        More info: https://urllib3.readthedocs.io/en/latest/advanced-usage.html#tls-warnings
        """
        disable_warnings()

    @property
    def connection_string(self) -> str:
        """Get couchdb connection string.

        Raises:
            RuntimeError: CouchDB server is not available

        Returns:
            str: Database connection string.
        """
        if self.connection_str:
            return self.connection_str

        # TODO(xorialexandrov): Modify connection string creating based on protocol.
        #       Some problems with http and https, different ports, local
        #       and cloud databases.
        protocol = self._get_protocol()

        if protocol == "http":
            host_url = f"http://{self.host}:{self.port}"
            uri = f"{self.host}:{self.port!s}"
        elif protocol == "https":
            host_url = f"https://{self.host}"
            uri = f"{self.host}"

        try:
            response = requests.get(host_url, timeout=5)
        except requests.exceptions.RequestException as exc:
            msg = f"Error CouchDB connecting to {host_url}."
            raise RuntimeError(msg) from exc

        # fmt: off
        try:
            couchdb_dict = ast.literal_eval(response._content.decode("utf-8"))  # type: ignore # noqa: SLF001
            couchdb_dict.get("couchdb", False)
        except Exception as exc:
            msg = f"Address {host_url} does not provide CouchDB attributes."
            raise RuntimeError(msg) from exc
        # fmt: on

        credentials = f"{self.user}:{self.password}"
        return f"{protocol}://{credentials}@{uri}/"

    def _get_protocol(self) -> str:
        success = 200
        try:
            # HTTPS attempt
            sock = socket.create_connection((self.host, self.port))
            sock.close()
            request = f"https://{self.host}"
            if requests.get(request, timeout=5).status_code == success:
                return "https"
            raise OSError  # noqa: TRY301
        except OSError:
            try:
                # HTTP attempt
                sock = socket.create_connection((self.host, self.port))
                sock.close()
                request = f"http://{self.host}:{self.port}"
                if requests.get(request, timeout=5).status_code == success:
                    return "http"
                raise OSError  # noqa: TRY301
            except OSError as exc:
                msg = f"Error connecting to couchdb server {self.host}:{self.port}."
                raise RuntimeError(msg) from exc
