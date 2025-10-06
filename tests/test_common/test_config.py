from pathlib import Path

import tomli
import tomli_w

from hardpy.common.config import (
    ConfigManager,
    DatabaseConfig,
    FrontendConfig,
    HardpyConfig,
    ModalResultConfig,
    StandCloudConfig,
)

tests_no_default_name = "Tests1"
db_no_default_user = "dev1"
db_no_default_password = "dev1"
db_no_default_host = "localhost1"
db_no_default_port = 5985
db_no_default_url = f"http://{db_no_default_user}:{db_no_default_password}@{db_no_default_host}:{db_no_default_port}/"
frontend_no_default_host = "localhost1"
frontend_no_default_port = 8001
stand_cloud_no_default_addr = "everypin1.standcloud.localhost"
db_no_default_doc_id = f"{frontend_no_default_host}_{frontend_no_default_port}"

db_default_user = "dev"
db_default_password = "dev"
db_default_host = "localhost"
db_default_port = 5984
db_default_url = f"http://{db_default_user}:{db_default_password}@{db_default_host}:{db_default_port}/"
frontend_default_host = "localhost"
frontend_default_port = 8000
frontend_default_language = "en"
stand_cloud_default_addr = ""
db_default_doc_id = f"{frontend_default_host}_{frontend_default_port}"


def test_config_manager_init():
    config_manager = ConfigManager()
    config_manager.init_config(
        tests_name=tests_no_default_name,
        database_user=db_no_default_user,
        database_password=db_no_default_password,
        database_host=db_no_default_host,
        database_port=db_no_default_port,
        frontend_host=frontend_no_default_host,
        frontend_port=frontend_no_default_port,
        frontend_language=frontend_default_language,
        sc_address=stand_cloud_no_default_addr,
        modal_result_enabled=True,
        modal_result_auto_dismiss_pass=False,
        modal_result_auto_dismiss_timeout=10,
    )
    config = config_manager.config
    assert isinstance(config, HardpyConfig)
    assert config.tests_name == tests_no_default_name
    assert config.database.user == db_no_default_user
    assert config.database.password == db_no_default_password
    assert config.database.host == db_no_default_host
    assert config.database.port == db_no_default_port
    assert config.database.doc_id == db_no_default_doc_id
    assert config.database.url == db_no_default_url
    assert config.frontend.host == frontend_no_default_host
    assert config.frontend.port == frontend_no_default_port
    assert config.frontend.language == frontend_default_language
    assert config.stand_cloud.address == stand_cloud_no_default_addr
    assert config.frontend.modal_result.enabled is True
    assert config.frontend.modal_result.auto_dismiss_pass is False
    assert config.frontend.modal_result.auto_dismiss_timeout == 10


def test_database_config():
    config = DatabaseConfig()
    assert config.user == db_default_user
    assert config.password == db_default_password
    assert config.host == db_default_host
    assert config.port == db_default_port
    assert config.doc_id == ""  # default before HardPyConfig init
    assert config.url == db_default_url


def test_frontend_config():
    config = FrontendConfig()
    assert config.host == frontend_default_host
    assert config.port == frontend_default_port
    assert config.language == frontend_default_language
    assert config.modal_result.enabled is False
    assert config.modal_result.auto_dismiss_pass is True
    assert config.modal_result.auto_dismiss_timeout == 5


def test_modal_result_config():
    config = ModalResultConfig()
    assert config.enabled is False
    assert config.auto_dismiss_pass is True
    assert config.auto_dismiss_timeout == 5


def test_stand_cloud_config():
    config = StandCloudConfig()
    assert config.address == stand_cloud_default_addr


def test_hardpy_config():
    config = HardpyConfig(
        title="HardPy TOML config",
        tests_name="tests",
        database=DatabaseConfig(),
        frontend=FrontendConfig(),
        stand_cloud=StandCloudConfig(),
    )
    assert config.title == "HardPy TOML config"
    assert config.tests_name == "tests"
    assert config.database.user == db_default_user
    assert config.database.password == db_default_password
    assert config.database.host == db_default_host
    assert config.database.port == db_default_port
    assert config.database.url == db_default_url
    assert config.database.doc_id == db_default_doc_id
    assert config.frontend.host == frontend_default_host
    assert config.frontend.port == frontend_default_port
    assert config.frontend.language == frontend_default_language
    assert config.stand_cloud.address == stand_cloud_default_addr
    assert config.frontend.modal_result.enabled is False
    assert config.frontend.modal_result.auto_dismiss_pass is True
    assert config.frontend.modal_result.auto_dismiss_timeout == 5


def test_config_manager_create_config(tmp_path: Path):
    tests_dir = tmp_path / "my_tests"
    Path.mkdir(tests_dir, exist_ok=True, parents=True)

    config_manager = ConfigManager()
    config_manager.init_config(
        tests_name=str(tests_dir),
        database_user=db_default_user,
        database_password=db_default_password,
        database_host=db_default_host,
        database_port=db_default_port,
        frontend_host=frontend_default_host,
        frontend_port=frontend_default_port,
        frontend_language=frontend_default_language,
        sc_address=stand_cloud_default_addr,
        modal_result_enabled=True,
        modal_result_auto_dismiss_pass=False,
        modal_result_auto_dismiss_timeout=20,
    )

    config_manager.create_config(tests_dir)

    config_file: Path = tests_dir / "hardpy.toml"
    config_data = tomli.loads(config_file.read_text())
    expected_data = config_manager.config.model_dump()

    assert config_data == expected_data
    assert "modal_result" in config_data["frontend"]
    assert config_data["frontend"]["modal_result"]["enabled"] is True
    assert config_data["frontend"]["modal_result"]["auto_dismiss_pass"] is False
    assert config_data["frontend"]["modal_result"]["auto_dismiss_timeout"] == 20


def test_read_config_success(tmp_path: Path):
    test_config_data = {
        "title": "Test HardPy Config",
        "tests_name": "My tests",
        "database": {
            "user": db_default_user,
            "password": db_default_password,
            "host": db_default_host,
            "port": db_default_port,
        },
        "frontend": {
            "host": frontend_default_host,
            "port": frontend_default_port,
            "language": frontend_default_language,
            "modal_result": {
                "enabled": True,
                "auto_dismiss_pass": False,
                "auto_dismiss_timeout": 15,
            },
        },
        "stand_cloud": {
            "address": stand_cloud_default_addr,
        },
    }
    tests_dir = tmp_path / "tests"
    Path.mkdir(tests_dir, exist_ok=True, parents=True)
    with Path.open(tests_dir / "hardpy.toml", "w") as file:
        file.write(tomli_w.dumps(test_config_data))

    config_manager = ConfigManager()
    config = config_manager.read_config(tests_dir)
    assert isinstance(config, HardpyConfig)
    assert config.title == test_config_data["title"]
    assert config.tests_name == test_config_data["tests_name"]
    assert config.database.user == test_config_data["database"]["user"]
    assert config.database.password == test_config_data["database"]["password"]
    assert config.database.host == test_config_data["database"]["host"]
    assert config.database.port == test_config_data["database"]["port"]
    assert config.database.url == db_default_url
    assert config.database.doc_id == db_default_doc_id
    assert config.frontend.host == test_config_data["frontend"]["host"]
    assert config.frontend.port == test_config_data["frontend"]["port"]
    assert config.frontend.language == test_config_data["frontend"]["language"]
    assert config.stand_cloud.address == test_config_data["stand_cloud"]["address"]
    assert config.frontend.modal_result.enabled is True
    assert config.frontend.modal_result.auto_dismiss_pass is False
    assert config.frontend.modal_result.auto_dismiss_timeout == 15


def test_read_config_without_modal_result(tmp_path: Path):
    """Test reading config without modal_result section (backward compatibility)."""
    test_config_data = {
        "title": "Test HardPy Config",
        "tests_name": "My tests",
        "database": {
            "user": db_default_user,
            "password": db_default_password,
            "host": db_default_host,
            "port": db_default_port,
        },
        "frontend": {
            "host": frontend_default_host,
            "port": frontend_default_port,
            "language": frontend_default_language,
        },
        "stand_cloud": {
            "address": stand_cloud_default_addr,
        },
    }
    tests_dir = tmp_path / "tests"
    Path.mkdir(tests_dir, exist_ok=True, parents=True)
    with Path.open(tests_dir / "hardpy.toml", "w") as file:
        file.write(tomli_w.dumps(test_config_data))

    config_manager = ConfigManager()
    config = config_manager.read_config(tests_dir)
    assert isinstance(config, HardpyConfig)
    assert config.frontend.modal_result.enabled is False
    assert config.frontend.modal_result.auto_dismiss_pass is True
    assert config.frontend.modal_result.auto_dismiss_timeout == 5
