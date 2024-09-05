import logging

import pytest

from hardpy import (
    CouchdbLoader,
    CouchdbConfig,
    get_current_report,
)
from driver_example import DriverExample


@pytest.fixture(scope="module")
def module_log(request):
    log_name = request.module.__name__
    yield logging.getLogger(log_name)


@pytest.fixture(scope="session")
def driver_example():
    example = DriverExample()
    yield example
    example.random_method()


def finish_executing():
    report = get_current_report()
    if report:
        loader = CouchdbLoader(CouchdbConfig())
        loader.load(report)


@pytest.fixture(scope="session", autouse=True)
def fill_actions_after_test(post_run_functions: list):
    post_run_functions.append(finish_executing)
    yield
