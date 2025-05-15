import subprocess
import time
from pathlib import Path

import requests

HARDPY_COMMAND = ["hardpy", "init"]
HARDPY_RUN_COMMAND = ["hardpy", "run"]
PORT = 8000


def test_basic_startup_simple(tmp_path: Path):
    test1_dir = tmp_path / "test_1"
    test1_dir.mkdir()

    subprocess.run(
        [*HARDPY_COMMAND, str(test1_dir), "--frontend-port", str(PORT)],
        check=True,
    )
    process = subprocess.Popen(
        [*HARDPY_RUN_COMMAND, str(test1_dir)],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    time.sleep(5)
    response = requests.get(f"http://localhost:{PORT}", timeout=10)
    time.sleep(5)
    assert response.status_code == 200
    process.kill()
    time.sleep(5)
    assert process.poll() in [-9, 1]

    test2_dir = tmp_path / "test_2"
    test2_dir.mkdir()

    subprocess.run(
        [
            *HARDPY_COMMAND,
            str(test2_dir),
            "--frontend-port",
            str(PORT),
            "--tests-name",
            "Test name",
        ],
        check=True,
    )
    process = subprocess.Popen(
        [*HARDPY_RUN_COMMAND, str(test2_dir)],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    time.sleep(5)
    response = requests.get(f"http://localhost:{PORT}", timeout=10)
    time.sleep(5)
    assert response.status_code == 200
    process.kill()
    time.sleep(5)
    assert process.poll() in [-9, 1]
