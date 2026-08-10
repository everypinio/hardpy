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

from jig import __version__ as jig_version
from jig.cli.template import TemplateGenerator
from jig.common import log_config
from jig.common.config import ConfigManager, JigConfig
from jig.common.stand_cloud import (
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
default_config = JigConfig()


def version_callback(value: bool) -> None:
    """Show the Jig version and exit."""
    if value:
        print(jig_version)
        raise typer.Exit(0)


@cli.callback()
def main(  # noqa: D103
    version_flag: Optional[bool] = typer.Option(
        None,
        "--version",
        "-v",
        callback=version_callback,
        is_eager=True,
        help="Show the Jig version and exit.",
    ),
) -> None:
    pass


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
        default=default_config.stand_cloud.address,
        help="Specify a StandCloud address.",
    ),
    sc_connection_only: bool = typer.Option(
        default=default_config.stand_cloud.connection_only,
        help="Check StandCloud service availability before start.",
    ),
    sc_autosync: bool = typer.Option(
        default=default_config.stand_cloud.autosync,
        help="Enable StandCloud auto syncronization.",
    ),
    sc_api_key: str | None = typer.Option(
        default=default_config.stand_cloud.api_key,
        help="Specify a StandCloud API key.",
    ),
    storage_type: str = typer.Option(
        default=default_config.database.storage_type.value,
        help="Specify a storage type.",
    ),
) -> None:
    """Initialize Jig tests directory.

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
        sc_autosync (bool): Flag to enable StandCloud auto syncronization
        sc_api_key (str | None): StandCloud API key
        storage_type (str): Storage type, "json" or "couchdb", "couchdb" by default
    """
    dir_path = Path(Path.cwd() / tests_dir if tests_dir else "tests")
    config_manager = ConfigManager()
    config_manager.init_config(
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
        sc_autosync=sc_autosync,
        sc_api_key=sc_api_key,
        storage_type=storage_type,
    )
    # create tests directory
    Path.mkdir(dir_path, exist_ok=True, parents=True)

    if create_database:
        # create database directory
        Path.mkdir(dir_path / "database", exist_ok=True, parents=True)

    # create jig.toml
    config_manager.create_config(dir_path)

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

    print(f"Jig project {dir_path.name} initialized successfully.")


@cli.command()
def run(
    tests_dir: Annotated[Optional[str], typer.Argument()] = None,
    verbose: bool = typer.Option(
        default=False,
        help="Print test collection output and Jig logs.",
    ),
) -> None:
    """Run Jig server.

    Args:
        tests_dir (Optional[str]): Test directory. Current directory by default
        verbose (bool): Print test collection output and Jig logs
    """
    log_level = log_config.resolve_level(is_verbose=verbose)
    log_config.configure(log_level)

    config = _get_config(tests_dir)
    _validate_config(config)

    print("\nLaunch the Jig operator panel...")

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        if s.connect_ex((config.frontend.host, config.frontend.port)) == 0:
            print(f"Error: Specified port {config.frontend.port} is already in use")
            sys.exit(1)

    url = typer.style(
        f"http://{config.frontend.host}:{config.frontend.port}",
        fg=typer.colors.BRIGHT_CYAN,
        bold=True,
    )
    typer.echo(f"🚀 Ready! Open {url} in your browser and let the testing begin.\n")

    try:
        uvicorn_run(
            "jig.jig_panel.api:app",
            host=config.frontend.host,
            port=config.frontend.port,
            log_level=log_config.uvicorn_level(log_level),
        )
    except RuntimeError as exc:
        print(f"Jig server cannot be started: {exc}")
        sys.exit()


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
    """Start Jig tests.

    Args:
        ctx: Typer context for accessing arguments from other sources
        tests_dir (Optional[str]): Test directory. Current directory by default
        arg (list[str]): Dynamic arguments for test execution
    """
    context_args = getattr(ctx, "jig_args", [])
    all_args = arg + context_args

    config = _get_config(tests_dir, validate=True)
    query_args = "&".join([f"args={urllib.parse.quote(a)}" for a in all_args])
    url = f"http://{config.frontend.host}:{config.frontend.port}/api/start?{query_args}"
    _request_jig(url)


@cli.command()
def stop(tests_dir: Annotated[Optional[str], typer.Argument()] = None) -> None:
    """Stop Jig tests.

    Args:
        tests_dir (Optional[str]): Test directory. Current directory by default
    """
    config = _get_config(tests_dir, validate=True)
    url = f"http://{config.frontend.host}:{config.frontend.port}/api/stop"
    _request_jig(url)


@cli.command()
def status(tests_dir: Annotated[Optional[str], typer.Argument()] = None) -> None:
    """Get Jig test launch status.

    Args:
        tests_dir (Optional[str]): Test directory. Current directory by default
    """
    config = _get_config(tests_dir, validate=True)
    url = f"http://{config.frontend.host}:{config.frontend.port}/api/status"
    _request_jig(url)


@cli.command()
def sc_login(
    address: Annotated[str, typer.Argument()],
    check: bool = typer.Option(
        False,
        help="Check StandCloud connection.",
    ),
) -> None:
    """Login Jig in StandCloud.

    The command opens an authentication and authorization portal of StandCloud
    where you will be requested for your credentials and consents to authorize
    Jig to upload test reports from your identity.

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
    """Logout Jig from StandCloud account.

    Args:
        address (str): StandCloud address
    """
    if auth_logout(address):
        print(f"Jig logout success from {address}")
    else:
        print(f"Jig logout failed from {address}")


@cli.command()
def sc_sync(
    tests_dir: Annotated[Optional[str], typer.Argument()] = None,
    timeout: int = typer.Option(
        default="60",
        help="Specify a synchronization timeout.",
    ),
) -> str:
    """Synchronize Jig tests with StandCloud.

    Args:
        tests_dir (Optional[str]): Test directory. Current directory by default
        timeout (int): Synchronization timeout
    """
    try:
        _timeout = int(timeout)
    except ValueError:
        print("Timeout must be a number.")
        sys.exit()
    config = _get_config(tests_dir, validate=True)
    url = f"http://{config.frontend.host}:{config.frontend.port}/api/stand_cloud_sync"
    return _request_jig(url, timeout=_timeout)


def _get_config(tests_dir: str | None = None, validate: bool = False) -> JigConfig:
    dir_path = Path.cwd() / tests_dir if tests_dir else Path.cwd()
    config_manager = ConfigManager()
    config = config_manager.read_config(dir_path)

    if not config:
        print(f"Config at path {dir_path} not found.")
        sys.exit()

    if validate:
        _validate_running_config(config, dir_path)

    return config


def _validate_running_config(config: JigConfig, tests_dir: str) -> None:
    url = f"http://{config.frontend.host}:{config.frontend.port}/api/jig_config"
    error_msg = f"Jig in directory {tests_dir} does not run."
    try:
        response = requests.get(url, timeout=2)
    except Exception:
        print(error_msg)
        sys.exit()

    running_config: dict = response.json()
    if config.model_dump() != running_config:
        print(error_msg)
        sys.exit()


def _validate_config(config: JigConfig) -> None:
    if config.stand_cloud.autosync:
        if config.stand_cloud.autosync_timeout < 1:
            print("StandCloud autosync timeout must be greater than 0.")
            sys.exit()
        if not config.stand_cloud.api_key:
            print("StandCloud API key is empty.")
            sys.exit()


def _request_jig(url: str, timeout: int = 5) -> str:
    try:
        response = requests.get(url, timeout=timeout)
    except Exception:
        print("Jig operator panel is not running.")
        sys.exit()
    try:
        status: dict = response.json().get("status", "ERROR")
    except ValueError:
        print(f"Jig internal error: {response}.")
        sys.exit()
    print(f"Jig status: {status}.")
    return status


if __name__ == "__main__":
    cli()
