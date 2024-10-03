# Expected configuration values from the provided instructions
import os
import shutil
import subprocess

asset_dir = "tests/test_cli/assets"


def test_cli_init():
    shutil.rmtree(asset_dir, ignore_errors=True)
    subprocess.run(["hardpy", "init", asset_dir], check=True)  # noqa: S603, S607


def test_cli_init_create_db():
    shutil.rmtree(asset_dir, ignore_errors=True)
    subprocess.run(["hardpy", "init", asset_dir, "--create-database"], check=True)  # noqa: S603, S607


def test_cli_init_no_create_db():
    shutil.rmtree(asset_dir, ignore_errors=True)
    subprocess.run(["hardpy", "init", asset_dir, "--no-create-database"], check=True)  # noqa: S603, S607


def test_cli_init_db_user():
    shutil.rmtree(asset_dir, ignore_errors=True)
    subprocess.run(  # noqa: S603
        ["hardpy", "init", asset_dir, "--database-user", "dev"],  # noqa: S607
        check=True,
    )
    docker_compose_path = os.path.join(asset_dir, "docker-compose.yaml")  # noqa: PTH118
    with open(docker_compose_path, "r") as f:  # noqa: PTH123, UP015
        content = f.read()
        assert (
            "COUCHDB_USER: dev" in content
        ), f"docker-compose.yaml does not contain the expected user."  # noqa: F541


def test_cli_init_db_password():
    shutil.rmtree(asset_dir, ignore_errors=True)
    subprocess.run(  # noqa: S603
        ["hardpy", "init", asset_dir, "--database-password", "dev"],  # noqa: S607
        check=True,
    )
    docker_compose_path = os.path.join(asset_dir, "docker-compose.yaml")  # noqa: PTH118
    with open(docker_compose_path, "r") as f:  # noqa: PTH123, UP015
        content = f.read()
        assert (
            "COUCHDB_PASSWORD: dev" in content
        ), f"docker-compose.yaml does not contain the expected password."  # noqa: F541


def test_cli_init_db_host():
    shutil.rmtree(asset_dir, ignore_errors=True)
    subprocess.run(  # noqa: S603
        ["hardpy", "init", asset_dir, "--database-host", "localhost"],  # noqa: S607
        check=True,
    )
    couchdb_ini_path = os.path.join(asset_dir, "database/couchdb.ini")  # noqa: PTH118
    with open(couchdb_ini_path, "r") as f:  # noqa: PTH123, UP015
        content = f.read()
        assert (
            ";bind_address = localhost" in content
        ), f"couchdb.ini does not contain the expected host."  # noqa: F541


def test_cli_init_db_port():
    shutil.rmtree(asset_dir, ignore_errors=True)
    subprocess.run(  # noqa: S603
        ["hardpy", "init", asset_dir, "--database-port", "5984"],  # noqa: S607
        check=True,
    )
    docker_compose_path = os.path.join(asset_dir, "docker-compose.yaml")  # noqa: PTH118
    with open(docker_compose_path, "r") as f:  # noqa: PTH123, UP015
        content = f.read()
        assert (
            "5984:5984" in content
        ), f"docker-compose.yaml does not contain the expected port."  # noqa: F541
    couchdb_ini_path = os.path.join(asset_dir, "database/couchdb.ini")  # noqa: PTH118
    with open(couchdb_ini_path, "r") as f:  # noqa: PTH123, UP015
        content = f.read()
        assert (
            ";port = 5984" in content
        ), f"couchdb.ini does not contain the expected port."  # noqa: F541


def test_cli_init_frontend_host():
    shutil.rmtree(asset_dir, ignore_errors=True)
    subprocess.run(  # noqa: S603
        ["hardpy", "init", asset_dir, "--frontend-host", "localhost"],  # noqa: S607
        check=True,
    )
    hardpy_toml_path = os.path.join(asset_dir, "hardpy.toml")  # noqa: PTH118
    with open(hardpy_toml_path, "r") as f:  # noqa: PTH123, UP015
        content = f.read()
        assert (
            'host = "localhost"' in content
        ), f"hardpy.toml does not contain the expected host."  # noqa: F541


def test_cli_init_frontend_port():
    shutil.rmtree(asset_dir, ignore_errors=True)
    subprocess.run(  # noqa: S603
        ["hardpy", "init", asset_dir, "--frontend-port", "8000"],  # noqa: S607
        check=True,
    )
    hardpy_toml_path = os.path.join(asset_dir, "hardpy.toml")  # noqa: PTH118
    with open(hardpy_toml_path, "r") as f:  # noqa: PTH123, UP015
        content = f.read()
        assert (
            "port = 8000" in content
        ), f"hardpy.toml does not contain the expected port."  # noqa: F541


def test_cli_init_socket_host():
    shutil.rmtree(asset_dir, ignore_errors=True)
    subprocess.run(  # noqa: S603
        ["hardpy", "init", asset_dir, "--socket-host", "localhost"],  # noqa: S607
        check=True,
    )
    hardpy_toml_path = os.path.join(asset_dir, "hardpy.toml")  # noqa: PTH118
    with open(hardpy_toml_path, "r") as f:  # noqa: PTH123, UP015
        content = f.read()
        assert (
            'host = "localhost"' in content
        ), f"hardpy.toml does not contain the expected host."  # noqa: F541


def test_cli_init_socket_port():
    shutil.rmtree(asset_dir, ignore_errors=True)
    subprocess.run(  # noqa: S603
        ["hardpy", "init", asset_dir, "--socket-port", "6525"],  # noqa: S607
        check=True,
    )
    hardpy_toml_path = os.path.join(asset_dir, "hardpy.toml")  # noqa: PTH118
    with open(hardpy_toml_path, "r") as f:  # noqa: PTH123, UP015
        content = f.read()
        assert (
            "port = 6525" in content
        ), f"hardpy.toml does not contain the expected port."  # noqa: F541


# def test_cli_run():
#     subprocess.run(["hardpy", "run", asset_dir], check=True)  # noqa: ERA001


def test_cli_clean():
    shutil.rmtree(asset_dir, ignore_errors=True)
