from pathlib import Path

import pytest

from hardpy.common.config import ConfigManager

pytest_plugins = "pytester"


@pytest.fixture
def hardpy_opts():
    config_data = ConfigManager().read_config(
        Path(__file__).parent.resolve(),
    )
    if not config_data:
        raise Exception("Config not found")  # noqa: EM101, TRY002, TRY003
    return ["--hardpy-db-url", config_data.database.connection_url(), "--hardpy-pt"]
