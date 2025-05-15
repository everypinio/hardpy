from __future__ import annotations

from http import HTTPStatus
from subprocess import PIPE, Popen, run as subprocess_run
from typing import TYPE_CHECKING
import getpass

import psutil
import pytest
import requests

if TYPE_CHECKING:
    from pathlib import Path
    from types import NoneType

PORT = 8000
RUN_CMD = ["hardpy", "run", "TEMPLATE_DIR"]
INIT_CMD = ["hardpy", "init", "TEMPLATE_DIR", "--frontend-port", str(PORT), "--frontend-host", getpass.getuser()]
ERROR_STR = f"Specified port {PORT} is already in use"


def test_single_start(process_killer: NoneType, tmp_path: Path):
    test_dir = _init_test_project(tmp_path, "test_1")
    RUN_CMD[2] = test_dir

    subprocess_run(INIT_CMD, check=True)
    process = Popen(RUN_CMD, stdout=PIPE, stderr=PIPE)

    collected_str = _collect_n_string(process=process, n=5)
    if ERROR_STR in collected_str:
        pytest.fail(ERROR_STR)

    launch_str = "Launch the HardPy operator panel"
    assert launch_str in collected_str

    psutil.Process(process.pid).kill()
    assert process.wait(3) is not None

def test_repeated_start(process_killer: NoneType, tmp_path: Path):
    test_dir = _init_test_project(tmp_path, "test_1")
    RUN_CMD[2] = test_dir

    process_1 = Popen(RUN_CMD, stdout=PIPE, stderr=PIPE)

    if ERROR_STR in _collect_n_string(process=process_1, n=5):
        pytest.fail(ERROR_STR)

    process_2 = Popen(RUN_CMD, stdout=PIPE, stderr=PIPE)
    assert ERROR_STR in _collect_n_string(process=process_2, n=5)

    psutil.Process(process_1.pid).kill()
    assert process_1.wait(3) is not None


def test_start_after_stop_single_port(process_killer: NoneType, tmp_path: Path):
    test_dir_1 = _init_test_project(tmp_path, "test_1")
    RUN_CMD[2] = test_dir_1

    process = Popen(RUN_CMD, stdout=PIPE, stderr=PIPE)

    if ERROR_STR in _collect_n_string(process=process, n=5):
        pytest.fail(ERROR_STR)

    psutil.Process(process.pid).kill()
    assert process.wait(3) is not None

    test_dir_2 = _init_test_project(tmp_path, "test_2")
    RUN_CMD[2] = test_dir_2

    process = Popen(RUN_CMD, stdout=PIPE, stderr=PIPE)

    if ERROR_STR in _collect_n_string(process=process, n=5):
        pytest.fail(ERROR_STR)

    psutil.Process(process.pid).kill()
    assert process.wait(3) is not None


def _init_test_project(tmp_path: Path, name: str) -> str:
    test1_dir = tmp_path / name
    test1_dir.mkdir()

    INIT_CMD[2] = str(test1_dir)
    subprocess_run(INIT_CMD, check=True)

    return str(test1_dir)

def _collect_n_string(process: Popen, n: int) -> str:
    """Collect n string from process output."""
    output = []
    if process.stdout:
        max_lines = n
        for i, line in enumerate(process.stdout):
            output.append(line.strip().decode("utf-8"))
            if i >= max_lines - 1:
                break
    return "\n".join(output)
