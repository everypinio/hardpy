# Copyright (c) 2024 Everypin
# GNU General Public License v3.0 (see LICENSE or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import annotations

import socket
import sys
import urllib
from pathlib import Path
from typing import Annotated, Optional

import requests
import typer
from uvicorn import run as uvicorn_run

from hardpy.cli.template import TemplateGenerator
from hardpy.common.config import ConfigManager, HardpyConfig
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
    tests_name: str = typer.Option(
        default="",
        help="Specify a tests suite name.",
    ),
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
        tests_name (str): Tests suite name, "Tests" by default
        create_database (bool): Flag to create database
        database_user (str): Database user name
        database_password (str): Database password
        database_host (str): Database host
        database_port (int): Database port
        frontend_host (str): Panel operator host
        frontend_port (int): Panel operator port
        frontend_language (str): Panel operator language
        sc_address (str): StandCloud address
        sc_connection_only (bool): Flag to check StandCloud service availability
    """
    dir_path = Path(Path.cwd() / tests_dir if tests_dir else "tests")
    ConfigManager().init_config(
        tests_name=tests_name if tests_name else dir_path.name,
        database_user=database_user,
        database_password=database_password,
        database_host=database_host,
        database_port=database_port,
        frontend_host=frontend_host,
        frontend_port=frontend_port,
        frontend_language=default_config.frontend.language,
        sc_address=sc_address,
        sc_connection_only=sc_connection_only,
    )
    # create tests directory
    Path.mkdir(dir_path, exist_ok=True, parents=True)

    if create_database:
        # create database directory
        Path.mkdir(dir_path / "database", exist_ok=True, parents=True)

    # create hardpy.toml
    ConfigManager().create_config(dir_path)

    config = _get_config(dir_path)
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
    config = _get_config(tests_dir)

    print("\nLaunch the HardPy operator panel...")

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        if s.connect_ex((config.frontend.host, config.frontend.port)) == 0:
            print(f"Error: Specified port {config.frontend.port} is already in use")
            sys.exit(1)

    print(f"http://{config.frontend.host}:{config.frontend.port}\n")

    uvicorn_run(
        "hardpy.hardpy_panel.api:app",
        host=config.frontend.host,
        port=config.frontend.port,
        log_level="critical",
    )


@cli.command()
def start(
    ctx: typer.Context,
    tests_dir: Annotated[Optional[str], typer.Argument()] = None,
    arg: list[str] = typer.Option(  # noqa: B008
        [],
        "--arg",
        "-a",
        help="Dynamic start arguments (format: key=value)",
    ),
) -> None:
    """Start HardPy tests.

    Args:
        ctx: Typer context for accessing arguments from other sources
        tests_dir (Optional[str]): Test directory. Current directory by default
        arg (list[str]): Dynamic arguments for test execution
    """
    context_args = getattr(ctx, "hardpy_args", [])
    all_args = arg + context_args

    config = _get_config(tests_dir, validate=True)
    query_args = "&".join([f"args={urllib.parse.quote(a)}" for a in all_args])
    url = f"http://{config.frontend.host}:{config.frontend.port}/api/start?{query_args}"
    _request_hardpy(url)


@cli.command()
def stop(tests_dir: Annotated[Optional[str], typer.Argument()] = None) -> None:
    """Stop HardPy tests.

    Args:
        tests_dir (Optional[str]): Test directory. Current directory by default
    """
    config = _get_config(tests_dir, validate=True)
    url = f"http://{config.frontend.host}:{config.frontend.port}/api/stop"
    _request_hardpy(url)


@cli.command()
def status(tests_dir: Annotated[Optional[str], typer.Argument()] = None) -> None:
    """Get HardPy test launch status.

    Args:
        tests_dir (Optional[str]): Test directory. Current directory by default
    """
    config = _get_config(tests_dir, validate=True)
    url = f"http://{config.frontend.host}:{config.frontend.port}/api/status"
    _request_hardpy(url)


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
    try:
        sc_connector = StandCloudConnector(address)
    except StandCloudError as exc:
        print(str(exc))
        sys.exit()

    if check:
        try:
            sc_connector.healthcheck()
        except StandCloudError:
            print("StandCloud connection failed")
            sys.exit()
        print("StandCloud connection success")
    else:
        auth_login(sc_connector)


@cli.command()
def sc_logout(address: Annotated[str, typer.Argument()]) -> None:
    """Logout HardPy from StandCloud account.

    Args:
        address (str): StandCloud address
    """
    if auth_logout(address):
        print(f"HardPy logout success from {address}")
    else:
        print(f"HardPy logout failed from {address}")


def _get_config(tests_dir: str | None = None, validate: bool = False) -> HardpyConfig:
    dir_path = Path.cwd() / tests_dir if tests_dir else Path.cwd()
    config = ConfigManager().read_config(dir_path)

    if not config:
        print(f"Config at path {dir_path} not found.")
        sys.exit()

    if validate:
        _validate_config(config, dir_path)

    return config


def _validate_config(config: HardpyConfig, tests_dir: str) -> None:
    url = f"http://{config.frontend.host}:{config.frontend.port}/api/hardpy_config"
    error_msg = f"HardPy in directory {tests_dir} does not run."
    try:
        response = requests.get(url, timeout=2)
    except Exception:
        print(error_msg)
        sys.exit()

    running_config: dict = response.json()
    if config.model_dump() != running_config:
        print(error_msg)
        sys.exit()


def _request_hardpy(url: str) -> None:
    try:
        response = requests.get(url, timeout=2)
    except Exception:
        print("HardPy operator panel is not running.")
        sys.exit()
    try:
        status: dict = response.json().get("status", "ERROR")
    except ValueError:
        print(f"Hardpy internal error: {response}.")
        sys.exit()
    print(f"HardPy status: {status}.")


if __name__ == "__main__":
    cli()
