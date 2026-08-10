import logging
import sys
from pathlib import Path

import pytest

from jig.pytest_jig import quiet_process

WAIT_TIMEOUT = 30
NOISY_CHILD = "import sys; print('collected tests'); sys.stderr.write('warning\\n')"
FAILING_CHILD = "import sys; print('boom'); sys.exit(3)"


def child_command(source: str) -> list[str]:
    return [sys.executable, "-c", source]


def messages_of_level(caplog: pytest.LogCaptureFixture, level: int) -> str:
    return "\n".join(
        record.getMessage() for record in caplog.records if record.levelno == level
    )


def test_quiet_process_keeps_its_output_off_the_console(
    tmp_path: Path,
    capfd: pytest.CaptureFixture,
):
    spawned = quiet_process.spawn(child_command(NOISY_CHILD), tmp_path)
    spawned.wait(timeout=WAIT_TIMEOUT)

    captured = capfd.readouterr()
    assert "collected tests" not in captured.out
    assert "warning" not in captured.err


def test_quiet_process_output_is_logged_for_debugging(
    tmp_path: Path,
    caplog: pytest.LogCaptureFixture,
):
    caplog.set_level(logging.DEBUG, logger=quiet_process.logger.name)

    spawned = quiet_process.spawn(child_command(NOISY_CHILD), tmp_path)
    spawned.wait(timeout=WAIT_TIMEOUT)

    assert "collected tests" in messages_of_level(caplog, logging.DEBUG)


def test_failing_quiet_process_is_reported_as_an_error(
    tmp_path: Path,
    caplog: pytest.LogCaptureFixture,
):
    caplog.set_level(logging.DEBUG, logger=quiet_process.logger.name)

    spawned = quiet_process.spawn(child_command(FAILING_CHILD), tmp_path)
    exit_code = spawned.wait(timeout=WAIT_TIMEOUT)

    errors = messages_of_level(caplog, logging.ERROR)
    assert exit_code == 3
    assert "exit code 3" in errors
    assert "boom" in errors


def test_verbose_process_writes_to_the_console(
    tmp_path: Path,
    capfd: pytest.CaptureFixture,
):
    spawned = quiet_process.spawn(
        child_command(NOISY_CHILD),
        tmp_path,
        is_quiet=False,
    )
    spawned.wait(timeout=WAIT_TIMEOUT)

    captured = capfd.readouterr()
    assert "collected tests" in captured.out
