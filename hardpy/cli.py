# Copyright (c) 2024 Everypin
# GNU General Public License v3.0 (see LICENSE or https://www.gnu.org/licenses/gpl-3.0.txt)


import os
from pathlib import Path

import typer

from hardpy.config import ConfigManager
from hardpy.file_generator import FileGenerator

cli = typer.Typer(add_completion=False)
default_config = ConfigManager.dict_config()


@cli.command()
def init(
    tests_dir: str = typer.Option(
        default_config["tests_dir"], help="Specify a tests directory."
    ),
    database_user: str = typer.Option(
        default_config["database"]["user"], help="Specify a database user."
    ),
    database_password: str = typer.Option(
        default_config["database"]["password"],
        help="Specify a database user password.",
    ),
    database_host: str = typer.Option(
        default_config["database"]["host"], help="Specify a database host."
    ),
    database_port: int = typer.Option(
        default_config["database"]["port"], help="Specify a database port."
    ),
    frontend_host: str = typer.Option(
        default_config["frontend"]["host"], help="Specify a frontend host."
    ),
    frontend_port: int = typer.Option(
        default_config["frontend"]["port"], help="Specify a frontend port."
    ),
    socket_host: str = typer.Option(
        default_config["socket"]["host"], help="Specify a socket host."
    ),
    socket_port: int = typer.Option(
        default_config["socket"]["port"], help="Specify a socket port."
    ),
):
    """Initialize HardPy."""
    ConfigManager.init_config(
        tests_dir=tests_dir,
        database_user=database_user,
        database_password=database_password,
        database_host=database_host,
        database_port=database_port,
        frontend_host=frontend_host,
        frontend_port=frontend_port,
        socket_host=socket_host,
        socket_port=socket_port,
    )
    # create tests directory
    dir_path = Path(Path.cwd() / tests_dir)
    os.makedirs(dir_path, exist_ok=True)

    # create database directory
    os.makedirs(dir_path / "database", exist_ok=True)

    # create hardpy_config.toml
    ConfigManager.create_config(dir_path)

    fg = FileGenerator()

    # create docker-compose.yaml
    file_path = Path(dir_path / "docker-compose.yaml")
    with open(file_path, "w") as docker_compose_yaml:
        docker_compose_yaml.write(fg.docker_compose_yaml)

    # create couchdb.ini
    file_path = Path(dir_path / "database" / "couchdb.ini")
    with open(file_path, "w") as couchdb_ini:
        couchdb_ini.write(fg.couchdb_ini)

    # create pytest.ini
    file_path = Path(dir_path / "pytest.ini")
    with open(file_path, "w") as pytest_ini:
        pytest_ini.write(fg.pytest_ini)

    # create test_1.py
    file_path = Path(dir_path / "test_1.py")
    with open(file_path, "w") as test_1_py:  # noqa: WPS114
        test_1_py.write(fg.test_1_py)

    # create conftest.py
    file_path = Path(dir_path / "conftest.py")
    with open(file_path, "w") as conftest_py:
        conftest_py.write(fg.conftest_py)
