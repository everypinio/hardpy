from __future__ import annotations

import os

import psutil
import pytest


@pytest.fixture(scope="session", autouse=True)
def clear_port():
    """Clear test port."""
    pid = _get_pid_by_port(port=8000)
    if pid is None:
        return False

    process = psutil.Process(pid)
    process.terminate()

    try:
        process.wait(timeout=3)
    except psutil.TimeoutExpired:
        process.kill()


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


def _get_pid_by_port(port: int) -> int | None:
    for conn in psutil.net_connections():
        if conn.laddr and conn.laddr.port == port:
            return conn.pid
    return None
