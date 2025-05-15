import os

import psutil
import pytest


@pytest.fixture
def process_killer():
    """Kill the process if tests are completed incorrectly.

    Must be called as the argument of the `hardpy run` test.
    """
    current_pid = os.getpid()
    yield

    children: list[psutil.Process] = []
    for proc in psutil.process_iter():
        try:
            if proc.ppid() == current_pid:
                children.append(proc)
        except (psutil.NoSuchProcess, psutil.AccessDenied):  # noqa: PERF203
            continue

    for child in children:
        child.kill()
