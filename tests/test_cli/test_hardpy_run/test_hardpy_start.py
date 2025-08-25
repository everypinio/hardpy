from __future__ import annotations

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
HARDPY_START_CMD = ["hardpy", "start"]
PYTEST_CMD = ["pytest"]
API_START_URL = "http://localhost:8000/api/start"
API_STOP_URL = "http://localhost:8000/api/stop"
API_STATUS_URL = "http://localhost:8000/api/status"
STATUS_CHECK_TIMEOUT = 30  # seconds
STATUS_CHECK_INTERVAL = 0.5  # seconds


def kill_process_on_port(port: int):
    for proc in psutil.process_iter(["pid", "name", "connections"]):
        try:
            for conn in proc.connections():
                if conn.laddr.port == port:
                    psutil.Process(proc.pid).kill()
                    return True
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue
    return False


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
    time.sleep(5)
    assert True
""")

    # Create empty __init__.py to mark as package
    (tmp_path / "__init__.py").touch()

    return tmp_path


@pytest.fixture(scope="function")  # noqa: PT003
def test_project_with_args(tmp_path: Path) -> Path:
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
    assert "test_id" in start_params, "test_id not found"
    assert "env" in start_params, "env not found"
    assert start_params["test_id"] == "123"
    assert start_params["env"] == "prod"
""")

    # Create empty __init__.py to mark as package
    (tmp_path / "__init__.py").touch()

    return tmp_path


@pytest.fixture(scope="function")
def test_project_with_ini(tmp_path: Path) -> Path:
    """Create test project with pytest.ini configuration"""
    subprocess.run([*HARDPY_INIT_CMD, str(tmp_path)], check=True)

    # Create pytest.ini with start arguments
    ini_content = """[pytest]
addopts = --hardpy-pt
        --hardpy-db-url http://dev:dev@localhost:5984/
        --hardpy-start-arg test_mode=debug
        --hardpy-start-arg device_id=DUT-007
        --hardpy-start-arg retry_count=3
"""
    (tmp_path / "pytest.ini").write_text(ini_content)

    # Create test file
    (tmp_path / "test_ini_params.py").write_text("""
def test_ini_parameters(start_params):
    assert start_params["test_mode"] == "debug"
    assert start_params["device_id"] == "DUT-007"
    assert start_params["retry_count"] == "3"
""")

    # Create conftest.py with start_params fixture
    (tmp_path / "conftest.py").write_text("""
import pytest

@pytest.fixture(scope="session")
def start_params(request):
    params = {}
    for item in request.config.getoption("--hardpy-start-param"):
        if "=" in item:
            key, value = item.split("=", 1)
            params[key] = value
    return params
""")

    (tmp_path / "__init__.py").touch()
    return tmp_path


@pytest.fixture(autouse=True)
def kill_port_process():
    yield
    kill_process_on_port(8000)


def test_hardpy_start(test_project: Path):
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


def test_hardpy_stop(test_project: Path):
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
        f"{API_START_URL}",
        timeout=2,
    )
    assert start_response.status_code == 200, "Test start failed"
    start_response = requests.get(
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


def test_hardpy_start_with_args(test_project_with_args: Path):
    """Test that args are correctly passed via API."""
    # Start HardPy server
    server_process = subprocess.Popen(
        [*HARDPY_RUN_CMD, str(test_project_with_args)],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    time.sleep(3)  # Wait for server initialization

    # Verify server is running
    status = requests.get(API_STATUS_URL, timeout=5).json()
    assert status["status"] == "ready", "Server not ready"

    start_response = requests.get(
        f"{API_START_URL}?args=test_id=123&args=env=prod",
        timeout=5,
    )
    assert start_response.status_code == 200, "Test start failed"
    time.sleep(3)
    while True:
        status_response = requests.get(API_STATUS_URL, timeout=5)
        status = status_response.json()
        if status["status"] == "ready":
            break
        time.sleep(1)


def test_hardpy_start_with_cli_args(test_project_with_args: Path):
    """Test passing arguments via CLI using hardpy start command"""
    # Start HardPy server with CLI arguments
    server_process = subprocess.Popen(
        [
            *HARDPY_START_CMD,
            str(test_project_with_args),
            "--arg",
            "test_id=123",
            "--arg",
            "env=prod",
        ],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    time.sleep(3)

    # Verify server is running
    status = requests.get(API_STATUS_URL, timeout=5).json()
    assert status["status"] == "ready", "Server not ready"

    # Start test execution
    start_response = requests.get(API_START_URL, timeout=5)
    assert start_response.status_code == 200, "Test start failed"

    # Wait for completion
    time.sleep(3)
    while True:
        status_response = requests.get(API_STATUS_URL, timeout=5)
        status = status_response.json()
        if status["status"] == "ready":
            break
        time.sleep(1)


def test_hardpy_start_with_ini(test_project_with_ini: Path):
    """Test passing arguments via pytest.ini configuration"""
    # Start HardPy server (should use arguments from pytest.ini)
    server_process = subprocess.Popen(
        [*HARDPY_RUN_CMD, str(test_project_with_ini)],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    time.sleep(3)

    # Verify server is running
    status = requests.get(API_STATUS_URL, timeout=5).json()
    assert status["status"] == "ready", "Server not ready"

    # Start test execution
    start_response = requests.get(API_START_URL, timeout=5)
    assert start_response.status_code == 200, "Test start failed"

    # Wait for completion
    time.sleep(3)
    while True:
        status_response = requests.get(API_STATUS_URL, timeout=5)
        status = status_response.json()
        if status["status"] == "ready":
            break
        time.sleep(1)


def test_hardpy_start_with_mixed_args(test_project_with_ini: Path):
    """Test CLI arguments override pytest.ini configuration"""
    # Start HardPy server with CLI args (should override pytest.ini)
    server_process = subprocess.Popen(
        [
            *PYTEST_CMD,
            str(test_project_with_ini),
            "--hardpy-start-arg",
            "test_mode=production",
            "--hardpy-start-arg",
            "device_id=OVERRIDE-001",
        ],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    time.sleep(3)

    # Verify server is running
    status = requests.get(API_STATUS_URL, timeout=5).json()
    assert status["status"] == "ready", "Server not ready"

    # Start test execution
    start_response = requests.get(API_START_URL, timeout=5)
    assert start_response.status_code == 200, "Test start failed"

    # Wait for completion
    time.sleep(3)
    while True:
        status_response = requests.get(API_STATUS_URL, timeout=5)
        status = status_response.json()
        if status["status"] == "ready":
            break
        time.sleep(1)
