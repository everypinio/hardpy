# Copyright (c) 2024 Everypin
# GNU General Public License v3.0 (see LICENSE or https://www.gnu.org/licenses/gpl-3.0.txt)

import sys
from argparse import ArgumentParser
from pathlib import Path

from uvicorn import run as uvicorn_run

from hardpy.pytest_hardpy.utils import ConfigData


def run():
    """Start server for frontend."""
    config = ConfigData()
    parser = ArgumentParser(description="Usage: hardpy-panel [OPTION]... [PATH]")
    # fmt: off
    parser.add_argument("-dbu", "--db_user", default=config.db_user, help="database user")  # noqa: E501
    parser.add_argument("-dbpw", "--db_pswd", default=config.db_pswd, help="database user password")  # noqa: E501
    parser.add_argument("-dbp", "--db_port", type=int, default=config.db_port, help="database port number")  # noqa: E501
    parser.add_argument("-dbh", "--db_host", type=str, default=config.db_host, help="database hostname")  # noqa: E501
    parser.add_argument("-wh", "--web_host", type=str, default=config.web_host, help="web operator panel hostname")  # noqa: E501
    parser.add_argument("-wp", "--web_port", type=str, default=config.web_port, help="web operator panel port")  # noqa: E501
    parser.add_argument("path", type=str, nargs='?', help="path to test directory")
    # fmt: on

    args = parser.parse_args()

    config.db_user = args.db_user
    config.db_pswd = args.db_pswd
    config.db_port = args.db_port
    config.db_host = args.db_host
    config.web_host = args.web_host
    config.web_port = args.web_port

    path = Path(args.path) if args.path else Path.cwd()

    config.tests_dir = path

    if not config.tests_dir.exists():
        print(f"Directory not found: {path}")
        sys.exit()

    uvicorn_run(
        "hardpy.hardpy_panel.api:app",
        host=config.web_host,
        port=config.web_port,
        log_level="critical",
    )


run()
