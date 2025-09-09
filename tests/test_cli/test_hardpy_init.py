import os
import subprocess
from pathlib import Path

HARDPY_COMMAND = ["hardpy", "init"]

db_no_default_user = "dev1"
db_no_default_password = "dev1"
db_no_default_host = "localhost1"
db_no_default_port = "5985"
db_no_default_doc_id = "current1"
frontend_no_default_host = "localhost1"
frontend_no_default_port = "8001"
stand_cloud_no_default_addr = "everypin1.standcloud.localhost"

db_default_port = "5984"
frontend_default_host = "localhost"
frontend_default_port = "8000"
frontend_default_language = "en"
db_default_doc_id = f"{frontend_default_host}_{frontend_default_port}"


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


def test_cli_init_db_doc_id(tmp_path: Path):
    subprocess.run(
        [*HARDPY_COMMAND, tmp_path, "--database-doc-id", db_no_default_doc_id],
        check=True,
    )
    hardpy_toml_path = tmp_path / "hardpy.toml"
    with Path.open(hardpy_toml_path) as f:
        content = f.read()

        database_info = (
            f"[database]\n"
            f'user = "dev"\n'
            f'password = "dev"\n'
            f'host = "localhost"\n'
            f"port = 5984\n"
            f'doc_id = "{db_no_default_doc_id}"\n'
        ).format(db_no_default_doc_id)
        assert (
            database_info in content
        ), "hardpy.toml does not contain the expected document id."


def test_cli_init_no_db_doc_id(tmp_path: Path):
    subprocess.run([*HARDPY_COMMAND, tmp_path], check=True)
    hardpy_toml_path = tmp_path / "hardpy.toml"
    with Path.open(hardpy_toml_path) as f:
        content = f.read()
        assert (
            f'doc_id = "{db_default_doc_id}"' in content
        ), "hardpy.toml contain not correct doc_id."


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
            f"port = {frontend_no_default_port}\n"
        ).format(frontend_no_default_port)
        assert (
            frontend_info in content
        ), "hardpy.toml does not contain the expected port."


def test_cli_init_frontend_language(tmp_path: Path):
    subprocess.run(
        [*HARDPY_COMMAND, tmp_path],
        check=True,
    )
    hardpy_toml_path = tmp_path / "hardpy.toml"
    with Path.open(hardpy_toml_path) as f:
        content = f.read()
        frontend_info = (
            f"[frontend]\n"
            f'host = "localhost"\n'
            f"port = 8000\n"
            f'language = "{frontend_default_language}"\n'
        )
        assert (
            frontend_info in content
        ), "hardpy.toml does not contain the expected language."


def test_cli_init_stand_cloud_addr(tmp_path: Path):
    subprocess.run(
        [*HARDPY_COMMAND, tmp_path, "--sc-address", stand_cloud_no_default_addr],
        check=True,
    )
    hardpy_toml_path = tmp_path / "hardpy.toml"
    with Path.open(hardpy_toml_path) as f:
        content = f.read()
        stand_cloud_info = f"""[stand_cloud]
address = "{stand_cloud_no_default_addr}"
"""
        assert_msg = "hardpy.toml does not contain the expected host."
        assert stand_cloud_info in content, assert_msg
