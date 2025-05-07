import subprocess
import time
from pathlib import Path

import requests

HARDPY_COMMAND = ["hardpy", "init"]
HARDPY_RUN_COMMAND = ["hardpy", "run"]
PORT = 8000


def test_basic_startup_simple(tmp_path: Path):
    subprocess.run(
        [*HARDPY_COMMAND, tmp_path, "--frontend-port", str(PORT)], check=True,
    )
    process = subprocess.Popen(
        [*HARDPY_RUN_COMMAND, tmp_path], stdout=subprocess.PIPE, stderr=subprocess.PIPE,
    )
    time.sleep(5)
    response = requests.get(f"http://localhost:{PORT}", timeout=10)
    time.sleep(5)
    assert response.status_code == 200
    process.kill()
    time.sleep(5)
    assert process.poll() in [1, -9]
