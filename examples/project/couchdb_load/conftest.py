import pytest

from hardpy import (
    HardpyPlugin,
    CouchdbLoader,
    CouchdbConfig,
    get_current_report,
)


def pytest_configure(config: pytest.Config):
    config.pluginmanager.register(HardpyPlugin())


def save_report_to_couchdb():
    report = get_current_report()
    if report:
        loader = CouchdbLoader(CouchdbConfig())
        loader.load(report)


@pytest.fixture(scope="session", autouse=True)
def fill_actions_after_test(post_run_functions: list):
    post_run_functions.append(save_report_to_couchdb)
    yield
