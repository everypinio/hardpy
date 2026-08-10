# Copyright (c) 2026 Everypin
# GNU General Public License v3.0 (see LICENSE or https://www.gnu.org/licenses/gpl-3.0.txt)
"""Console verbosity of Jig and of the processes it spawns."""

from __future__ import annotations

import logging
import os

LOG_LEVEL_ENV_VAR = "JIG_LOG_LEVEL"
DEFAULT_LEVEL = logging.WARNING
VERBOSE_LEVEL = logging.INFO
LOG_FORMAT = "%(asctime)s %(levelname)s:\t %(message)s"

UVICORN_QUIET_LEVEL = "critical"


def resolve_level(*, is_verbose: bool = False) -> int:
    """Resolve the log level to use.

    The verbose flag takes precedence over the environment variable,
    which takes precedence over the default level. Set the environment
    variable to `debug` for a level deeper than the verbose flag.

    Args:
        is_verbose (bool): value of the `--verbose` command line flag

    Returns:
        int: logging level
    """
    if is_verbose:
        return VERBOSE_LEVEL
    return _level_from_env_value(os.environ.get(LOG_LEVEL_ENV_VAR))


def configure(level: int) -> None:
    """Configure the root logger and expose the level to child processes.

    Args:
        level (int): logging level
    """
    logging.basicConfig(level=level, format=LOG_FORMAT, force=True)
    os.environ[LOG_LEVEL_ENV_VAR] = _level_to_env_value(level)


def is_verbose() -> bool:
    """Check whether informational output is wanted on the console.

    Returns:
        bool: True when the effective level lets INFO records through
    """
    return logging.getLogger().getEffectiveLevel() <= logging.INFO


def uvicorn_level(level: int) -> str:
    """Convert a logging level into a uvicorn log level name.

    Args:
        level (int): logging level

    Returns:
        str: uvicorn log level name
    """
    if level > logging.INFO:
        return UVICORN_QUIET_LEVEL
    return logging.getLevelName(level).lower()


def _level_from_env_value(value: str | None) -> int:
    if not value:
        return DEFAULT_LEVEL

    stripped = value.strip()
    if stripped.isdigit():
        return int(stripped)

    level = logging.getLevelName(stripped.upper())
    return level if isinstance(level, int) else DEFAULT_LEVEL


def _level_to_env_value(level: int) -> str:
    name = logging.getLevelName(level)
    return name if _level_from_env_value(name) == level else str(level)
