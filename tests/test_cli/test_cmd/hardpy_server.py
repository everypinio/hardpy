from __future__ import annotations

import subprocess
import time
from typing import TYPE_CHECKING

import requests

from hardpy.common.config import ConfigManager
from hardpy.pytest_hardpy.result import CouchdbReader
from hardpy.pytest_hardpy.result.couchdb_config import CouchdbConfig

if TYPE_CHECKING:
    from pathlib import Path


class HardPyServer:  # noqa: D101
    def __init__(self, project_path: Path):  # noqa: ANN204
        self.project_path = project_path
        self.process = None
        self._status_check_timeout = 30  # seconds
        self._status_check_interval = 0.5  # seconds
        self._config = ConfigManager().read_config(project_path)

    def start_server(self):  # noqa: D102
        self.process = subprocess.Popen(
            ["hardpy", "run"],  # noqa: S607
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            cwd=str(self.project_path),
        )
        return self.process

    def stop_server(self):  # noqa: D102
        if self.process:
            self.process.terminate()
            self.process.wait(timeout=10)

    def check_status(self) -> dict:  # noqa: D102
        url = "http://localhost:8000/api/status"
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            msg = f"Server status check failed: {e}"
            raise RuntimeError(msg) from e

    def wait_until_ready(self) -> str:  # noqa: D102
        timeout = time.time() + self._status_check_timeout
        while time.time() < timeout:
            try:
                status = self.check_status()
                if status.get("status") == "ready":
                    return status
            except RuntimeError:
                pass
            time.sleep(self._status_check_interval)
        msg = "Server did not become ready in time"
        raise TimeoutError(msg)

    def wait_until_test_complete(self):  # noqa: D102
        timeout = time.time() + self._status_check_timeout
        while time.time() < timeout:
            status = self.check_status()
            if status.get("status") != "busy":
                return status
            time.sleep(self._status_check_interval)
        msg = "Test did not complete in time"
        raise TimeoutError(msg)

    def get_test_result(self):  # noqa: D102
        config = CouchdbConfig(
            db_name="runstore",
            user="dev",
            password="dev",
            host="localhost",
            port=5984,
        )
        return CouchdbReader(config).get_report_status(self._config.database.doc_id)

    def run_command(self, command: list, cwd: str | None = None, timeout: int = 30):  # noqa: D102
        return subprocess.run(
            command,
            capture_output=True,
            cwd=cwd,
            timeout=timeout,
            check=False,
        )
