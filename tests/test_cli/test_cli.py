import os
import subprocess
from pathlib import Path

HARDPY_COMMAND = ["hardpy", "init"]

db_no_default_user = "dev1"
db_no_default_password = "dev1"
db_no_default_host = "localhost1"
db_no_default_port = "5985"
frontend_no_default_host = "localhost1"
frontend_no_default_port = "8001"
socket_no_default_host = "localhost1"
socket_no_default_port = "6526"
stand_cloud_no_default_api = "api1.standcloud.localhost"
stand_cloud_no_default_auth = "auth1.standcloud.localhost"

db_default_port = "5984"
frontend_default_host = "localhost"
frontend_default_port = "8000"
socket_default_host = "localhost"
socket_default_port = "6525"
stand_cloud_default_api = "api.standcloud.localhost"
stand_cloud_default_auth = "auth.standcloud.localhost"


def test_cli_init(tmp_path: Path):
    subprocess.run([*HARDPY_COMMAND, tmp_path], check=True)
    expected_files = [
        "database",
        "hardpy.toml",
        "docker-compose.yaml",
        "pytest.ini",
        "test_1.py",
        "conftest.py",
    ]
    assert set(os.listdir(tmp_path)) == set(expected_files)


def test_cli_init_create_db(tmp_path: Path):
    subprocess.run([*HARDPY_COMMAND, tmp_path, "--create-database"], check=True)
    expected_files = [
        "database",
        "docker-compose.yaml",
        "hardpy.toml",
        "pytest.ini",
        "test_1.py",
        "conftest.py",
    ]
    assert set(os.listdir(tmp_path)) == set(expected_files)


def test_cli_init_no_create_db(tmp_path: Path):
    subprocess.run([*HARDPY_COMMAND, tmp_path, "--no-create-database"], check=True)
    expected_files = [
        "hardpy.toml",
        "pytest.ini",
        "test_1.py",
        "conftest.py",
    ]
    assert set(os.listdir(tmp_path)) == set(expected_files)


def test_cli_init_db_user(tmp_path: Path):
    subprocess.run(
        [*HARDPY_COMMAND, tmp_path, "--database-user", db_no_default_user],
        check=True,
    )
    docker_compose_path = tmp_path / "docker-compose.yaml"
    with Path.open(docker_compose_path) as f:
        content = f.read()
        assert (
            f"COUCHDB_USER: {db_no_default_user}" in content
        ), "docker-compose.yaml does not contain the expected user."


def test_cli_init_db_password(tmp_path: Path):
    subprocess.run(
        [*HARDPY_COMMAND, tmp_path, "--database-password", db_no_default_password],
        check=True,
    )
    docker_compose_path = tmp_path / "docker-compose.yaml"
    with Path.open(docker_compose_path) as f:
        content = f.read()
        assert (
            f"COUCHDB_PASSWORD: {db_no_default_password}" in content
        ), "docker-compose.yaml does not contain the expected password."


def test_cli_init_db_host(tmp_path: Path):
    subprocess.run(
        [*HARDPY_COMMAND, tmp_path, "--database-host", db_no_default_host],
        check=True,
    )
    couchdb_ini_path = tmp_path / "database/couchdb.ini"
    with Path.open(couchdb_ini_path) as f:
        content = f.read()
        assert (
            f";bind_address = {db_no_default_host}" in content
        ), "couchdb.ini does not contain the expected host."


def test_cli_init_db_port(tmp_path: Path):
    subprocess.run(
        [*HARDPY_COMMAND, tmp_path, "--database-port", db_no_default_port],
        check=True,
    )
    docker_compose_path = tmp_path / "docker-compose.yaml"
    with Path.open(docker_compose_path) as f:
        content = f.read()
        assert (
            f"{db_no_default_port}:5984" in content
        ), "docker-compose.yaml does not contain the expected port."
    couchdb_ini_path = tmp_path / "database/couchdb.ini"
    with Path.open(couchdb_ini_path) as f:
        content = f.read()
        assert (
            ";port = 5985" in content
        ), "couchdb.ini does not contain the expected port."


def test_cli_init_frontend_host(tmp_path: Path):
    subprocess.run(
        [*HARDPY_COMMAND, tmp_path, "--frontend-host", frontend_no_default_host],
        check=True,
    )
    hardpy_toml_path = tmp_path / "hardpy.toml"
    with Path.open(hardpy_toml_path) as f:
        content = f.read()
        frontend_info = (
            f'[frontend]\nhost = "{frontend_no_default_host}"\nport = 8000\n'
        )
        assert (
            frontend_info in content
        ), "hardpy.toml does not contain the expected host."


def test_cli_init_frontend_port(tmp_path: Path):
    subprocess.run(
        [*HARDPY_COMMAND, tmp_path, "--frontend-port", frontend_no_default_port],
        check=True,
    )
    hardpy_toml_path = tmp_path / "hardpy.toml"
    with Path.open(hardpy_toml_path) as f:
        content = f.read()
        frontend_info = (
            f"[frontend]\n"
            f'host = "localhost"\n'
            f"port = {frontend_no_default_port}\n\n"
        ).format(frontend_no_default_port)
        assert (
            frontend_info in content
        ), "hardpy.toml does not contain the expected port."


def test_cli_init_socket_host(tmp_path: Path):
    subprocess.run(
        [*HARDPY_COMMAND, tmp_path, "--socket-host", socket_no_default_host],
        check=True,
    )
    hardpy_toml_path = tmp_path / "hardpy.toml"
    with Path.open(hardpy_toml_path) as f:
        content = f.read()
        socket_info = f"""[socket]
host = "{socket_no_default_host}"
port = 6525
"""
        assert socket_info in content, "hardpy.toml does not contain the expected host."


def test_cli_init_socket_port(tmp_path: Path):
    subprocess.run(
        [*HARDPY_COMMAND, tmp_path, "--socket-port", socket_no_default_port],
        check=True,
    )
    hardpy_toml_path = tmp_path / "hardpy.toml"
    with Path.open(hardpy_toml_path) as f:
        content = f.read()
        socket_info = f'[socket]\nhost = "localhost"\nport = {socket_no_default_port}\n'
        assert socket_info in content, "hardpy.toml does not contain the expected port."


def test_cli_init_stand_cloud_api(tmp_path: Path):
    subprocess.run(
        [*HARDPY_COMMAND, tmp_path, "--stand-cloud-api", stand_cloud_no_default_api],
        check=True,
    )
    hardpy_toml_path = tmp_path / "hardpy.toml"
    with Path.open(hardpy_toml_path) as f:
        content = f.read()
        stand_cloud_info = f"""[stand_cloud]
api = "{stand_cloud_no_default_api}"
"""
        assert_msg = "hardpy.toml does not contain the expected host."
        assert stand_cloud_info in content, assert_msg


def test_cli_init_stand_cloud_auth(tmp_path: Path):
    subprocess.run(
        [*HARDPY_COMMAND, tmp_path, "--stand-cloud-auth", stand_cloud_no_default_auth],
        check=True,
    )
    hardpy_toml_path = tmp_path / "hardpy.toml"
    with Path.open(hardpy_toml_path) as f:
        content = f.read()
        stand_cloud_info = f'"\nauth = "{stand_cloud_no_default_auth}"'
        assert_msg = "hardpy.toml does not contain the expected host."
        assert stand_cloud_info in content, assert_msg


# TODO(@RiByryn): cli hardpy run
