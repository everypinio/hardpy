from pathlib import Path

import rtoml

from hardpy.common.config import (
    ConfigManager,
    DatabaseConfig,
    FrontendConfig,
    HardpyConfig,
    SocketConfig,
)

db_no_default_user = "dev1"
db_no_default_password = "dev1"
db_no_default_host = "localhost1"
db_no_default_port = 5985
frontend_no_default_host = "localhost1"
frontend_no_default_port = 8001
socket_no_default_host = "localhost1"
socket_no_default_port = 6526

db_default_user = "dev"
db_default_password = "dev"
db_default_host = "localhost"
db_default_port = 5984
frontend_default_host = "localhost"
frontend_default_port = 8000
socket_default_host = "localhost"
socket_default_port = 6525


def test_config_manager_init(tmp_path: Path):
    tests_dir = tmp_path / "my_tests"
    ConfigManager.init_config(
        tests_dir=str(tests_dir),
        database_user=db_no_default_user,
        database_password=db_no_default_password,
        database_host=db_no_default_host,
        database_port=db_no_default_port,
        frontend_host=frontend_no_default_host,
        frontend_port=frontend_no_default_port,
        socket_host=socket_no_default_host,
        socket_port=socket_no_default_port,
    )
    config = ConfigManager.get_config()
    assert isinstance(config, HardpyConfig)
    assert config.tests_dir == str(tests_dir)
    assert config.database.user == db_no_default_user
    assert config.database.password == db_no_default_password
    assert config.database.host == db_no_default_host
    assert config.database.port == db_no_default_port
    assert config.frontend.host == frontend_no_default_host
    assert config.frontend.port == frontend_no_default_port
    assert config.socket.host == socket_no_default_host
    assert config.socket.port == socket_no_default_port


def test_database_config():
    config = DatabaseConfig()
    assert config.user == db_default_user
    assert config.password == db_default_password
    assert config.host == db_no_default_host
    assert config.port == db_default_port

    connection_url = config.connection_url()
    assert (
        connection_url
        == f"http://{db_default_user}:{db_default_password}@{db_default_host}:{db_default_port}/"
    )


def test_frontend_config():
    config = FrontendConfig()
    assert config.host == frontend_default_host
    assert config.port == frontend_default_port


def test_socket_config():
    config = SocketConfig()
    assert config.host == socket_default_host
    assert config.port == socket_default_port


def test_hardpy_config():
    config = HardpyConfig(
        title="HardPy TOML config",
        tests_dir="tests",
        database=DatabaseConfig(),
        frontend=FrontendConfig(),
        socket=SocketConfig(),
    )
    assert config.title == "HardPy TOML config"
    assert config.tests_dir == "tests"
    assert config.database.user == db_default_user
    assert config.database.password == db_default_password
    assert config.database.host == db_default_host
    assert config.database.port == db_default_port
    assert config.frontend.host == frontend_default_host
    assert config.frontend.port == frontend_default_port
    assert config.socket.host == socket_default_host
    assert config.socket.port == socket_default_port


def test_config_manager_create_config(tmp_path: Path):
    tests_dir = tmp_path / "my_tests"
    Path.mkdir(tests_dir, exist_ok=True, parents=True)

    ConfigManager.init_config(
        tests_dir=str(tests_dir),
        database_user=db_default_user,
        database_password=db_default_password,
        database_host=db_default_host,
        database_port=db_default_port,
        frontend_host=frontend_default_host,
        frontend_port=frontend_default_port,
        socket_host=socket_default_host,
        socket_port=socket_default_port,
    )

    ConfigManager.create_config(tests_dir)

    config_file: Path = tests_dir / "hardpy.toml"
    assert config_file.read_text() == rtoml.dumps(
        ConfigManager.get_config().model_dump(),
    )


def test_read_config_success(tmp_path: Path):
    test_config_data = {
        "title": "Test HardPy Config",
        "tests_dir": "my_tests",
        "database": {
            "user": db_default_user,
            "password": db_default_password,
            "host": db_default_host,
            "port": db_default_port,
        },
        "frontend": {"host": frontend_default_host, "port": frontend_default_port},
        "socket": {"host": socket_default_host, "port": socket_default_port},
    }
    tests_dir = tmp_path / "tests"
    Path.mkdir(tests_dir, exist_ok=True, parents=True)
    with Path.open(tests_dir / "hardpy.toml", "w") as file:
        file.write(rtoml.dumps(test_config_data))

    config = ConfigManager.read_config(tests_dir)
    assert isinstance(config, HardpyConfig)
    assert config.title == test_config_data["title"]
    assert config.tests_dir == test_config_data["tests_dir"]
    assert config.database.user == test_config_data["database"]["user"]
