# Copyright (c) 2024 Everypin
# GNU General Public License v3.0 (see LICENSE or https://www.gnu.org/licenses/gpl-3.0.txt)

from pathlib import Path
from logging import getLogger

import rtoml
from pydantic import BaseModel, ConfigDict, ValidationError

logger = getLogger(__name__)


class DatabaseConfig(BaseModel):
    model_config = ConfigDict(extra="forbid")

    user: str
    password: str
    host: str
    port: int

    def connection_url(self) -> str:
        """Get database connection url.

        Returns:
            str: database connection url
        """
        credentials = f"{self.user}:{self.password}"
        uri = f"{self.host}:{str(self.port)}"  # noqa: WPS237
        return f"http://{credentials}@{uri}/"


class FrontendConfig(BaseModel):
    model_config = ConfigDict(extra="forbid")

    host: str
    port: int


class SocketConfig(BaseModel):
    model_config = ConfigDict(extra="forbid")

    host: str
    port: int


class HardpyConfig(BaseModel):
    model_config = ConfigDict(extra="forbid")

    title: str = "HardPy TOML config"
    tests_dir: str = "tests"
    database: DatabaseConfig
    frontend: FrontendConfig
    socket: SocketConfig


class ConfigManager:

    obj = HardpyConfig(
        tests_dir="tests",
        database=DatabaseConfig(
            user="dev",
            password="dev",
            host="localhost",
            port=5984,
        ),
        frontend=FrontendConfig(
            host="localhost",
            port=8000,
        ),
        socket=SocketConfig(
            host="localhost",
            port=6525,
        ),
    )
    tests_path = Path.cwd()

    @classmethod
    def init_config(  # noqa: WPS211
        cls,
        tests_dir: str | None = None,
        database_user: str | None = None,
        database_password: str | None = None,
        database_host: str | None = None,
        database_port: int | None = None,
        frontend_host: str | None = None,
        frontend_port: int | None = None,
        socket_host: str | None = None,
        socket_port: int | None = None,
    ):

        if tests_dir:
            cls.obj.tests_dir = str(tests_dir)
        if database_user:
            cls.obj.database.user = database_user
        if database_password:
            cls.obj.database.password = database_password
        if database_host:
            cls.obj.database.host = database_host
        if database_port:
            cls.obj.database.port = database_port
        if frontend_host:
            cls.obj.frontend.host = frontend_host
        if frontend_port:
            cls.obj.frontend.port = frontend_port
        if socket_host:
            cls.obj.socket.host = socket_host
        if socket_port:
            cls.obj.socket.port = socket_port

    @classmethod
    def create_config(cls, parent_dir: Path):
        with open(parent_dir / "hardpy.toml", "w") as file:
            file.write(rtoml.dumps(cls.obj.model_dump()))

    @classmethod
    def read_config(cls, toml_path: Path) -> HardpyConfig | None:
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
    def get_config(cls):
        return cls.obj

    @classmethod
    def get_tests_path(cls):
        return cls.tests_path
