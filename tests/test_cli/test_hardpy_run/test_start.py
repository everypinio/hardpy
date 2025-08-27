from __future__ import annotations

import subprocess
import time
from typing import TYPE_CHECKING

import pytest
import requests

if TYPE_CHECKING:
    from pathlib import Path

HARDPY_RUN_CMD = ["hardpy", "run"]
HARDPY_INIT_CMD = ["hardpy", "init", "--frontend-port", "8000"]
HARDPY_START_CMD = ["hardpy", "start"]
PYTEST_CMD = ["pytest"]
API_START_URL = "http://localhost:8000/api/start"
API_STOP_URL = "http://localhost:8000/api/stop"
API_STATUS_URL = "http://localhost:8000/api/status"
STATUS_CHECK_TIMEOUT = 30  # seconds
STATUS_CHECK_INTERVAL = 0.5  # seconds


def wait_for_server_ready(timeout: int = STATUS_CHECK_TIMEOUT):
    """Waits for the HardPy server to be in a "ready" state by polling the status API."""  # noqa: E501
    start_time = time.time()
    while time.time() - start_time < timeout:
        try:
            status_response = requests.get(API_STATUS_URL, timeout=2)
            if status_response.status_code == 200:
                status = status_response.json()
                if status["status"] == "ready":
                    print("Server is ready.")  # noqa: T201
                    return True
        except (requests.exceptions.ConnectionError, requests.exceptions.Timeout):  # noqa: PERF203
            print("Waiting for server to start...")  # noqa: T201
            time.sleep(STATUS_CHECK_INTERVAL)

    # If the loop finishes without the server being ready, something is wrong.
    print(f"Timed out waiting for server to become ready after {timeout} seconds.")  # noqa: T201
    return False


def wait_for_test_completion():
    """Waits for the server to return to the 'ready' state after a test run."""
    start_time = time.time()
    print("Waiting for test execution to complete...")  # noqa: T201
    while True:
        try:
            status_response = requests.get(API_STATUS_URL, timeout=5)
            status = status_response.json()
            if status["status"] == "ready":
                print("Test execution complete.")  # noqa: T201
                return True
        except (requests.exceptions.ConnectionError, requests.exceptions.Timeout):
            pass  # Server might be temporarily down or busy during test run
        time.sleep(1)
        if time.time() - start_time > STATUS_CHECK_TIMEOUT * 2:
            print("Timed out waiting for test completion.")  # noqa: T201
            return False


# This fixture creates a simple test project with a basic test file.
@pytest.fixture(scope="function")  # noqa: PT003
def test_project(tmp_path: Path) -> Path:
    """Create a test project with necessary test files."""
    # Initialize HardPy project
    subprocess.run([*HARDPY_INIT_CMD, str(tmp_path)], check=True)

    # Create a simple test file that doesn't rely on start arguments
    (tmp_path / "test_simple.py").write_text("""
def test_basic_api_call():
    assert True
""")
    (tmp_path / "__init__.py").touch()
    return tmp_path


@pytest.fixture(scope="function")  # noqa: PT003
def test_project_with_ini(tmp_path: Path) -> Path:
    """Create test project with pytest.ini configuration and a test file that uses hardpy.get_start_args()."""  # noqa: E501
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

    # Create test file that uses hardpy.get_start_args() to check for parameters
    (tmp_path / "test_hardpy_args.py").write_text("""
import hardpy

def test_ini_parameters():
    start_args = hardpy.get_start_args()
    print(f"Arguments: {{start_args}}")
    assert start_args.get("test_mode") == "debug"
    assert start_args.get("device_id") == "DUT-007"
    assert start_args.get("retry_count") == "3"
""")

    (tmp_path / "__init__.py").touch()
    return tmp_path


@pytest.fixture(scope="function")  # noqa: PT003
def test_project_with_args(tmp_path: Path) -> Path:
    """Create test project with pytest.ini configuration and a test file that uses hardpy.get_start_args()."""  # noqa: E501
    subprocess.run([*HARDPY_INIT_CMD, str(tmp_path)], check=True)

    # Create pytest.ini with start arguments
    ini_content = """[pytest]
addopts = --hardpy-pt
        --hardpy-db-url http://dev:dev@localhost:5984/
"""
    (tmp_path / "pytest.ini").write_text(ini_content)

    # Create test file that uses hardpy.get_start_args() to check for parameters
    (tmp_path / "test_hardpy_args.py").write_text("""
import hardpy

def test_ini_parameters():
    start_args = hardpy.get_start_args()
    assert start_args.get("test_mode") == "debug"
    assert start_args.get("device_id") == "DUT-00"
    assert start_args.get("retry_count") == "3"
""")

    (tmp_path / "__init__.py").touch()
    return tmp_path


@pytest.mark.manual
def test_with_hardpy_run_and_hardpy_start(test_project: Path):
    """Test that hardpy run and hardpy start can be used together."""
    server_process = None
    try:
        server_process = run_hardpy_server(test_project)
        time.sleep(5)
        status = check_server_status()
        assert status.get("status") == "ready", f"Server not ready: {status}"

        result = run_command(["hardpy", "start"], cwd=str(test_project))
        assert result.returncode == 0, f"Command failed: {result.stderr.decode()}"

    finally:
        if server_process:
            server_process.terminate()
            server_process.wait(timeout=10)


@pytest.mark.manual
def test_with_hardpy_run_and_hardpy_start_with_ini_args(test_project_with_ini: Path):
    """Test that hardpy run and hardpy start can be used together."""
    server_process = None
    try:
        server_process = run_hardpy_server(test_project_with_ini)
        time.sleep(5)
        status = check_server_status()
        assert status.get("status") == "ready", f"Server not ready: {status}"

        result = run_command(["hardpy", "start"], cwd=str(test_project_with_ini))
        assert result.returncode == 0, f"Command failed: {result.stderr.decode()}"
        time.sleep(10)

    finally:
        if server_process:
            server_process.terminate()
            server_process.wait(timeout=10)


@pytest.mark.manual
def test_with_hardpy_run_and_hardpy_start_with_args(test_project_with_args: Path):
    """Test that hardpy run and hardpy start can be used together."""
    server_process = None
    try:
        server_process = run_hardpy_server(test_project_with_args)
        time.sleep(5)
        status = check_server_status()
        assert status.get("status") == "ready", f"Server not ready: {status}"

        result = run_command(
            [
                "hardpy",
                "start",
                "--arg",
                "test_mode=debug",
                "--arg",
                "device_id=DUT-007",
                "--arg",
                "retry_count=3",
            ],
            cwd=str(test_project_with_args),
        )
        assert result.returncode == 0, f"Command failed: {result.stderr.decode()}"
        time.sleep(10)

    finally:
        if server_process:
            server_process.terminate()
            server_process.wait(timeout=10)


@pytest.mark.manual
def test_with_hardpy_run_and_pytest_with_args(test_project_with_args: Path):
    """Test that hardpy run and hardpy start can be used together."""
    server_process = None
    try:
        server_process = run_hardpy_server(test_project_with_args)
        time.sleep(5)
        status = check_server_status()
        assert status.get("status") == "ready", f"Server not ready: {status}"

        result = run_command(
            [
                "pytest",
                "--hardpy-start-arg",
                "test_mode=debug",
                "--hardpy-start-arg",
                "device_id=DUT-007",
                "--hardpy-start-arg",
                "retry_count=3",
            ],
            cwd=str(test_project_with_args),
        )
        assert result.returncode == 0, f"Command failed: {result.stderr.decode()}"
        time.sleep(10)

    finally:
        if server_process:
            server_process.terminate()
            server_process.wait(timeout=10)


@pytest.mark.manual
def test_with_hardpy_run_and_api_start_with_args(test_project_with_args: Path):
    """Test that hardpy run and hardpy start can be used together."""
    server_process = None
    try:
        server_process = run_hardpy_server(test_project_with_args)
        time.sleep(5)
        status = check_server_status()
        assert status.get("status") == "ready", f"Server not ready: {status}"

        start_response = requests.get(
            f"{API_START_URL}?args=test_mode=debug&args=device_id=DUT-007&args=retry_count=3",
            timeout=5,
        )
        assert start_response.status_code == 200, "Test start failed"
        time.sleep(10)

    finally:
        if server_process:
            server_process.terminate()
            server_process.wait(timeout=10)


def run_hardpy_server(plan_dir: Path) -> subprocess.Popen:
    """Starts HardPy server in background mode."""
    return run_background_process(["hardpy", "run"], cwd=str(plan_dir))


def run_background_process(command, cwd=None):  # noqa: ANN001
    """Runs a command in background and returns the process."""
    return subprocess.Popen(
        command,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        cwd=cwd,
    )


def run_command(command, cwd=None, timeout=30):  # noqa: ANN001
    """Runs a command and waits for completion. Returns completed process."""
    return subprocess.run(
        command,
        capture_output=True,
        cwd=cwd,
        timeout=timeout,
        check=False,
    )


def check_server_status(url="http://localhost:8000/api/status") -> dict:  # noqa: ANN001
    """Checks HardPy server status via API."""
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        msg = f"Server status check failed: {e}"
        raise RuntimeError(msg) from e
