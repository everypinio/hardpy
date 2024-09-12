import pytest

from hardpy.common.config import ConfigManager

pytest_plugins = "pytester"


@pytest.fixture
def hardpy_opts():
    config_data = ConfigManager().get_config()
    return [
        "--hardpy-db-url",
        config_data.database.connection_url(),
        "--hardpy-pt"
    ]
