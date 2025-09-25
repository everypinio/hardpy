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
    language: str = "en"


class StandCloudConfig(BaseModel):
    """StandCloud configuration."""

    model_config = ConfigDict(extra="forbid")

    address: str = ""
    connection_only: bool = False


class TestConfig(BaseModel):
    """Test configuration entry."""

    model_config = ConfigDict(extra="allow")

    name: str
    description: str = ""
    file: str | None = None


class TestConfigs(BaseModel):
    """Test configurations container."""

    model_config = ConfigDict(extra="allow")

    available: list[str] = []


class HardpyConfig(BaseModel, extra="allow"):
    """HardPy configuration."""

    model_config = ConfigDict(extra="forbid")

    title: str = "HardPy TOML config"
    tests_name: str = ""
    database: DatabaseConfig = DatabaseConfig()
    frontend: FrontendConfig = FrontendConfig()
    stand_cloud: StandCloudConfig = StandCloudConfig()
    current_test_config: str = ""
    test_configs: list[TestConfig] | None = None
    sound_on: bool = False
    enable_test_pass_fail_modal: bool = False


class ConfigManager:
    """HardPy configuration manager."""

    obj = HardpyConfig()
    tests_path = Path.cwd()

    @classmethod
    def init_config(  # noqa: PLR0913
        cls,
        tests_name: str,
        database_user: str,
        database_password: str,
        database_host: str,
        database_port: int,
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
            frontend_host (str): Operator panel host.
            frontend_port (int): Operator panel port.
            frontend_language (str): Operator panel language.
            sc_address (str): StandCloud address.
            sc_connection_only (bool): StandCloud check availability.
        """
        cls.obj.tests_name = tests_name
        cls.obj.database.user = database_user
        cls.obj.database.password = database_password
        cls.obj.database.host = database_host
        cls.obj.database.port = database_port
        cls.obj.frontend.host = frontend_host
        cls.obj.frontend.port = frontend_port
        cls.obj.frontend.language = frontend_language
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
        if not cls.obj.tests_name:
            del cls.obj.tests_name
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
                toml_data = tomli.load(f)
        except tomli.TOMLDecodeError as exc:
            msg = f"Error parsing TOML: {exc}"
            logger.exception(msg)
            return None

        try:
            cls.obj = HardpyConfig(**toml_data)
        except ValidationError:
            logger.exception("Error parsing TOML")
            return None
        return cls.obj

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

    @classmethod
    def get_test_configs(cls) -> TestConfigs:
        """Get test configurations for statestore.

        Returns:
            TestConfigs: Test configurations with current and available
        """
        available_configs = [config.name for config in cls.obj.test_configs]

        return TestConfigs(
            available = available_configs,
        )

    @classmethod
    def set_current_test_config(cls, config_name: str) -> None:
        """Set current test configuration.

        Args:
            config_name (str): Test configuration name
        """
        available_configs = [config.name for config in cls.obj.test_configs]
        if config_name in available_configs:
            cls.obj.current_test_config = config_name
        else:
            logger.warning("Test configuration '%s' \
                           not found among available configurations.", config_name)

    @classmethod
    def get_current_test_config(cls) -> str:
        """Get current test configuration.

        Returns:
            str: Current test configuration name
        """
        return cls.obj.current_test_config

    @classmethod
    def get_test_config_file(cls, config_name: str) -> str | None:
        """Get test configuration file by name.

        Args:
            config_name (str): Test configuration name

        Returns:
            str | None: Test configuration file or None if not found
        """
        if cls.obj.test_configs is None:
            return None
        for config in cls.obj.test_configs:
            if config.name == config_name:
                return config.file
        return None
