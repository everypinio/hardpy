import pytest
from utils.system_driver import SystemDriver

from hardpy import (
    CouchdbConfig,
    CouchdbLoader,
    get_current_report,
)


@pytest.fixture(scope="session")
def system_driver():
    example = SystemDriver()
    yield example
    example.disconnect()


def finish_executing():
    report = get_current_report()
    if report:
        loader = CouchdbLoader(CouchdbConfig())
        loader.load(report)


@pytest.fixture(scope="session", autouse=True)
def fill_actions_after_test(post_run_functions: list):
    post_run_functions.append(finish_executing)
    yield
