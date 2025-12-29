# Copyright (c) 2024 Everypin
# GNU General Public License v3.0 (see LICENSE or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import annotations

from enum import Enum
from logging import getLogger
from pathlib import Path

import tomli
import tomli_w
from pydantic import BaseModel, ConfigDict, Field, ValidationError

from hardpy.common.singleton import SingletonMeta

logger = getLogger(__name__)


class StorageType(str, Enum):
    """Storage backend types for HardPy data persistence.

    Attributes:
        JSON: JSON file-based storage on local filesystem
        COUCHDB: CouchDB database storage
    """

    JSON = "json"
    COUCHDB = "couchdb"


class DatabaseConfig(BaseModel):
    """Database configuration."""

    model_config = ConfigDict(extra="forbid")

    storage_type: StorageType = StorageType.COUCHDB
    user: str = "dev"
    password: str = "dev"
    host: str = "localhost"
    port: int = 5984
    doc_id: str = Field(exclude=True, default="")
    url: str = Field(exclude=True, default="")
    # This field is relevant only when storage_type is "json"
    storage_path: str = Field(exclude=True, default=".hardpy")

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
    manual_collect: bool = False
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
    test_configs: list[TestConfig] = []

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
        storage_type: str,
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
            storage_type (str): Database storage type.
        """
        self._config.tests_name = tests_name
        self._config.frontend.host = frontend_host
        self._config.frontend.port = frontend_port
        self._config.frontend.language = frontend_language
        self._config.database.user = database_user
        self._config.database.storage_type = StorageType(storage_type)
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
        # test_config is filled in by the user as an array
        config_str = tomli_w.dumps(self._config.model_dump(exclude="test_configs"))
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
            # TODO (xorialexandrov): Add a log that cannot cause tests to fail
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

    def set_current_test_config(self, config_name: str) -> None:
        """Set current test configuration.

        Args:
            config_name (str): Test configuration name
        """
        if self._config.test_configs == []:
            logger.warning("No test configurations available.")
            return

        available_configs = [config.name for config in self._config.test_configs]
        if config_name in available_configs:
            self._config.current_test_config = config_name
        else:
            msg = (
                f"Test configuration {config_name} not ",
                "found among available configurations.",
            )
            logger.warning(msg)
