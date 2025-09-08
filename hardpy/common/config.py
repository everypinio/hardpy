# Copyright (c) 2024 Everypin
# GNU General Public License v3.0 (see LICENSE or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import annotations

from logging import getLogger
from pathlib import Path

import tomli
import tomli_w
from pydantic import BaseModel, ConfigDict, ValidationError

from hardpy.common.singleton import SingletonMeta

logger = getLogger(__name__)


class DatabaseConfig(BaseModel):
    """Database configuration."""

    model_config = ConfigDict(extra="forbid")

    user: str = "dev"
    password: str = "dev"
    host: str = "localhost"
    port: int = 5984
    doc_id: str = ""

    def connection_url(self) -> str:
        """Get database connection url.

        Returns:
            str: database connection url
        """
        credentials = f"{self.user}:{self.password}"
        uri = f"{self.host}:{self.port!s}"
        return f"http://{credentials}@{uri}/"


class FrontendConfig(BaseModel):
    """Frontend configuration."""

    model_config = ConfigDict(extra="forbid")

    host: str = "localhost"
    port: int = 8000
    language: str = "en"


class StandCloudConfig(BaseModel):
    """StandCloud configuration."""

    model_config = ConfigDict(extra="forbid")

    address: str = ""
    connection_only: bool = False


class HardpyConfig(BaseModel, extra="allow"):
    """HardPy configuration."""

    model_config = ConfigDict(extra="forbid")

    title: str = "HardPy TOML config"
    tests_name: str = ""
    database: DatabaseConfig = DatabaseConfig()
    frontend: FrontendConfig = FrontendConfig()
    stand_cloud: StandCloudConfig = StandCloudConfig()

    def get_doc_id(self) -> str:
        """Get the id of the synchronized database document (name).

        Returns:
            str: document name
        """
        if not self.database.doc_id:
            return f"{self.frontend.host}_{self.frontend.port}"
        return self.database.doc_id


class ConfigManager(metaclass=SingletonMeta):
    """HardPy configuration manager."""

    def __init__(self) -> None:
        self.config = HardpyConfig()
        self._test_path = Path.cwd()

    @property
    def tests_path(self) -> Path:
        """Get tests path.

        Returns:
            Path: HardPy tests path
        """
        return self._tests_path

    def init_config(  # noqa: PLR0913
        self,
        tests_name: str,
        database_user: str,
        database_password: str,
        database_host: str,
        database_port: int,
        database_doc_id: str,
        frontend_host: str,
        frontend_port: int,
        frontend_language: str,
        sc_address: str = "",
        sc_connection_only: bool = False,
    ) -> None:
        """Initialize HardPy configuration.

        Args:
            tests_name (str): Tests suite name.
            database_user (str): Database user name.
            database_password (str): Database password.
            database_host (str): Database host.
            database_port (int): Database port.
            database_doc_id (str): Database document name.
            frontend_host (str): Operator panel host.
            frontend_port (int): Operator panel port.
            frontend_language (str): Operator panel language.
            sc_address (str): StandCloud address.
            sc_connection_only (bool): StandCloud check availability.
        """
        self.config.tests_name = tests_name
        self.config.database.user = database_user
        self.config.database.password = database_password
        self.config.database.host = database_host
        self.config.database.port = database_port
        self.config.database.doc_id = database_doc_id
        self.config.frontend.host = frontend_host
        self.config.frontend.port = frontend_port
        self.config.frontend.language = frontend_language
        self.config.stand_cloud.address = sc_address
        self.config.stand_cloud.connection_only = sc_connection_only

    def default_config(self) -> HardpyConfig:
        """Get default HardPy config.

        Returns:
            HardpyConfig: default config.
        """
        return HardpyConfig()

    def create_config(self, parent_dir: Path) -> None:
        """Create HardPy configuration.

        Args:
            parent_dir (Path): Configuration file parent directory.
        """
        config = self.config
        if not self.config.stand_cloud.address:
            del config.stand_cloud
        if not self.config.tests_name:
            del config.tests_name
        if not self.config.database.doc_id:
            del config.database.doc_id
        config_str = tomli_w.dumps(config.model_dump())
        with Path.open(parent_dir / "hardpy.toml", "w") as file:
            file.write(config_str)

    def read_config(self, toml_path: Path) -> HardpyConfig | None:
        """Read HardPy configuration.

        Args:
            toml_path (Path): hardpy.toml file path.

        Returns:
            HardpyConfig | None: HardPy configuration
        """
        self._tests_path = toml_path
        toml_file = toml_path / "hardpy.toml"
        if not toml_file.exists():
            logger.error("File hardpy.toml not found at path: %s", toml_file)
            return None
        try:
            with Path.open(toml_path / "hardpy.toml", "rb") as f:
                toml_data = tomli.load(f)
        except tomli.TOMLDecodeError as exc:
            msg = f"Error parsing TOML: {exc}"
            logger.exception(msg)
            return None

        try:
            self.config = HardpyConfig(**toml_data)
        except ValidationError:
            logger.exception("Error parsing TOML")
            return None
        return self.config
