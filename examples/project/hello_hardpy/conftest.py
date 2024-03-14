import pytest
from hardpy import HardpyPlugin


def pytest_configure(config: pytest.Config):
    config.pluginmanager.register(HardpyPlugin())
