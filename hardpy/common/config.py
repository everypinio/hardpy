# Copyright (c) 2024 Everypin
# GNU General Public License v3.0 (see LICENSE or https://www.gnu.org/licenses/gpl-3.0.txt)

from logging import getLogger
from pathlib import Path

import rtoml
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
        uri = f"{self.host}:{str(self.port)}"  # noqa: WPS237
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


class HardpyConfig(BaseModel):
    """HardPy configuration."""

    model_config = ConfigDict(extra="forbid")

    title: str = "HardPy TOML config"
    tests_dir: str = "tests"
    database: DatabaseConfig = DatabaseConfig()
    frontend: FrontendConfig = FrontendConfig()
    socket: SocketConfig = SocketConfig()


class ConfigManager:
    """HardPy configuration manager."""

    obj = HardpyConfig()
    tests_path = Path.cwd()

    @classmethod
    def init_config(  # noqa: WPS211
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
    ):
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

    @classmethod
    def create_config(cls, parent_dir: Path):
        """Create HardPy configuration.

        Args:
            parent_dir (Path): Configuration file parent directory.
        """
        with open(parent_dir / "hardpy.toml", "w") as file:
            file.write(rtoml.dumps(cls.obj.model_dump()))

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
            logger.error(f"File hardpy.toml not found at path: {toml_file}")
            return None
        try:
            with open(toml_path / "hardpy.toml", "r") as f:
                cls.obj = HardpyConfig(**rtoml.load(f))
            return cls.obj
        except rtoml.TomlParsingError as exc:
            logger.error(f"Error parsing TOML: {exc}")
        except rtoml.TomlSerializationError as exc:
            logger.error(f"Error parsing TOML: {exc}")
        except ValidationError as exc:
            logger.error(f"Error parsing TOML: {exc}")
        return None

    @classmethod
    def get_config(cls) -> HardpyConfig:
        """Get HardPy configuration.

        Returns:
            HardpyConfig: HardPy configuration
        """
        return cls.obj

    @classmethod
    def get_tests_path(cls) -> Path:  # noqa: WPS615
        """Get tests path.

        Returns:
            Path: HardPy tests path
        """
        return cls.tests_path
