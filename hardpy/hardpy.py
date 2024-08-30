# Copyright (c) 2024 Everypin
# GNU General Public License v3.0 (see LICENSE or https://www.gnu.org/licenses/gpl-3.0.txt)

import os
import sys
from pathlib import Path
from typing_extensions import Annotated
from typing import Optional

import typer
from uvicorn import run as uvicorn_run

from hardpy.config import ConfigManager
from hardpy.template import TemplateGenerator

cli = typer.Typer(add_completion=False)
default_config = ConfigManager().get_config()


@cli.command()
def init(
    tests_dir: Annotated[Optional[str], typer.Argument()] = None,
    create_database: bool = typer.Option(
        True,
        help="Create CouchDB database.",
    ),
    database_user: str = typer.Option(
        default_config.database.user,
        help="Specify a database user.",
    ),
    database_password: str = typer.Option(
        default_config.database.password,
        help="Specify a database user password.",
    ),
    database_host: str = typer.Option(
        default_config.database.host,
        help="Specify a database host.",
    ),
    database_port: int = typer.Option(
        default_config.database.port,
        help="Specify a database port.",
    ),
    frontend_host: str = typer.Option(
        default_config.frontend.host,
        help="Specify a frontend host.",
    ),
    frontend_port: int = typer.Option(
        default_config.frontend.port,
        help="Specify a frontend port.",
    ),
    socket_host: str = typer.Option(
        default_config.socket.host,
        help="Specify a socket host.",
    ),
    socket_port: int = typer.Option(
        default_config.socket.port,
        help="Specify a socket port.",
    ),
):
    """Initialize HardPy tests directory."""
    _tests_dir = tests_dir if tests_dir else default_config.tests_dir
    ConfigManager().init_config(
        tests_dir=_tests_dir,
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
    dir_path = Path(Path.cwd() / _tests_dir)
    os.makedirs(dir_path, exist_ok=True)

    if create_database:
        # create database directory
        os.makedirs(dir_path / "database", exist_ok=True)

    # create hardpy.toml
    ConfigManager().create_config(dir_path)
    config = ConfigManager().read_config(dir_path)
    if not config:
        sys.exit()

    template = TemplateGenerator(config)

    if create_database:
        # create docker-compose.yaml
        file_path = Path(dir_path / "docker-compose.yaml")
        with open(file_path, "w") as docker_compose_yaml:
            docker_compose_yaml.write(template.docker_compose_yaml)

    # create couchdb.ini
    file_path = Path(dir_path / "database" / "couchdb.ini")
    with open(file_path, "w") as couchdb_ini:
        couchdb_ini.write(template.couchdb_ini)

    # create pytest.ini
    file_path = Path(dir_path / "pytest.ini")
    with open(file_path, "w") as pytest_ini:
        pytest_ini.write(template.pytest_ini)

    # create test_1.py
    file_path = Path(dir_path / "test_1.py")
    with open(file_path, "w") as test_1_py:  # noqa: WPS114
        test_1_py.write(template.test_1_py)

    # create conftest.py
    file_path = Path(dir_path / "conftest.py")
    with open(file_path, "w") as conftest_py:
        conftest_py.write(template.conftest_py)

    print(f"HardPy project {dir_path.name} initialized successfully.")


@cli.command()
def run(tests_dir: Annotated[Optional[str], typer.Argument()] = None):
    """Run HardPy server."""
    dir_path = Path.cwd() / tests_dir if tests_dir else Path.cwd()
    config = ConfigManager().read_config(dir_path)

    if not config:
        print(f"Config at path {dir_path} not found.")
        sys.exit()

    print("\nLaunch the HardPy operator panel...")
    print(f"http://{config.frontend.host}:{config.frontend.port}\n")

    uvicorn_run(
        "hardpy.hardpy_panel.api:app",
        host=config.frontend.host,
        port=config.frontend.port,
        log_level="critical",
    )


if __name__ == "__main__":
    cli()
