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
    config = DatabaseConfig()
    assert config.user == "dev"
    assert config.password == "dev"  # noqa: S105
    assert config.host == "localhost"
    assert config.port == 5984

    connection_url = config.connection_url()
    assert connection_url == "http://dev:dev@localhost:5984/"


def test_frontend_config():
    config = FrontendConfig()
    assert config.host == "localhost"
    assert config.port == 8000


def test_socket_config():
    config = SocketConfig()
    assert config.host == "localhost"
    assert config.port == 6525


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
        frontend_port=8080,
        socket_host="test_socket_host",
        socket_port=6000,
    )
    config = ConfigManager.get_config()
    assert isinstance(config, HardpyConfig)
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
    assert config_file.read_text() == rtoml.dumps(
        ConfigManager.get_config().model_dump(),
    )


def test_read_config_success(tmp_path):  # noqa: ANN001
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
    tests_dir = tmp_path / "tests"
    Path.mkdir(tests_dir, exist_ok=True, parents=True)
    with Path.open(tests_dir / "hardpy.toml", "w") as file:
        file.write(rtoml.dumps(test_config_data))

    config = ConfigManager.read_config(tests_dir)
    assert isinstance(config, HardpyConfig)
    assert config.title == test_config_data["title"]
    assert config.tests_dir == test_config_data["tests_dir"]
    assert config.database.user == test_config_data["database"]["user"]
