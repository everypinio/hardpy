# Copyright (c) 2024 Everypin
# GNU General Public License v3.0 (see LICENSE or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import annotations

import sys
from pathlib import Path
from typing import Annotated, Optional

import typer
from uvicorn import run as uvicorn_run

from hardpy.cli.template import TemplateGenerator
from hardpy.common.config import ConfigManager
from hardpy.common.stand_cloud import (
    StandCloudConnector,
    StandCloudError,
    login as auth_login,
    logout as auth_logout,
)

if __debug__:
    from urllib3 import disable_warnings
    from urllib3.exceptions import InsecureRequestWarning

    disable_warnings(InsecureRequestWarning)

cli = typer.Typer(add_completion=False)
default_config = ConfigManager().get_config()


@cli.command()
def init(  # noqa: PLR0913
    tests_dir: Annotated[Optional[str], typer.Argument()] = None,
    create_database: bool = typer.Option(
        default=True,
        help="Create CouchDB database.",
    ),
    database_user: str = typer.Option(
        default=default_config.database.user,
        help="Specify a database user.",
    ),
    database_password: str = typer.Option(
        default=default_config.database.password,
        help="Specify a database user password.",
    ),
    database_host: str = typer.Option(
        default=default_config.database.host,
        help="Specify a database host.",
    ),
    database_port: int = typer.Option(
        default=default_config.database.port,
        help="Specify a database port.",
    ),
    frontend_host: str = typer.Option(
        default=default_config.frontend.host,
        help="Specify a frontend host.",
    ),
    frontend_port: int = typer.Option(
        default=default_config.frontend.port,
        help="Specify a frontend port.",
    ),
    socket_host: str = typer.Option(
        default=default_config.socket.host,
        help="Specify a socket host.",
    ),
    socket_port: int = typer.Option(
        default=default_config.socket.port,
        help="Specify a socket port.",
    ),
    sc_address: str = typer.Option(
        default="",
        help="Specify a StandCloud address.",
    ),
    sc_connection_only: bool = typer.Option(
        default=False,
        help="Check StandCloud service availability before start.",
    ),
) -> None:
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
        sc_address (str): StandCloud address
        sc_connection_only (bool): Flag to check StandCloud service availability
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
        sc_address=sc_address,
        sc_connection_only=sc_connection_only,
    )
    # create tests directory
    dir_path = Path(Path.cwd() / _tests_dir)
    Path.mkdir(dir_path, exist_ok=True, parents=True)

    if create_database:
        # create database directory
        Path.mkdir(dir_path / "database", exist_ok=True, parents=True)

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
def run(tests_dir: Annotated[Optional[str], typer.Argument()] = None) -> None:
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


@cli.command()
def sc_login(
    address: Annotated[str, typer.Argument()],
    check: bool = typer.Option(
        False,
        help="Check StandCloud connection.",
    ),
) -> None:
    """Login HardPy in StandCloud.

    The command opens an authentication and authorization portal of StandCloud
    where you will be requested for your credentials and consents to authorize
    HardPy to upload test reports from your identity.

    Args:
        address (str): StandCloud address
        check (bool): Check StandCloud connection
    """
    if check:
        try:
            sc_connector = StandCloudConnector(address)
        except StandCloudError as exc:
            print(str(exc))
            sys.exit()
        try:
            sc_connector.healthcheck()
        except StandCloudError:
            print("StandCloud connection failed")
            sys.exit()
        print("StandCloud connection success")
    else:
        auth_login(address)


@cli.command()
def sc_logout() -> None:
    """Logout HardPy from all StandCloud accounts."""
    if auth_logout():
        print("HardPy logout success")
    else:
        print("HardPy logout failed")


if __name__ == "__main__":
    cli()
