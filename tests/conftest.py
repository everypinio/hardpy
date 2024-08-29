import os
import pytest

from hardpy.config import ConfigManager

pytest_plugins = "pytester"


@pytest.fixture
def hardpy_opts():
    db_host = os.environ.get("COUCH_DB_HOST")
    config_data = ConfigManager().get_config()
    return [
        # TODO:
        "--hardpy-dbh",
        config_data.database.host if db_host is None else db_host,
        "--hardpy-pt"
    ]
