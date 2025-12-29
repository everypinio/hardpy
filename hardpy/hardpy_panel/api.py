# Copyright (c) 2024 Everypin
# GNU General Public License v3.0 (see LICENSE or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import annotations

import asyncio
import contextlib
import json
import logging
import os
import re
from concurrent.futures import ThreadPoolExecutor
from enum import Enum
from pathlib import Path
from typing import TYPE_CHECKING, Annotated, Any, Final
from urllib.parse import unquote

from fastapi import FastAPI, Query, Request
from fastapi.staticfiles import StaticFiles

from hardpy.common.config import ConfigManager, StorageType
from hardpy.pytest_hardpy.pytest_wrapper import PyTestWrapper
from hardpy.pytest_hardpy.result.report_synchronizer import StandCloudSynchronizer

if TYPE_CHECKING:
    from collections.abc import AsyncGenerator

# TODO (xorialexandrov): Move logging to own module
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s:\t %(message)s",
)
logger = logging.getLogger(__name__)


@contextlib.asynccontextmanager
async def lifespan_sync_scheduler(app: FastAPI) -> AsyncGenerator[Any, Any]:
    """Manages the lifecycle events (startup and shutdown) for background tasks."""
    # Start StandCloud synchronization if enabled
    config_manager = ConfigManager()
    sc_autosync = config_manager.config.stand_cloud.autosync
    if sc_autosync:
        autosync_timeout = config_manager.config.stand_cloud.autosync_timeout
        app.state.sync_task = asyncio.create_task(sync_stand_cloud(autosync_timeout))

    yield

    # Cleanup on shutdown
    if sc_autosync and hasattr(app.state, "sync_task"):
        app.state.sync_task.cancel()
        await asyncio.gather(app.state.sync_task, return_exceptions=True)
        logger.info("Cancelled StandCloud synchronization task.")

    if hasattr(app.state, "executor"):
        app.state.executor.shutdown(wait=False)
        logger.info("Shut down ThreadPoolExecutor.")


# Initialize application state
app = FastAPI(lifespan=lifespan_sync_scheduler)
app.state.pytest_wrp = PyTestWrapper()
app.state.sc_synchronizer = StandCloudSynchronizer()
app.state.executor = ThreadPoolExecutor(max_workers=1)
app.state.manual_collect_mode = False
app.state.selected_tests = []


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


async def sync_stand_cloud(sc_sync_interval_minutes: int) -> None:
    """Periodically calls the blocking stand_cloud_sync logic in a separate thread."""
    sc_sync_interval: Final[int] = sc_sync_interval_minutes * 60
    initial_pause: Final[int] = 30

    loop = asyncio.get_event_loop()
    await asyncio.sleep(initial_pause)

    while True:
        try:
            sync_result = await loop.run_in_executor(
                app.state.executor,
                app.state.sc_synchronizer.sync,
            )
            logger.info(f"StandCloud synchronization status: {sync_result}")
        except asyncio.CancelledError:
            logger.info("StandCloud synchronization task cancelled.")
            break
        except Exception as exc:  # noqa: BLE001
            logger.info(f"Error during StandCloud synchronization. {exc}")
        await asyncio.sleep(sc_sync_interval)


@app.get("/api/hardpy_config")
def hardpy_config() -> dict:
    """Get config of HardPy.

    Returns:
        dict: HardPy config
    """
    return app.state.pytest_wrp.get_config()


@app.post("/api/set_test_config/{config_name}")
def set_test_config(config_name: str) -> dict:
    """Set the current test configuration.

    Args:
        config_name (str): Name of the test configuration to set
    Returns:
        dict: Status of the operation.
    """
    config_manager = ConfigManager()
    config_manager.set_current_test_config(config_name)
    try:
        app.state.pytest_wrp.collect(is_clear_database=True)
    except (ValueError, RuntimeError) as e:
        return {"status": "error", "message": str(e)}
    else:
        return {"status": "success", "current_config": config_name}


@app.get("/api/start")
def start_pytest(args: Annotated[list[str] | None, Query()] = None) -> dict:
    """Start pytest subprocess.

    Args:
        args: List of arguments in key=value format

    Returns:
        dict[str, RunStatus]: run status
    """
    if app.state.manual_collect_mode:
        return {"status": Status.BUSY, "message": "Manual collect mode is active"}

    if args is None:
        args_dict = []
    else:
        args_dict = dict(arg.split("=", 1) for arg in args if "=" in arg)

    if app.state.pytest_wrp.start(
        start_args=args_dict,
        selected_tests=app.state.selected_tests,
    ):
        logger.info("Start testing process.")
        return {"status": Status.STARTED}
    logger.info("Testing process is already running.")
    return {"status": Status.BUSY}


@app.get("/api/stop")
def stop_pytest() -> dict:
    """Stop pytest subprocess.

    Returns:
        dict[str, RunStatus]: run status
    """
    if app.state.manual_collect_mode:
        return {"status": Status.BUSY, "message": "Manual collect mode is active"}

    if app.state.pytest_wrp.stop():
        logger.info("Stop testing process.")
        return {"status": Status.STOPPED}
    logger.info("Testing process is not running.")
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


@app.get("/api/stand_cloud_sync")
async def stand_cloud_sync() -> dict:
    """Stop pytest subprocess.

    Returns:
        dict[status, str]: synchronization status
    """
    loop = asyncio.get_event_loop()
    try:
        sync_result = await loop.run_in_executor(
            app.state.executor,
            app.state.sc_synchronizer.sync,
        )
    except Exception as exc:  # noqa: BLE001
        msg = f"Error during StandCloud synchronization. {exc}"
        logger.info(msg)
        return {"status": msg}
    logger.info(f"StandCloud syncronization status: {sync_result}")
    return {"status": sync_result}


@app.post("/api/confirm_dialog_box")
def confirm_dialog_box(dbx_data: dict) -> dict:
    """Confirm dialog box with unified JSON structure.

    Args:
        dbx_data: dict with 'result' (pass/fail/confirm) and 'data' (widget data)

    Returns:
        dict[str, RunStatus]: run status
    """
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


@app.post("/api/selected_tests")
async def set_selected_tests(request: Request) -> dict:
    """Set the selected tests in the application state.

    Args:
        request (Request): The incoming request object.

    Returns:
        dict[str, str]: A dictionary containing the
                        status and message of the operation.
            - status (str): The status of the operation.
                            Possible values are "success" or "error".
            - message (str): A message describing the
                             result of the operation.

    Raises:
        TypeError: If the `selected_tests` is not a list.
    """
    selected_tests = await request.json()

    if not isinstance(selected_tests, list):
        msg = "Expected list."
        raise TypeError(msg)

    app.state.selected_tests = selected_tests
    app.state.pytest_wrp.collect(is_clear_database=True, selected_tests=selected_tests)
    return {"status": "success", "message": f"Selected {len(selected_tests)} tests"}


@app.get("/api/manual_collect_mode")
def get_manual_collect_mode() -> dict:
    """Get manual collect mode status.

    Returns:
        dict[str, bool]: manual collect mode status
    """
    return {"manual_collect_mode": app.state.manual_collect_mode}


@app.post("/api/manual_collect_mode")
def set_manual_collect_mode(mode_data: dict) -> dict:
    """Set manual collect mode.

    Args:
        mode_data: dict with 'enabled' key

    Returns:
        dict[str, str]: operation status
    """
    enabled = mode_data.get("enabled", False)
    app.state.manual_collect_mode = enabled

    if enabled:
        app.state.pytest_wrp.collect()

    return {"status": "success", "manual_collect_mode": enabled}


@app.get("/api/storage_type")
def get_storage_type() -> dict:
    """Get the configured storage type.

    Returns:
        dict[str, str]: storage type ("json" or "couchdb")
    """
    config_manager = ConfigManager()
    return {"storage_type": config_manager.config.database.storage_type}


@app.get("/api/json_data")
def get_json_data() -> dict:
    """Get test run data from JSON storage.

    Returns:
        dict: Test run data from JSON files
    """
    config_manager = ConfigManager()
    storage_type = config_manager.config.database.storage_type

    if storage_type != StorageType.JSON:
        return {"error": "JSON storage not configured"}

    try:
        config_storage_path = Path(config_manager.config.database.storage_path)
        if config_storage_path.is_absolute():
            storage_dir = config_storage_path / "storage" / "statestore"
        else:
            storage_dir = Path(
                config_manager.tests_path
                / config_manager.config.database.storage_path
                / "storage"
                / "statestore",
            )
        _doc_id = config_manager.config.database.doc_id
        statestore_file = storage_dir / f"{_doc_id}.json"

        if not statestore_file.exists():
            return {"rows": [], "total_rows": 0}

        with statestore_file.open("r") as f:
            data = json.load(f)

        # Format data to match CouchDB's _all_docs format
        return {
            "rows": [
                {
                    "id": data.get("_id", ""),
                    "key": data.get("_id", ""),
                    "value": {"rev": data.get("_rev", "1-0")},
                    "doc": data,
                },
            ],
            "total_rows": 1,
        }
    except Exception as exc:
        logger.exception("Error reading JSON storage")
        return {"error": str(exc), "rows": [], "total_rows": 0}


if "DEBUG_FRONTEND" not in os.environ:
    app.mount(
        "/",
        StaticFiles(
            directory=Path(__file__).parent / "frontend/dist",
            html=True,
        ),
        name="static",
    )
