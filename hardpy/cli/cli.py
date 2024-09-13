# Copyright (c) 2024 Everypin
# GNU General Public License v3.0 (see LICENSE or https://www.gnu.org/licenses/gpl-3.0.txt)

import os
import sys
from pathlib import Path
from typing import Optional
from typing_extensions import Annotated

import typer
from uvicorn import run as uvicorn_run

from hardpy.cli.template import TemplateGenerator
from hardpy.common.config import ConfigManager

cli = typer.Typer(add_completion=False)
default_config = ConfigManager().get_config()


@cli.command()
def init(  # noqa: WPS211
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
    """Initialize HardPy tests directory.

    Args:
        tests_dir (str | None): Tests directory. Current directory + `tests` by default
        create_database (bool): Flag to create database
        database_user (str): Database user name
        database_password (str): Database password
        database_host (str): Database host
        database_port (int): Database port
        frontend_host (str): Panel operator host
        frontend_port (int): Panel operator port
        socket_host (str): Socket host
        socket_port (int): Socket port
    """
    _tests_dir = tests_dir if tests_dir else default_config.tests_dir
    ConfigManager().init_config(
        tests_dir=str(_tests_dir),
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
        print(f"hardpy.toml config by path {dir_path} not detected.")
        sys.exit()

    template = TemplateGenerator(config)

    files = {}

    if create_database:
        files[Path(dir_path / "docker-compose.yaml")] = template.docker_compose_yaml
        files[Path(dir_path / "database" / "couchdb.ini")] = template.couchdb_ini

    files[Path(dir_path / "pytest.ini")] = template.pytest_ini
    files[Path(dir_path / "test_1.py")] = template.test_1_py
    files[Path(dir_path / "conftest.py")] = template.conftest_py

    for key, value in files.items():
        template.create_file(key, value)

    print(f"HardPy project {dir_path.name} initialized successfully.")


@cli.command()
def run(tests_dir: Annotated[Optional[str], typer.Argument()] = None):
    """Run HardPy server.

    Args:
        tests_dir (Optional[str]): Test directory. Current directory by default
    """
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
