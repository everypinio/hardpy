import subprocess
import time
from pathlib import Path
from subprocess import PIPE, Popen, run as subprocess_run
from typing import TYPE_CHECKING

import psutil
import pytest

if TYPE_CHECKING:
    from pathlib import Path

RUN_CMD = ["hardpy", "run", "TEMPLATE_DIR"]
INIT_CMD = ["hardpy", "init", "TEMPLATE_DIR"]
ERROR_STR = "Specified port 8000 is already in use"
SUCCESS_STR = "test session starts"


def test_run_basic(process_killer, tmp_path: Path):
    """Test basic hardpy run command"""
    test_dir = _init_test_project(tmp_path, "test_basic")
    run_cmd = RUN_CMD.copy()
    run_cmd[2] = str(test_dir)

    process = Popen(run_cmd, stdout=PIPE, stderr=PIPE, text=True)
    time.sleep(3)

    output = _collect_n_string(process=process, n=15)

    assert ERROR_STR not in output, "Port 8000 is busy when it shouldn't be"
    assert SUCCESS_STR in output, "Failed to start test session"
    assert process.poll() is None, "Process terminated prematurely"

    psutil.Process(process.pid).kill()


def test_run_with_custom_port(process_killer, tmp_path: Path):
    """Test run with custom port"""
    test_dir = _init_test_project(tmp_path, "test_custom_port")
    custom_port = "8001"

    init_cmd = INIT_CMD.copy()
    init_cmd[2] = str(test_dir)
    init_cmd.extend(["--frontend-port", custom_port])
    subprocess_run(init_cmd, check=True, stdout=PIPE, stderr=PIPE)

    run_cmd = RUN_CMD.copy()
    run_cmd[2] = str(test_dir)

    process = Popen(run_cmd, stdout=PIPE, stderr=PIPE, text=True)
    time.sleep(3)

    output = _collect_n_string(process=process, n=15)
    assert f"Port {custom_port} is already in use" not in output
    assert SUCCESS_STR in output
    assert process.poll() is None

    psutil.Process(process.pid).kill()


def test_run_with_invalid_path():
    """Test run with invalid project path"""
    run_cmd = RUN_CMD.copy()
    run_cmd[2] = "/nonexistent/path/to/project"

    result = subprocess_run(run_cmd, stderr=PIPE, stdout=PIPE, text=True)

    print("=== INVALID PATH STDERR ===\n", result.stderr)

    assert result.returncode == 0


def _init_test_project(tmp_path: Path, name: str) -> str:
    test_dir = tmp_path / name
    test_dir.mkdir()

    init_cmd = INIT_CMD.copy()
    init_cmd[2] = str(test_dir)
    result = subprocess_run(init_cmd, check=True, stdout=PIPE, stderr=PIPE, text=True)

    if result.returncode != 0:
        pytest.fail(f"Project initialization failed: {result.stderr}")

    return str(test_dir)


def _collect_n_string(process: Popen, n: int) -> str:
    output = []
    try:
        if process.stdout:
            for i, line in enumerate(process.stdout):
                output.append(line.strip())
                if i >= n - 1:
                    break
    except ValueError:
        pass
    return "\n".join(output)
