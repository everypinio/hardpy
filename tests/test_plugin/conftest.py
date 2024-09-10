import os
import pytest

from hardpy.config import ConfigManager

pytest_plugins = "pytester"


@pytest.fixture
def hardpy_opts():
    db_host = os.environ.get("COUCH_DB_HOST")
    config_data = ConfigManager().get_config()
    return [
        "--hardpy-db-url",
        config_data.database.connection_url() if db_host is None else db_host,
        "--hardpy-pt"
    ]
