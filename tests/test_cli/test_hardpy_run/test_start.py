from __future__ import annotations

import subprocess
import time
from typing import TYPE_CHECKING

import pytest
import requests

from hardpy.pytest_hardpy.result import CouchdbReader
from hardpy.pytest_hardpy.result.couchdb_config import CouchdbConfig
from hardpy.pytest_hardpy.utils.const import TestStatus as Status

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


# This fixture creates a simple test project with a basic test file.
@pytest.fixture(scope="function")  # noqa: PT003
def test_project(tmp_path: Path) -> Path:
    """Create a test project with necessary test files."""
    # Initialize HardPy project
    subprocess.run([*HARDPY_INIT_CMD, str(tmp_path)], check=True)

    # Create a simple test file that doesn't rely on start arguments
    (tmp_path / "test_simple.py").write_text("""
import time

def test_basic_api_call():
    time.sleep(3)
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
def test_project_with_ini_incorrect(tmp_path: Path) -> Path:
    """Create test project with pytest.ini configuration and a test file that uses hardpy.get_start_args()."""  # noqa: E501
    subprocess.run([*HARDPY_INIT_CMD, str(tmp_path)], check=True)

    # Create pytest.ini with start arguments
    ini_content = """[pytest]
addopts = --hardpy-pt
        --hardpy-db-url http://dev:dev@localhost:5984/
        --hardpy-start-arg test_mode=debug
        --hardpy-start-arg device_id=DUT-006
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
import time

def test_ini_parameters():
    time.sleep(3)
    start_args = hardpy.get_start_args()
    assert start_args.get("test_mode") == "debug"
    assert start_args.get("device_id") == "DUT-007"
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
def test_with_hardpy_run_and_hardpy_start_stop(test_project: Path):
    """Test that hardpy run and hardpy start can be used together."""
    server_process = None
    try:
        server_process = run_hardpy_server(test_project)
        time.sleep(5)
        status = check_server_status()
        assert status.get("status") == "ready", f"Server not ready: {status}"

        result = run_command(["hardpy", "start"], cwd=str(test_project))
        assert result.returncode == 0, f"Command failed: {result.stderr.decode()}"
        stop_response = requests.get(
            f"{API_STOP_URL}",
            timeout=2,
        )
        assert stop_response.status_code == 200, "Test stop failed"

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
        status = check_server_status()
        while status.get("status") == "busy":
            time.sleep(3)
            status = check_server_status()
        config = CouchdbConfig(
            db_name="runstore",
            user="dev",
            password="dev",
            host="localhost",
            port=5984,
        )
        report = CouchdbReader(config).get_report_status("current")
        assert report == Status.PASSED

    finally:
        if server_process:
            server_process.terminate()
            server_process.wait(timeout=10)


@pytest.mark.manual
def test_with_hardpy_run_and_hardpy_start_with_ini_args_incorrect(
    test_project_with_ini_incorrect: Path,
):
    """Test that hardpy run and hardpy start can be used together."""
    server_process = None
    try:
        server_process = run_hardpy_server(test_project_with_ini_incorrect)
        time.sleep(5)
        status = check_server_status()
        assert status.get("status") == "ready", f"Server not ready: {status}"

        result = run_command(
            ["hardpy", "start"], cwd=str(test_project_with_ini_incorrect),
        )
        assert result.returncode == 0, f"Command failed: {result.stderr.decode()}"
        status = check_server_status()
        while status.get("status") == "busy":
            time.sleep(3)
            status = check_server_status()
        config = CouchdbConfig(
            db_name="runstore",
            user="dev",
            password="dev",
            host="localhost",
            port=5984,
        )
        report = CouchdbReader(config).get_report_status("current")
        assert report == Status.FAILED

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
        status = check_server_status()
        while status.get("status") == "busy":
            time.sleep(3)
            status = check_server_status()
        config = CouchdbConfig(
            db_name="runstore",
            user="dev",
            password="dev",
            host="localhost",
            port=5984,
        )
        report = CouchdbReader(config).get_report_status("current")
        assert report == Status.PASSED

    finally:
        if server_process:
            server_process.terminate()
            server_process.wait(timeout=10)


@pytest.mark.manual
def test_with_hardpy_run_and_hardpy_start_with_args_incorrect(
    test_project_with_args: Path,
):
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
                "device_id=DUT-006",
                "--arg",
                "retry_count=3",
            ],
            cwd=str(test_project_with_args),
        )
        assert result.returncode == 0, f"Command failed: {result.stderr.decode()}"
        status = check_server_status()
        while status.get("status") == "busy":
            time.sleep(3)
            status = check_server_status()
        config = CouchdbConfig(
            db_name="runstore",
            user="dev",
            password="dev",
            host="localhost",
            port=5984,
        )
        report = CouchdbReader(config).get_report_status("current")
        assert report == Status.FAILED

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
        status = check_server_status()
        while status.get("status") == "busy":
            time.sleep(3)
            status = check_server_status()
        config = CouchdbConfig(
            db_name="runstore",
            user="dev",
            password="dev",
            host="localhost",
            port=5984,
        )
        report = CouchdbReader(config).get_report_status("current")
        assert report == Status.PASSED

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
        status = check_server_status()
        while status.get("status") == "busy":
            time.sleep(3)
            status = check_server_status()
        config = CouchdbConfig(
            db_name="runstore",
            user="dev",
            password="dev",
            host="localhost",
            port=5984,
        )
        report = CouchdbReader(config).get_report_status("current")
        assert report == Status.PASSED

    finally:
        if server_process:
            server_process.terminate()
            server_process.wait(timeout=10)


@pytest.mark.manual
def test_with_hardpy_run_and_api_start_with_args_incorrect(
    test_project_with_args: Path,
):
    """Test that hardpy run and hardpy start can be used together."""
    server_process = None
    try:
        server_process = run_hardpy_server(test_project_with_args)
        time.sleep(5)
        status = check_server_status()
        assert status.get("status") == "ready", f"Server not ready: {status}"

        start_response = requests.get(
            f"{API_START_URL}?args=test_mode=debug&args=device_id=DUT-006&args=retry_count=3",
            timeout=5,
        )
        assert start_response.status_code == 200, "Test start failed"
        status = check_server_status()
        while status.get("status") == "busy":
            time.sleep(3)
            status = check_server_status()
        config = CouchdbConfig(
            db_name="runstore",
            user="dev",
            password="dev",
            host="localhost",
            port=5984,
        )
        report = CouchdbReader(config).get_report_status("current")
        assert report == Status.FAILED

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
