from __future__ import annotations

import time
from typing import TYPE_CHECKING

import pytest
import requests
from jig_server import JigServer

from jig.pytest_jig.utils.const import TestStatus as Status

if TYPE_CHECKING:
    from pathlib import Path

API_START_URL = "http://localhost:8000/api/start"


@pytest.mark.manual
def test_jig_run_and_jig_start(project_dir: Path):
    """Test that jig run and jig start can be used together."""
    server = JigServer(project_dir)
    server_process = server.start_server()
    try:
        server.wait_until_ready()

        result = server.run_command(["jig", "start"], cwd=str(project_dir))
        assert result.returncode == 0, f"Command failed: {result.stderr.decode()}"
        assert server.check_status().get("status") == "busy"
        server.wait_until_test_complete()
        assert server.get_test_result() == Status.PASSED
    finally:
        server_process.terminate()
        server_process.wait(timeout=10)


@pytest.mark.manual
def test_jig_run_and_jig_start_stop(project_dir: Path):
    """Test that jig run and jig start can be used together."""
    server = JigServer(project_dir)
    server_process = server.start_server()
    try:
        server.wait_until_ready()

        result = server.run_command(["jig", "start"], cwd=str(project_dir))
        assert result.returncode == 0, f"Command failed: {result.stderr.decode()}"
        assert server.check_status().get("status") == "busy"
        time.sleep(3)

        result = server.run_command(["jig", "stop"], cwd=str(project_dir))
        assert result.returncode == 0, f"Command failed: {result.stderr.decode()}"
        time.sleep(1)
        assert server.get_test_result() == Status.STOPPED
    finally:
        server_process.terminate()
        server_process.wait(timeout=10)


@pytest.mark.manual
def test_jig_run_and_jig_start_ini_args(project_dir_with_ini: Path):
    """Test that jig run and jig start can be used together."""
    server = JigServer(project_dir_with_ini)
    server_process = server.start_server()
    try:
        server.wait_until_ready()

        result = server.run_command(["jig", "start"], cwd=str(project_dir_with_ini))
        assert result.returncode == 0, f"Command failed: {result.stderr.decode()}"

        server.wait_until_test_complete()
        time.sleep(2)
        assert server.get_test_result() == Status.PASSED
    finally:
        server_process.terminate()
        server_process.wait(timeout=10)


@pytest.mark.manual
def test_jig_run_and_jig_start_ini_args_incorrect(
    project_dir_with_ini_incorrect: Path,
):
    """Test that jig run and jig start can be used together."""
    server = JigServer(project_dir_with_ini_incorrect)
    server_process = server.start_server()
    try:
        server.wait_until_ready()

        result = server.run_command(
            ["jig", "start"],
            cwd=str(project_dir_with_ini_incorrect),
        )
        assert result.returncode == 0, f"Command failed: {result.stderr.decode()}"

        server.wait_until_test_complete()
        assert server.get_test_result() == Status.FAILED
    finally:
        server_process.terminate()
        server_process.wait(timeout=10)


@pytest.mark.manual
def test_jig_run_and_jig_start_args(project_dir_with_args: Path):
    """Test that jig run and jig start can be used together."""
    server = JigServer(project_dir_with_args)
    server_process = server.start_server()
    try:
        server.wait_until_ready()

        result = server.run_command(
            [
                "jig",
                "start",
                "--arg",
                "test_mode=debug",
                "--arg",
                "device_id=DUT-007",
                "--arg",
                "retry_count=3",
            ],
            cwd=str(project_dir_with_args),
        )

        assert result.returncode == 0, f"Command failed: {result.stderr.decode()}"
        server.wait_until_test_complete()
        assert server.get_test_result() == Status.PASSED
    finally:
        server_process.terminate()
        server_process.wait(timeout=10)


@pytest.mark.manual
def test_jig_run_and_jig_start_args_incorrect(project_dir_with_args: Path):
    """Test that jig run and jig start can be used together."""
    server = JigServer(project_dir_with_args)
    server_process = server.start_server()
    try:
        server.wait_until_ready()

        result = server.run_command(
            [
                "jig",
                "start",
                "--arg",
                "test_mode=debug",
                "--arg",
                "device_id=DUT-006",
                "--arg",
                "retry_count=3",
            ],
            cwd=str(project_dir_with_args),
        )

        assert result.returncode == 0, f"Command failed: {result.stderr.decode()}"
        server.wait_until_test_complete()
        assert server.get_test_result() == Status.FAILED
    finally:
        server_process.terminate()
        server_process.wait(timeout=10)


@pytest.mark.manual
def test_jig_run_and_pytest_args(project_dir_with_args: Path):
    """Test that jig run and jig start can be used together."""
    server = JigServer(project_dir_with_args)
    server_process = server.start_server()
    try:
        server.wait_until_ready()

        result = server.run_command(
            [
                "pytest",
                "--jig-start-arg",
                "test_mode=debug",
                "--jig-start-arg",
                "device_id=DUT-007",
                "--jig-start-arg",
                "retry_count=3",
            ],
            cwd=str(project_dir_with_args),
        )

        assert result.returncode == 0, f"Command failed: {result.stderr.decode()}"
        server.wait_until_test_complete()
        assert server.get_test_result() == Status.PASSED
    finally:
        server_process.terminate()
        server_process.wait(timeout=10)


@pytest.mark.manual
def test_jig_run_and_api_start_args(project_dir_with_args: Path):
    """Test that jig run and jig start can be used together."""
    server = JigServer(project_dir_with_args)
    server_process = server.start_server()
    try:
        server.wait_until_ready()

        start_response = requests.get(
            f"{API_START_URL}?args=test_mode=debug&args=device_id=DUT-007&args=retry_count=3",
            timeout=5,
        )
        assert start_response.status_code == 200, "Test start failed"

        server.wait_until_test_complete()
        assert server.get_test_result() == Status.PASSED
    finally:
        server_process.terminate()
        server_process.wait(timeout=10)


@pytest.mark.manual
def test_jig_run_and_api_start_args_incorrect(project_dir_with_args: Path):
    """Test that jig run and jig start can be used together."""
    server = JigServer(project_dir_with_args)
    server_process = server.start_server()
    try:
        server.wait_until_ready()

        start_response = requests.get(
            f"{API_START_URL}?args=test_mode=debug&args=device_id=DUT-006&args=retry_count=3",
            timeout=5,
        )
        assert start_response.status_code == 200, "Test start failed"

        server.wait_until_test_complete()
        assert server.get_test_result() == Status.FAILED
    finally:
        server_process.terminate()
        server_process.wait(timeout=10)
