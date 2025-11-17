# Copyright (c) 2024 Everypin
# GNU General Public License v3.0 (see LICENSE or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import annotations

import json
import os
import re
import secrets
import time
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

# Store authentication state with session data
app.state.authenticated_users = {}


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
    UNAUTHORIZED = "unauthorized"


def _is_authenticated(session_id: str | None = None) -> bool:
    """Check if user is authenticated."""
    config_manager = ConfigManager()
    if not config_manager.config.frontend.auth.enabled:
        return True

    if not session_id:
        return False

    # Check if session exists and is not expired
    if session_id in app.state.authenticated_users:
        session_data = app.state.authenticated_users[session_id]
        timeout_minutes = config_manager.config.frontend.auth.timeout_minutes
        minutes_in_ms = timeout_minutes * 60 * 1000

        # Check if session expired
        if (time.time() * 1000 - session_data["last_activity"]) > minutes_in_ms:
            # Remove expired session
            app.state.authenticated_users.pop(session_id, None)
            return False

        # Update last activity
        session_data["last_activity"] = time.time() * 1000
        return True

    return False


@app.get("/api/hardpy_config")
def hardpy_config() -> dict:
    """Get config of HardPy.

    Returns:
        dict: HardPy config
    """
    return app.state.pytest_wrp.get_config()


@app.post("/api/auth/login")
async def login_user(credentials: dict) -> dict:
    """Authenticate user with username and password.

    Args:
        credentials: dict with 'username' and 'password'

    Returns:
        dict: authentication result with user info or error
    """
    config_manager = ConfigManager()
    if not config_manager.config.frontend.auth.enabled:
        return {"authenticated": True, "user": {"name": "guest", "role": "operator"}}

    username = credentials.get("username", "").strip()
    password = credentials.get("password", "").strip()

    valid_users = {"test": "test"}

    if username in valid_users and valid_users[username] == password:
        # Generate secure session ID
        session_id = secrets.token_urlsafe(32)
        current_time = time.time() * 1000

        app.state.authenticated_users[session_id] = {
            "username": username,
            "login_time": current_time,
            "last_activity": current_time,
        }

        return {
            "authenticated": True,
            "user": {"name": username, "role": "operator"},
            "session_id": session_id,
        }

    return {"authenticated": False, "error": "Invalid username or password"}


@app.post("/api/auth/validate_session")
async def validate_session(session_data: dict) -> dict:
    """Validate user session.

    Args:
        session_data: dict with user session information

    Returns:
        dict: validation result
    """
    config_manager = ConfigManager()
    if not config_manager.config.frontend.auth.enabled:
        return {"valid": True}

    session_id = session_data.get("session_id")

    if not session_id or not _is_authenticated(session_id):
        return {"valid": False, "error": "Invalid or expired session"}

    # Session is valid, return user info
    session_info = app.state.authenticated_users.get(session_id, {})
    return {
        "valid": True,
        "user": {"name": session_info.get("username", ""), "role": "operator"},
    }


@app.post("/api/auth/logout")
async def logout_user(session_data: dict) -> dict:
    """Logout user and invalidate session.

    Args:
        session_data: dict with session information

    Returns:
        dict: logout result
    """
    session_id = session_data.get("session_id")
    if session_id:
        app.state.authenticated_users.pop(session_id, None)

    return {"success": True}


@app.get("/api/start")
def start_pytest(
    args: Annotated[list[str] | None, Query()] = None,
    session_id: Annotated[str | None, Query()] = None,
) -> dict:
    """Start pytest subprocess.

    Args:
        args: List of arguments in key=value format
        session_id: User session ID for authentication

    Returns:
        dict[str, RunStatus]: run status
    """
    if not _is_authenticated(session_id):
        return {"status": Status.UNAUTHORIZED}

    if args is None:
        args_dict = []
    else:
        args_dict = dict(arg.split("=", 1) for arg in args if "=" in arg)

    if app.state.pytest_wrp.start(start_args=args_dict):
        return {"status": Status.STARTED}
    return {"status": Status.BUSY}


@app.get("/api/stop")
def stop_pytest(session_id: Annotated[str | None, Query()] = None) -> dict:
    """Stop pytest subprocess.

    Args:
        session_id: User session ID for authentication

    Returns:
        dict[str, RunStatus]: run status
    """
    if not _is_authenticated(session_id):
        return {"status": Status.UNAUTHORIZED}

    if app.state.pytest_wrp.stop():
        return {"status": Status.STOPPED}
    return {"status": Status.READY}


@app.get("/api/collect")
def collect_pytest(session_id: Annotated[str | None, Query()] = None) -> dict:
    """Collect pytest subprocess.

    Args:
        session_id: User session ID for authentication

    Returns:
        dict[str, RunStatus]: run status
    """
    if not _is_authenticated(session_id):
        return {"status": Status.UNAUTHORIZED}

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
def confirm_dialog_box(
    dbx_data: dict, session_id: Annotated[str | None, Query()] = None
) -> dict:
    """Confirm dialog box with unified JSON structure.

    Args:
        dbx_data: dict with 'result' (pass/fail/confirm) and 'data' (widget data)
        session_id: User session ID for authentication

    Returns:
        dict[str, RunStatus]: run status
    """
    if not _is_authenticated(session_id):
        return {"status": Status.UNAUTHORIZED}

    RESULT_KEY = "result"  # noqa: N806
    DATA_KEY = "data"  # noqa: N806
    STATUS_KEY = "status"  # noqa: N806
    EMPTY_STRING = ""  # noqa: N806

    HEX_BASE = 16  # noqa: N806
    HEX_PATTERN = r"%([0-9a-fA-F]{2})"  # noqa: N806

    result = dbx_data.get(RESULT_KEY, EMPTY_STRING)
    widget_data = dbx_data.get(DATA_KEY, EMPTY_STRING)

    unquoted_string = unquote(widget_data)
    decoded_string = re.sub(
        HEX_PATTERN,
        lambda match: chr(int(match.group(1), HEX_BASE)),
        unquoted_string,
    )

    # Create JSON structure for all dialog types
    dialog_result = {
        RESULT_KEY: result,
        DATA_KEY: decoded_string,
    }

    # Convert to JSON string for transmission
    combined_data = json.dumps(dialog_result)

    if app.state.pytest_wrp.send_data(combined_data):
        return {STATUS_KEY: Status.BUSY}
    return {STATUS_KEY: Status.ERROR}


@app.post("/api/confirm_operator_msg/{is_msg_visible}")
def confirm_operator_msg(
    is_msg_visible: str, session_id: Annotated[str | None, Query()] = None
) -> dict:
    """Confirm operator msg.

    Args:
        is_msg_visible (bool): is operator message is visible
        session_id: User session ID for authentication

    Returns:
        dict[str, RunStatus]: run status
    """
    if not _is_authenticated(session_id):
        return {"status": Status.UNAUTHORIZED}

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
