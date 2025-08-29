# Copyright (c) 2024 Everypin
# GNU General Public License v3.0 (see LICENSE or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import annotations

import os
import re
from enum import Enum
from pathlib import Path
from typing import Annotated
from urllib.parse import unquote

from fastapi import FastAPI, Query
from fastapi.staticfiles import StaticFiles

from hardpy.common.config import ConfigManager
from hardpy.pytest_hardpy.pytest_wrapper import PyTestWrapper

app = FastAPI()
app.state.pytest_wrp = PyTestWrapper()


class Status(str, Enum):
    """HardPy status.

    Statuses, that can be returned by HardPy API.
    """

    STOPPED = "stopped"
    STARTED = "started"
    COLLECTED = "collected"
    BUSY = "busy"
    READY = "ready"
    ERROR = "error"


@app.get("/api/hardpy_config")
def hardpy_config() -> dict:
    """Get config of HardPy.

    Returns:
        dict: HardPy config
    """
    return app.state.pytest_wrp.get_config()


@app.get("/api/start")
def start_pytest(args: Annotated[list[str] | None, Query()] = None) -> dict:
    """Start pytest subprocess.

    Args:
        args: List of arguments in key=value format

    Returns:
        dict[str, RunStatus]: run status
    """
    if args is None:
        args_dict = []
    else:
        args_dict = dict(arg.split("=", 1) for arg in args if "=" in arg)

    if app.state.pytest_wrp.start(start_args=args_dict):
        return {"status": Status.STARTED}
    return {"status": Status.BUSY}


@app.get("/api/stop")
def stop_pytest() -> dict:
    """Stop pytest subprocess.

    Returns:
        dict[str, RunStatus]: run status
    """
    if app.state.pytest_wrp.stop():
        return {"status": Status.STOPPED}
    return {"status": Status.READY}


@app.get("/api/collect")
def collect_pytest() -> dict:
    """Collect pytest subprocess.

    Returns:
        dict[str, RunStatus]: run status

    """
    if app.state.pytest_wrp.collect():
        return {"status": Status.COLLECTED}
    return {"status": Status.BUSY}


@app.get("/api/status")
def status() -> dict:
    """Get pytest subprocess status.

    Returns:
        dict[str, RunStatus]: run status
    """
    is_running = app.state.pytest_wrp.is_running()
    status = Status.BUSY if is_running else Status.READY
    return {"status": status}


@app.get("/api/couch")
def couch_connection() -> dict:
    """Get couchdb connection string.

    Returns:
        dict[str, str]: couchdb connection string
    """
    connection_url = ConfigManager().get_config().database.connection_url()

    return {
        "connection_str": connection_url,
    }


@app.post("/api/confirm_dialog_box/{dialog_box_output}")
def confirm_dialog_box(dialog_box_output: str) -> dict:
    """Confirm dialog box.

    Args:
        dialog_box_output (str): output data from dialog box.

    Returns:
        dict[str, RunStatus]: run status
    """
    hex_base = 16
    unquoted_string = unquote(dialog_box_output)
    decoded_string = re.sub(
        "%([0-9a-fA-F]{2})",
        lambda match: chr(int(match.group(1), hex_base)),
        unquoted_string,
    )

    if app.state.pytest_wrp.send_data(str(decoded_string)):
        return {"status": Status.BUSY}
    return {"status": Status.ERROR}


@app.post("/api/confirm_operator_msg/{is_msg_visible}")
def confirm_operator_msg(is_msg_visible: str) -> dict:
    """Confirm operator msg.

    Args:
        is_msg_visible (bool): is operator message is visible

    Returns:
        dict[str, RunStatus]: run status
    """
    if app.state.pytest_wrp.send_data(str(is_msg_visible)):
        return {"status": Status.BUSY}
    return {"status": Status.ERROR}


if "DEBUG_FRONTEND" not in os.environ:
    app.mount(
        "/",
        StaticFiles(
            directory=Path(__file__).parent / "frontend/dist",
            html=True,
        ),
        name="static",
    )
