import os
import pytest

from hardpy.pytest_hardpy.utils.config_data import ConfigData

pytest_plugins = "pytester"


@pytest.fixture
def hardpy_opts():
    db_host = os.environ.get("COUCH_DB_HOST")
    config_data = ConfigData()
    return [
        "--hardpy-dbh",
        config_data.db_host if db_host is None else db_host,
        "--hardpy-pt"
    ]
