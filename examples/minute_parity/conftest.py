import logging

import pytest
from driver_example import DriverExample

from hardpy import (
    CouchdbConfig,
    CouchdbLoader,
    get_current_report,
)


@pytest.fixture(scope="module")
def module_log(request: pytest.FixtureRequest):
    log_name = request.module.__name__
    yield logging.getLogger(log_name)  # noqa: PT022


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
    yield  # noqa: PT022
