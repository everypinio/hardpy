import subprocess
import time

import requests

HARDPY_COMMAND = ["hardpy", "init"]
HARDPY_RUN_COMMAND = ["hardpy", "run"]
PORT = 8000


def test_basic_startup_simple():
    subprocess.run(
        [*HARDPY_COMMAND, "test_1", "--frontend-port", str(PORT)],
        check=True,
    )
    process = subprocess.Popen(
        [*HARDPY_RUN_COMMAND, "test_1"],
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
    subprocess.run(
        [
            *HARDPY_COMMAND,
            "test_2",
            "--frontend-port",
            str(PORT),
            "--tests-name",
            "Test name",
        ],
        check=True,
    )
    process = subprocess.Popen(
        [*HARDPY_RUN_COMMAND, "test_2"],
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
