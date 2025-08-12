from __future__ import annotations

import json
import subprocess
import time
from pathlib import Path
from typing import TYPE_CHECKING

import psutil
import pytest
import requests

if TYPE_CHECKING:
    from types import NoneType

HARDPY_RUN_CMD = ["hardpy", "run"]
HARDPY_INIT_CMD = ["hardpy", "init", "--frontend-port", "8000"]
API_START_URL = "http://localhost:8000/api/start"
API_STOP_URL = "http://localhost:8000/api/stop"
API_STATUS_URL = "http://localhost:8000/api/status"
STATUS_CHECK_TIMEOUT = 30  # seconds
STATUS_CHECK_INTERVAL = 0.5  # seconds


@pytest.fixture(scope="function")  # noqa: PT003
def test_project(tmp_path: Path) -> Path:
    """Create a test project with necessary test files."""
    # Initialize HardPy project
    subprocess.run([*HARDPY_INIT_CMD, str(tmp_path)], check=True)

    # Create test files with FIXED conftest.py
    (tmp_path / "conftest.py").write_text("""
import pytest

@pytest.fixture(scope="session")
def start_params(request):
    params = {}
    # Parse multiple parameters correctly
    for item in request.config.getoption("--hardpy-start-param"):
        # Handle key=value pairs
        if "=" in item:
            key, value = item.split("=", 1)
            params[key] = value
    return params
""")

    (tmp_path / "test_api_params.py").write_text("""
import time

def test_api_parameters(start_params):
    # time.sleep(15)
    # assert True
    assert "test_id" in start_params, "test_id not found"
    assert "env" in start_params, "env not found"
    assert start_params["test_id"] == "123"
    assert start_params["env"] == "prod"
""")

    # Create empty __init__.py to mark as package
    (tmp_path / "__init__.py").touch()

    return tmp_path


def test_hardpy_start(process_killer: NoneType, test_project: Path):
    """Test that parameters are correctly passed via API."""
    # Start HardPy server
    server_process = subprocess.Popen(
        [*HARDPY_RUN_CMD, str(test_project)],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    time.sleep(3)  # Wait for server initialization

    # Verify server is running
    status = requests.get(API_STATUS_URL, timeout=5).json()
    assert status["status"] == "ready", "Server not ready"

    start_response = requests.get(
        # f"{API_START_URL}?param=test_id=123&param=env=prod",
        f"{API_START_URL}",
        timeout=5,
    )
    assert start_response.status_code == 200, "Test start failed"

    while True:
        status_response = requests.get(API_STATUS_URL, timeout=5)
        status = status_response.json()
        if status["status"] == "ready":
            break
        time.sleep(1)


def test_hardpy_stop(process_killer: NoneType, test_project: Path):
    """Test that parameters are correctly passed via API."""
    # Start HardPy server
    server_process = subprocess.Popen(
        [*HARDPY_RUN_CMD, str(test_project)],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    time.sleep(3)  # Wait for server initialization

    # Verify server is running
    status = requests.get(API_STATUS_URL, timeout=5).json()
    assert status["status"] == "ready", "Server not ready"
    start_response = requests.get(
        # f"{API_START_URL}?param=test_id=123&param=env=prod",
        f"{API_START_URL}",
        timeout=2,
    )
    assert start_response.status_code == 200, "Test start failed"
    start_response = requests.get(
        # f"{API_START_URL}?param=test_id=123&param=env=prod",
        f"{API_STOP_URL}",
        timeout=2,
    )
    assert start_response.status_code == 200, "Test start failed"

    while True:
        status_response = requests.get(API_STATUS_URL, timeout=5)
        status = status_response.json()
        if status["status"] == "ready":
            break
        time.sleep(1)


def test_hardpy_start_with_params(process_killer: NoneType, test_project: Path):
    """Test that parameters are correctly passed via API."""
    # Start HardPy server
    server_process = subprocess.Popen(
        [*HARDPY_RUN_CMD, str(test_project)],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    time.sleep(3)  # Wait for server initialization

    # Verify server is running
    status = requests.get(API_STATUS_URL, timeout=5).json()
    assert status["status"] == "ready", "Server not ready"

    start_response = requests.get(
        f"{API_START_URL}?params=test_id=123&params=env=prod",
        timeout=5,
    )
    assert start_response.status_code == 200, "Test start failed"
    time.sleep(5)
    while True:
        status_response = requests.get(API_STATUS_URL, timeout=5)
        status = status_response.json()
        if status["status"] == "ready":
            break
        time.sleep(1)
