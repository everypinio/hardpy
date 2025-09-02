from __future__ import annotations

import subprocess
import time
from typing import TYPE_CHECKING

import pytest
import requests

from hardpy.pytest_hardpy.result import CouchdbReader
from hardpy.pytest_hardpy.result.couchdb_config import CouchdbConfig

if TYPE_CHECKING:
    from pathlib import Path

API_STATUS_URL = "http://localhost:8000/api/status"
HARDPY_INIT_CMD = ["hardpy", "init", "--frontend-port", "8000"]
STATUS_CHECK_TIMEOUT = 30  # seconds
STATUS_CHECK_INTERVAL = 0.5  # seconds


class HardPyServer:  # noqa: D101
    def __init__(self, project_path: Path):  # noqa: ANN204
        self.project_path = project_path
        self.process = None

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

    def check_status(self, url=API_STATUS_URL):  # noqa: ANN001, D102
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            msg = f"Server status check failed: {e}"
            raise RuntimeError(msg) from e

    def wait_until_ready(self):  # noqa: D102
        timeout = time.time() + STATUS_CHECK_TIMEOUT
        while time.time() < timeout:
            try:
                status = self.check_status()
                if status.get("status") == "ready":
                    return status
            except RuntimeError:
                pass
            time.sleep(STATUS_CHECK_INTERVAL)
        msg = "Server did not become ready in time"
        raise TimeoutError(msg)

    def wait_until_test_complete(self):  # noqa: D102
        timeout = time.time() + STATUS_CHECK_TIMEOUT
        while time.time() < timeout:
            status = self.check_status()
            if status.get("status") != "busy":
                return status
            time.sleep(STATUS_CHECK_INTERVAL)
        msg = "Test did not complete in time"
        raise TimeoutError(msg)

    @staticmethod
    def get_test_result():  # noqa: ANN205, D102
        config = CouchdbConfig(
            db_name="runstore",
            user="dev",
            password="dev",
            host="localhost",
            port=5984,
        )
        return CouchdbReader(config).get_report_status("current")

    @staticmethod
    def run_command(command, cwd=None, timeout=30):  # noqa: ANN001, ANN205, D102
        return subprocess.run(
            command,
            capture_output=True,
            cwd=cwd,
            timeout=timeout,
            check=False,
        )


@pytest.fixture
def project_dir(tmp_path: Path) -> Path:
    """Create a test project with necessary test files."""
    subprocess.run([*HARDPY_INIT_CMD, str(tmp_path)], check=True)

    (tmp_path / "test_simple.py").write_text("""
import time

def test_basic_api_call():
    time.sleep(7)
    assert True
""")
    (tmp_path / "__init__.py").touch()
    return tmp_path


@pytest.fixture
def project_dir_with_ini(tmp_path: Path) -> Path:
    """Create test project with pytest.ini configuration."""
    return _create_test_project_with_ini(tmp_path, "DUT-007")


@pytest.fixture
def project_dir_with_ini_incorrect(tmp_path: Path) -> Path:
    """Create test project with pytest.ini configuration (incorrect)."""
    return _create_test_project_with_ini(tmp_path, "DUT-006")


@pytest.fixture
def project_dir_with_args(tmp_path: Path) -> Path:
    """Create test project with pytest.ini configuration."""
    subprocess.run([*HARDPY_INIT_CMD, str(tmp_path)], check=True)

    ini_content = """[pytest]
addopts = --hardpy-pt
        --hardpy-db-url http://dev:dev@localhost:5984/
"""
    (tmp_path / "pytest.ini").write_text(ini_content)

    (tmp_path / "test_hardpy_args.py").write_text("""
import hardpy
import time

def test_ini_parameters(hardpy_start_args):
    time.sleep(3)
    assert hardpy_start_args.get("test_mode") == "debug"
    assert hardpy_start_args.get("device_id") == "DUT-007"
    assert hardpy_start_args.get("retry_count") == "3"
""")

    (tmp_path / "__init__.py").touch()
    return tmp_path


@pytest.fixture
def hardpy_server_class():
    return HardPyServer


def _create_test_project_with_ini(tmp_path: Path, device_id: str) -> Path:
    subprocess.run([*HARDPY_INIT_CMD, str(tmp_path)], check=True)

    ini_content = f"""[pytest]
addopts = --hardpy-pt
        --hardpy-db-url http://dev:dev@localhost:5984/
        --hardpy-start-arg test_mode=debug
        --hardpy-start-arg device_id={device_id}
        --hardpy-start-arg retry_count=3
"""
    (tmp_path / "pytest.ini").write_text(ini_content)

    (tmp_path / "test_hardpy_args.py").write_text("""
import hardpy

def test_ini_parameters(hardpy_start_args):
    assert hardpy_start_args.get("test_mode") == "debug"
    assert hardpy_start_args.get("device_id") == "DUT-007"
    assert hardpy_start_args.get("retry_count") == "3"
""")

    (tmp_path / "__init__.py").touch()
    return tmp_path
