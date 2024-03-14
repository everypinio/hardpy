import pytest
import os

from hardpy.pytest_hardpy.utils.config_data import ConfigData

pytest_plugins = "pytester"


@pytest.fixture()
def hardpy_init(pytester):
    # create a temporary conftest.py file
    pytester.makeconftest(
        """
        import pytest

        from hardpy import HardpyPlugin


        def pytest_configure(config: pytest.Config):
            config.pluginmanager.register(HardpyPlugin())
    """
    )


def hardpy_connect_db():
    db_host = os.environ.get("COUCH_DB_HOST")
    if db_host is None:
        config_data = ConfigData()
        return config_data.db_host
    return db_host


def hardpy_dbh():
    return "--hardpy-dbh"
