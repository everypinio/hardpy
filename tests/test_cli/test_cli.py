from pathlib import Path

import rtoml

from hardpy.common.config import (
    ConfigManager,
    DatabaseConfig,
    FrontendConfig,
    HardpyConfig,
    SocketConfig,
)


def test_database_config():
    config = DatabaseConfig(
        user="test_user",
        password="test_password",  # noqa: S106
        host="test_host",
        port=1234,
    )
    assert config.user == "test_user"
    assert config.password == "test_password"  # noqa: S105
    assert config.host == "test_host"
    assert config.port == 1234

    connection_url = config.connection_url()
    assert connection_url == "http://test_user:test_password@test_host:1234/"


def test_frontend_config():
    config = FrontendConfig(host="test_frontend_host", port=8080)
    assert config.host == "test_frontend_host"
    assert config.port == 8080


def test_socket_config():
    config = SocketConfig(host="test_socket_host", port=9000)
    assert config.host == "test_socket_host"
    assert config.port == 9000


def test_hardpy_config():
    config = HardpyConfig(
        title="Test HardPy Config",
        tests_dir="my_tests",
        database=DatabaseConfig(user="db_user", password="db_password"),  # noqa: S106
        frontend=FrontendConfig(host="fe_host", port=3000),
        socket=SocketConfig(host="socket_host", port=4000),
    )
    assert config.title == "Test HardPy Config"
    assert config.tests_dir == "my_tests"
    assert config.database.user == "db_user"
    assert config.frontend.host == "fe_host"
    assert config.socket.port == 4000


def test_config_manager_init(tmp_path):  # noqa: ANN001
    tests_dir = tmp_path / "my_tests"
    ConfigManager.init_config(
        tests_dir=str(tests_dir),
        database_user="test_user",
        database_password="test_password",  # noqa: S106
        database_host="test_host",
        database_port=5432,
        frontend_host="test_frontend_host",
        frontend_port=8000,
        socket_host="test_socket_host",
        socket_port=6000,
    )
    config = ConfigManager.get_config()
    assert config.tests_dir == str(tests_dir)
    assert config.database.user == "test_user"
    assert config.frontend.host == "test_frontend_host"
    assert config.socket.port == 6000


def test_config_manager_create_config(tmp_path):  # noqa: ANN001
    tests_dir = tmp_path / "my_tests"
    Path.mkdir(tests_dir, exist_ok=True, parents=True)

    ConfigManager.init_config(
        tests_dir=str(tests_dir),
        database_user="test_user",
        database_password="test_password",  # noqa: S106
        database_host="test_host",
        database_port=5432,
        frontend_host="test_frontend_host",
        frontend_port=8000,
        socket_host="test_socket_host",
        socket_port=6000,
    )

    ConfigManager.create_config(tests_dir)

    config_file = tests_dir / "hardpy.toml"
    assert config_file.exists()


# Test data
test_config_data = {
    "title": "Test HardPy Config",
    "tests_dir": "my_tests",
    "database": {
        "user": "db_user",
        "password": "db_password",
        "host": "test_host",
        "port": 5432,
    },
    "frontend": {"host": "test_frontend_host", "port": 8000},
    "socket": {"host": "test_socket_host", "port": 6000},
}


def test_read_config_success(tmp_path):  # noqa: ANN001
    tests_dir = tmp_path / "tests"
    Path.mkdir(tests_dir, exist_ok=True, parents=True)
    with Path.open(tests_dir / "hardpy.toml", "w") as file:
        file.write(rtoml.dumps(test_config_data))

    config = ConfigManager.read_config(tests_dir)
    assert isinstance(config, HardpyConfig)
    assert config.title == test_config_data["title"]
    assert config.tests_dir == test_config_data["tests_dir"]
    assert config.database.user == test_config_data["database"]["user"]


def test_read_config_not_found(tmp_path):  # noqa: ANN001
    tests_dir = tmp_path / "my_tests"
    Path.mkdir(tests_dir, exist_ok=True, parents=True)

    config = ConfigManager.read_config(tests_dir)
    assert config is None


def test_read_config_parsing_error(tmp_path):  # noqa: ANN001
    tests_dir = tmp_path / "my_tests"
    Path.mkdir(tests_dir, exist_ok=True, parents=True)
    with Path.open(tests_dir / "hardpy.toml", "w") as file:
        file.write("invalid_toml_data")


def test_get_config():
    config = ConfigManager.get_config()
    assert isinstance(config, HardpyConfig)


def test_get_tests_path():
    tests_path = ConfigManager.get_tests_path()
    assert isinstance(tests_path, Path)
