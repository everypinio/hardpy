import logging
import os

import pytest

from jig.common import log_config


@pytest.fixture(autouse=True)
def _isolate_logging_state():
    root_logger = logging.getLogger()
    level = root_logger.level
    handlers = root_logger.handlers[:]
    env_level = os.environ.get(log_config.LOG_LEVEL_ENV_VAR)

    yield

    root_logger.handlers = handlers
    root_logger.setLevel(level)
    if env_level is None:
        os.environ.pop(log_config.LOG_LEVEL_ENV_VAR, None)
    else:
        os.environ[log_config.LOG_LEVEL_ENV_VAR] = env_level


def test_level_defaults_to_warning(monkeypatch: pytest.MonkeyPatch):
    monkeypatch.delenv(log_config.LOG_LEVEL_ENV_VAR, raising=False)

    assert log_config.resolve_level() == logging.WARNING


def test_level_comes_from_the_environment(monkeypatch: pytest.MonkeyPatch):
    monkeypatch.setenv(log_config.LOG_LEVEL_ENV_VAR, "info")

    assert log_config.resolve_level() == logging.INFO


def test_numeric_environment_level_is_accepted(monkeypatch: pytest.MonkeyPatch):
    monkeypatch.setenv(log_config.LOG_LEVEL_ENV_VAR, str(logging.ERROR))

    assert log_config.resolve_level() == logging.ERROR


def test_unknown_environment_level_falls_back_to_the_default(
    monkeypatch: pytest.MonkeyPatch,
):
    monkeypatch.setenv(log_config.LOG_LEVEL_ENV_VAR, "chatty")

    assert log_config.resolve_level() == logging.WARNING


def test_verbose_flag_overrides_the_environment(monkeypatch: pytest.MonkeyPatch):
    monkeypatch.setenv(log_config.LOG_LEVEL_ENV_VAR, "error")

    assert log_config.resolve_level(is_verbose=True) == logging.INFO


def test_configure_sets_the_root_logger_level(monkeypatch: pytest.MonkeyPatch):
    monkeypatch.delenv(log_config.LOG_LEVEL_ENV_VAR, raising=False)

    log_config.configure(logging.DEBUG)

    assert logging.getLogger().getEffectiveLevel() == logging.DEBUG


def test_configure_exports_the_level_to_child_processes(
    monkeypatch: pytest.MonkeyPatch,
):
    monkeypatch.delenv(log_config.LOG_LEVEL_ENV_VAR, raising=False)

    log_config.configure(logging.DEBUG)

    assert log_config.resolve_level() == logging.DEBUG


def test_verbosity_follows_the_configured_level(monkeypatch: pytest.MonkeyPatch):
    monkeypatch.delenv(log_config.LOG_LEVEL_ENV_VAR, raising=False)

    log_config.configure(logging.WARNING)
    assert log_config.is_verbose() is False

    log_config.configure(logging.INFO)
    assert log_config.is_verbose() is True


def test_uvicorn_stays_quiet_below_info():
    assert log_config.uvicorn_level(logging.WARNING) == log_config.UVICORN_QUIET_LEVEL


def test_uvicorn_level_follows_verbose_levels():
    assert log_config.uvicorn_level(logging.DEBUG) == "debug"
    assert log_config.uvicorn_level(logging.INFO) == "info"
