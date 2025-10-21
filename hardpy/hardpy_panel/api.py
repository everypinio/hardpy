# Copyright (c) 2024 Everypin
# GNU General Public License v3.0 (see LICENSE or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import annotations

import json
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
    config_manager = ConfigManager()

    return {
        "connection_str": config_manager.config.database.url,
    }


@app.get("/api/database_document_id")
def database_document_id() -> dict:
    """Get couchdb syncronized document name.

    Returns:
        dict[str, str]: couchdb connection string
    """
    config_manager = ConfigManager()
    return {"document_id": config_manager.config.database.doc_id}


@app.post("/api/confirm_dialog_box")
def confirm_dialog_box(payload: dict) -> dict:
    """Confirm dialog box with unified JSON structure.

    Args:
        payload: dict with 'result' (pass/fail), 'data' (widget data), and 'has_pass_fail' flag

    Returns:
        dict[str, RunStatus]: run status
    """  # noqa: E501
    # String constants
    RESULT_KEY = "result"  # noqa: N806
    DATA_KEY = "data"  # noqa: N806
    HAS_PASS_FAIL_KEY = "has_pass_fail"  # noqa: N806, S105
    STATUS_KEY = "status"  # noqa: N806
    EMPTY_STRING = ""  # noqa: N806

    # Numeric constants
    HEX_BASE = 16  # noqa: N806
    HEX_PATTERN = r"%([0-9a-fA-F]{2})"  # noqa: N806

    result = payload.get(RESULT_KEY, EMPTY_STRING)
    widget_data = payload.get(DATA_KEY, EMPTY_STRING)
    has_pass_fail = payload.get(HAS_PASS_FAIL_KEY, False)

    unquoted_string = unquote(widget_data)
    decoded_string = re.sub(
        HEX_PATTERN,
        lambda match: chr(int(match.group(1), HEX_BASE)),
        unquoted_string,
    )

    # Create JSON structure for all dialog types
    dialog_result = {
        HAS_PASS_FAIL_KEY: has_pass_fail,
        RESULT_KEY: result,
        DATA_KEY: decoded_string,
    }

    # Convert to JSON string for transmission
    combined_data = json.dumps(dialog_result)

    if app.state.pytest_wrp.send_data(combined_data):
        return {STATUS_KEY: Status.BUSY}
    return {STATUS_KEY: Status.ERROR}


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
