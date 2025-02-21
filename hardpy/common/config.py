# Copyright (c) 2024 Everypin
# GNU General Public License v3.0 (see LICENSE or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import annotations

from logging import getLogger
from pathlib import Path

import tomli
import tomli_w
from pydantic import BaseModel, ConfigDict, ValidationError

logger = getLogger(__name__)


class DatabaseConfig(BaseModel):
    """Database configuration."""

    model_config = ConfigDict(extra="forbid")

    user: str = "dev"
    password: str = "dev"
    host: str = "localhost"
    port: int = 5984

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


class SocketConfig(BaseModel):
    """Socket configuration."""

    model_config = ConfigDict(extra="forbid")

    host: str = "localhost"
    port: int = 6525

class StandCloudConfig(BaseModel):
    """StandCloud configuration."""

    model_config = ConfigDict(extra="forbid")

    address: str = ""
    connection_only: bool = False

class HardpyConfig(BaseModel):
    """HardPy configuration."""

    model_config = ConfigDict(extra="forbid")

    title: str = "HardPy TOML config"
    tests_dir: str = "tests"
    database: DatabaseConfig = DatabaseConfig()
    frontend: FrontendConfig = FrontendConfig()
    socket: SocketConfig = SocketConfig()
    stand_cloud: StandCloudConfig = StandCloudConfig()


class ConfigManager:
    """HardPy configuration manager."""

    obj = HardpyConfig()
    tests_path = Path.cwd()

    @classmethod
    def init_config(  # noqa: PLR0913
        cls,
        tests_dir: str,
        database_user: str,
        database_password: str,
        database_host: str,
        database_port: int,
        frontend_host: str,
        frontend_port: int,
        socket_host: str,
        socket_port: int,
        sc_address: str = "",
        sc_connection_only: bool = False,
    ) -> None:
        """Initialize HardPy configuration.

        Args:
            tests_dir (str): Tests directory.
            database_user (str): Database user name.
            database_password (str): Database password.
            database_host (str): Database host.
            database_port (int): Database port.
            frontend_host (str): Operator panel host.
            frontend_port (int): Operator panel port.
            socket_host (str): Socket host.
            socket_port (int): Socket port.
            sc_address (str): StandCloud address.
            sc_connection_only (bool): StandCloud check availability.
        """
        cls.obj.tests_dir = str(tests_dir)
        cls.obj.database.user = database_user
        cls.obj.database.password = database_password
        cls.obj.database.host = database_host
        cls.obj.database.port = database_port
        cls.obj.frontend.host = frontend_host
        cls.obj.frontend.port = frontend_port
        cls.obj.socket.host = socket_host
        cls.obj.socket.port = socket_port
        cls.obj.stand_cloud.address = sc_address
        cls.obj.stand_cloud.connection_only = sc_connection_only

    @classmethod
    def create_config(cls, parent_dir: Path) -> None:
        """Create HardPy configuration.

        Args:
            parent_dir (Path): Configuration file parent directory.
        """
        if not cls.obj.stand_cloud.address:
            del cls.obj.stand_cloud
        config_str = tomli_w.dumps(cls.obj.model_dump())
        with Path.open(parent_dir / "hardpy.toml", "w") as file:
            file.write(config_str)

    @classmethod
    def read_config(cls, toml_path: Path) -> HardpyConfig | None:
        """Read HardPy configuration.

        Args:
            toml_path (Path): hardpy.toml file path.

        Returns:
            HardpyConfig | None: HardPy configuration
        """
        cls.tests_path = toml_path
        toml_file = toml_path / "hardpy.toml"
        if not toml_file.exists():
            logger.error("File hardpy.toml not found at path: %s", toml_file)
            return None
        try:
            with Path.open(toml_path / "hardpy.toml", "rb") as f:
                cls.obj = HardpyConfig(**tomli.load(f))
            return cls.obj  # noqa: TRY300
        except tomli.TOMLDecodeError:
            logger.exception("Error parsing TOML")
        except ValidationError:
            logger.exception("Error parsing TOML")
        return None

    @classmethod
    def get_config(cls) -> HardpyConfig:
        """Get HardPy configuration.

        Returns:
            HardpyConfig: HardPy configuration
        """
        return cls.obj

    @classmethod
    def get_tests_path(cls) -> Path:
        """Get tests path.

        Returns:
            Path: HardPy tests path
        """
        return cls.tests_path
