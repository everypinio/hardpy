import os
import subprocess
from pathlib import Path

HARDPY_COMMAND = ["hardpy", "init"]

db_user = "dev1"
db_password = "dev1"
db_host = "localhost1"
db_port = "5985"

frontend_host = "localhost1"
frontend_port = "8001"

socket_host = "localhost1"
socket_port = "6526"


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
    subprocess.run([*HARDPY_COMMAND, tmp_path, "--database-user", db_user], check=True)
    docker_compose_path = tmp_path / "docker-compose.yaml"
    with Path.open(docker_compose_path) as f:
        content = f.read()
        assert (
            f"COUCHDB_USER: {db_user}" in content
        ), "docker-compose.yaml does not contain the expected user."


def test_cli_init_db_password(tmp_path: Path):
    subprocess.run(
        [*HARDPY_COMMAND, tmp_path, "--database-password", db_password],
        check=True,
    )
    docker_compose_path = tmp_path / "docker-compose.yaml"
    with Path.open(docker_compose_path) as f:
        content = f.read()
        assert (
            f"COUCHDB_PASSWORD: {db_password}" in content
        ), "docker-compose.yaml does not contain the expected password."


def test_cli_init_db_host(tmp_path: Path):
    subprocess.run([*HARDPY_COMMAND, tmp_path, "--database-host", db_host], check=True)
    couchdb_ini_path = tmp_path / "database/couchdb.ini"
    with Path.open(couchdb_ini_path) as f:
        content = f.read()
        assert (
            f";bind_address = {db_host}" in content
        ), "couchdb.ini does not contain the expected host."


def test_cli_init_db_port(tmp_path: Path):
    subprocess.run([*HARDPY_COMMAND, tmp_path, "--database-port", db_port], check=True)
    docker_compose_path = tmp_path / "docker-compose.yaml"
    with Path.open(docker_compose_path) as f:
        content = f.read()
        assert (
            f"{db_port}:5984" in content
        ), "docker-compose.yaml does not contain the expected port."
    couchdb_ini_path = tmp_path / "database/couchdb.ini"
    with Path.open(couchdb_ini_path) as f:
        content = f.read()
        assert (
            ";port = 5985" in content
        ), "couchdb.ini does not contain the expected port."


def test_cli_init_frontend_host(tmp_path: Path):
    subprocess.run(
        [*HARDPY_COMMAND, tmp_path, "--frontend-host", frontend_host],
        check=True,
    )
    hardpy_toml_path = tmp_path / "hardpy.toml"
    with Path.open(hardpy_toml_path) as f:
        content = f.read()
        frontend_info = f'[frontend]\nhost = "{frontend_host}"\nport = 8000\n'
        assert (
            frontend_info in content
        ), "hardpy.toml does not contain the expected host."


def test_cli_init_frontend_port(tmp_path: Path):
    subprocess.run(
        [*HARDPY_COMMAND, tmp_path, "--frontend-port", frontend_port],
        check=True,
    )
    hardpy_toml_path = tmp_path / "hardpy.toml"
    with Path.open(hardpy_toml_path) as f:
        content = f.read()
        frontend_info = (
            f'[frontend]\nhost = "localhost"\nport = {frontend_port}\n\n'.format(
                frontend_port,
            )
        )
        assert (
            frontend_info in content
        ), "hardpy.toml does not contain the expected port."


def test_cli_init_socket_host(tmp_path: Path):
    subprocess.run(
        [*HARDPY_COMMAND, tmp_path, "--socket-host", socket_host],
        check=True,
    )
    hardpy_toml_path = tmp_path / "hardpy.toml"
    with Path.open(hardpy_toml_path) as f:
        content = f.read()
        socket_info = f"""[socket]
host = "{socket_host}"
port = 6525
"""
        assert socket_info in content, "hardpy.toml does not contain the expected host."


def test_cli_init_socket_port(tmp_path: Path):
    subprocess.run(
        [*HARDPY_COMMAND, tmp_path, "--socket-port", socket_port],
        check=True,
    )
    hardpy_toml_path = tmp_path / "hardpy.toml"
    with Path.open(hardpy_toml_path) as f:
        content = f.read()
        socket_info = f'[socket]\nhost = "localhost"\nport = {socket_port}\n'
        assert socket_info in content, "hardpy.toml does not contain the expected port."


# TODO(@RiByryn): cli hardpy run
