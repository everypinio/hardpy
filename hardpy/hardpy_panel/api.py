# Copyright (c) 2024 Everypin
# GNU General Public License v3.0 (see LICENSE or https://www.gnu.org/licenses/gpl-3.0.txt)

import os

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from hardpy.pytest_hardpy.utils import ConfigData, RunStatus as Status
from hardpy.pytest_hardpy.pytest_wrapper import PyTestWrapper

app = FastAPI()
app.state.pytest_wrp = PyTestWrapper()


@app.get("/api/start")
def start_pytest():
    """Start pytest subprocess.

    Returns:
        dict[str, RunStatus]: run status
    """
    if app.state.pytest_wrp.start():
        return {"status": Status.STARTED}
    return {"status": Status.BUSY}


@app.get("/api/stop")
def stop_pytest():
    """Stop pytest subprocess.

    Returns:
        dict[str, RunStatus]: run status
    """
    if app.state.pytest_wrp.stop():
        return {"status": Status.STOPPED}
    return {"status": Status.READY}


@app.get("/api/collect")
def collect_pytest():
    """Collect pytest subprocess.

    Returns:
        dict[str, RunStatus]: run status

    """
    if app.state.pytest_wrp.collect():
        return {"status": Status.COLLECTED}
    return {"status": Status.BUSY}


@app.get("/api/couch")
def couch_connection():
    """Get couchdb connection string.

    Returns:
        dict[str, str, str]: couchdb connection string
    """
    config_data = ConfigData()

    return {
        "connection_str": config_data.connection_string,
    }


app.mount(
    "/",
    StaticFiles(directory=(os.path.dirname(__file__))+'/frontend/dist', html=True),
    name="static",
)
