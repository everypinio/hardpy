# Copyright (c) 2024 Everypin
# GNU General Public License v3.0 (see LICENSE or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import annotations

from logging import getLogger
from pathlib import Path

import tomli
import tomli_w
from pydantic import BaseModel, ConfigDict, Field, ValidationError

from hardpy.common.singleton import SingletonMeta

logger = getLogger(__name__)


class DatabaseConfig(BaseModel):
    """Database configuration."""

    model_config = ConfigDict(extra="forbid")

    user: str = "dev"
    password: str = "dev"
    host: str = "localhost"
    port: int = 5984
    doc_id: str = Field(exclude=True, default="")
    url: str = Field(exclude=True, default="")

    def model_post_init(self, __context) -> None:  # noqa: ANN001,PYI063
        """Get database connection url."""
        self.url = self.get_url()

    def get_url(self) -> str:
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
    full_size_button: bool = False
    sound_on: bool = False
    measurement_display: bool = True
    modal_result: ModalResultConfig = Field(default_factory=lambda: ModalResultConfig())


class ModalResultConfig(BaseModel):
    """Modal result configuration."""

    model_config = ConfigDict(extra="forbid")

    enable: bool = False
    auto_dismiss_pass: bool = True
    auto_dismiss_timeout: int = 5


class StandCloudConfig(BaseModel):
    """StandCloud configuration."""

    model_config = ConfigDict(extra="forbid")

    address: str = "standcloud.io"
    connection_only: bool = False
    autosync: bool = False
    autosync_timeout: int = 30  # 30 minutes
    api_key: str = ""


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

    def model_post_init(self, __context) -> None:  # noqa: ANN001,PYI063
        """Get database document name."""
        self.database.doc_id = self.get_doc_id()

    def get_doc_id(self) -> str:
        """Update database document name."""
        return f"{self.frontend.host}_{self.frontend.port}"


class ConfigManager(metaclass=SingletonMeta):
    """HardPy configuration manager."""

    def __init__(self) -> None:
        self._config = HardpyConfig()
        self._tests_path = Path.cwd()

    @property
    def config(self) -> HardpyConfig:
        """Get HardPy configuration.

        Returns:
            HardpyConfig: HardPy configuration
        """
        return self._config

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
        frontend_host: str,
        frontend_port: int,
        frontend_language: str,
        sc_address: str,
        sc_connection_only: bool,
        sc_autosync: bool,
        sc_api_key: str,
    ) -> None:
        """Initialize the HardPy configuration.

        Only call once to create a configuration.

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
            sc_autosync (bool): StandCloud auto syncronization.
            sc_api_key (str): StandCloud API key.
        """
        self._config.tests_name = tests_name
        self._config.frontend.host = frontend_host
        self._config.frontend.port = frontend_port
        self._config.frontend.language = frontend_language
        self._config.database.user = database_user
        self._config.database.password = database_password
        self._config.database.host = database_host
        self._config.database.port = database_port
        self._config.database.doc_id = self._config.get_doc_id()
        self._config.database.url = self._config.database.get_url()
        self._config.stand_cloud.address = sc_address
        self._config.stand_cloud.connection_only = sc_connection_only
        self._config.stand_cloud.autosync = sc_autosync
        self._config.stand_cloud.api_key = sc_api_key

    def create_config(self, parent_dir: Path) -> None:
        """Create HardPy configuration.

        Args:
            parent_dir (Path): Configuration file parent directory.
        """
        config_dict = self._config.model_dump(exclude_none=True)

        config_dict = self._clean_none_values(config_dict)

        if "database" in config_dict:
            config_dict["database"].pop("doc_id", None)
            config_dict["database"].pop("url", None)

        # Remove empty sections
        if not config_dict.get("stand_cloud", {}).get("address"):
            config_dict.pop("stand_cloud", None)
        if not config_dict.get("tests_name"):
            config_dict.pop("tests_name", None)

        config_str = tomli_w.dumps(config_dict)
        with Path.open(parent_dir / "hardpy.toml", "w") as file:
            file.write(config_str)

    def _clean_none_values(self, obj: any) -> any:
        """Recursively remove None values from nested dictionaries and lists."""
        if isinstance(obj, dict):
            return {
                k: self._clean_none_values(v) for k, v in obj.items() if v is not None
            }
        if isinstance(obj, list):
            return [self._clean_none_values(item) for item in obj if item is not None]
        return obj

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
            self._config = HardpyConfig(**toml_data)
        except ValidationError:
            logger.exception("Error parsing TOML")
            return None
        return self._config

    def get_test_configs(self) -> TestConfigs:
        """Get test configurations for statestore.

        Returns:
            TestConfigs: Test configurations with current and available
        """
        if self._config.test_configs is None:
            return TestConfigs(available=[])

        available_configs = [config.name for config in self._config.test_configs]

        return TestConfigs(
            available=available_configs,
        )

    def set_current_test_config(self, config_name: str) -> None:
        """Set current test configuration.

        Args:
            config_name (str): Test configuration name
        """
        if self._config.test_configs is None:
            logger.warning("No test configurations available.")
            return

        available_configs = [config.name for config in self._config.test_configs]
        if config_name in available_configs:
            self._config.current_test_config = config_name
        else:
            logger.warning(
                "Test configuration '%s' not found among available configurations.",
                config_name,
            )

    def get_current_test_config(self) -> str:
        """Get current test configuration.

        Returns:
            str: Current test configuration name
        """
        return self._config.current_test_config

    def get_test_config_file(self, config_name: str) -> str | None:
        """Get test configuration file by name.

        Args:
            config_name (str): Test configuration name

        Returns:
            str | None: Test configuration file or None if not found
        """
        if self._config.test_configs is None:
            return None
        for config in self._config.test_configs:
            if config.name == config_name:
                return config.file
        return None
