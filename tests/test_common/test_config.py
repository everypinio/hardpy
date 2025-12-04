from pathlib import Path

import tomli
import tomli_w

from hardpy.common.config import (
    ConfigManager,
    DatabaseConfig,
    FrontendConfig,
    HardpyConfig,
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
frontend_no_default_full_size_button = True
frontend_no_default_sound_on = True
frontend_no_default_manual_collect = True
frontend_no_default_measurement_display = False
stand_cloud_no_default_addr = "everypin1.standcloud.localhost"
stand_cloud_no_default_connection_only = True
stand_cloud_no_default_autosync = True
stand_cloud_no_default_api_key = "1"
db_no_default_doc_id = f"{frontend_no_default_host}_{frontend_no_default_port}"

db_default_user = "dev"
db_default_password = "dev"
db_default_host = "localhost"
db_default_port = 5984
db_default_url = f"http://{db_default_user}:{db_default_password}@{db_default_host}:{db_default_port}/"
frontend_default_host = "localhost"
frontend_default_port = 8000
frontend_default_language = "en"
frontend_default_full_size_button = False
frontend_default_sound_on = False
frontend_default_manual_collect = False
frontend_default_measurement_display = True
stand_cloud_default_addr = "standcloud.io"
stand_cloud_dafault_connection_only = False
stand_cloud_default_api_key = ""
stand_cloud_default_autosync = False
stand_cloud_default_autosync_timeout = 30
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
        sc_connection_only=stand_cloud_no_default_connection_only,
        sc_autosync=stand_cloud_no_default_autosync,
        sc_api_key=stand_cloud_no_default_api_key,
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
    assert config.stand_cloud.connection_only == stand_cloud_no_default_connection_only
    assert config.stand_cloud.autosync == stand_cloud_no_default_autosync
    assert config.stand_cloud.api_key == stand_cloud_no_default_api_key


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
    assert config.full_size_button == frontend_default_full_size_button
    assert config.sound_on == frontend_default_sound_on
    assert config.manual_collect == frontend_default_manual_collect
    assert config.measurement_display == frontend_default_measurement_display


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
    assert config.frontend.full_size_button == frontend_default_full_size_button
    assert config.frontend.sound_on == frontend_default_sound_on
    assert config.frontend.manual_collect == frontend_default_manual_collect
    assert config.frontend.measurement_display == frontend_default_measurement_display
    assert config.stand_cloud.address == stand_cloud_default_addr
    assert config.stand_cloud.connection_only == stand_cloud_dafault_connection_only
    assert config.stand_cloud.api_key == stand_cloud_default_api_key
    assert config.stand_cloud.autosync == stand_cloud_default_autosync
    assert config.stand_cloud.autosync_timeout == stand_cloud_default_autosync_timeout


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
        sc_connection_only=stand_cloud_dafault_connection_only,
        sc_autosync=stand_cloud_default_autosync,
        sc_api_key=stand_cloud_default_api_key,
    )

    config_manager.create_config(tests_dir)

    config_file: Path = tests_dir / "hardpy.toml"
    config_data = tomli.loads(config_file.read_text())
    expected_data = config_manager.config.model_dump(exclude="test_configs")

    assert config_data == expected_data


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
            "full_size_button": frontend_default_full_size_button,
            "sound_on": frontend_default_sound_on,
            "manual_collect": True,
            "measurement_display": frontend_default_measurement_display,
        },
        "stand_cloud": {
            "address": stand_cloud_default_addr,
            "connection_only": stand_cloud_dafault_connection_only,
            "autosync": stand_cloud_default_autosync,
            "autosync_timeout": stand_cloud_default_autosync_timeout,
            "api_key": stand_cloud_default_api_key,
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
    assert (
        config.frontend.full_size_button
        == test_config_data["frontend"]["full_size_button"]
    )
    assert config.frontend.sound_on == test_config_data["frontend"]["sound_on"]
    assert (
        config.frontend.manual_collect == test_config_data["frontend"]["manual_collect"]
    )
    assert (
        config.frontend.measurement_display
        == test_config_data["frontend"]["measurement_display"]
    )
    assert config.stand_cloud.address == test_config_data["stand_cloud"]["address"]
    assert (
        config.stand_cloud.connection_only
        == test_config_data["stand_cloud"]["connection_only"]
    )
    assert config.stand_cloud.api_key == test_config_data["stand_cloud"]["api_key"]
    assert config.stand_cloud.autosync == test_config_data["stand_cloud"]["autosync"]
    assert (
        config.stand_cloud.autosync_timeout
        == test_config_data["stand_cloud"]["autosync_timeout"]
    )
