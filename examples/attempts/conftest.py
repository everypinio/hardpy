import datetime
import logging

import pytest

from hardpy import (
    CouchdbConfig,
    CouchdbLoader,
    get_current_report,
)


@pytest.fixture(scope="module")
def module_log(request: pytest.FixtureRequest):
    log_name = request.module.__name__
    yield logging.getLogger(log_name)


@pytest.fixture(scope="session")
def current_minute():
    current_time = datetime.datetime.now()  # noqa: DTZ005
    return int(current_time.strftime("%M"))


def finish_executing():
    report = get_current_report()
    if report:
        loader = CouchdbLoader(CouchdbConfig())
        loader.load(report)


@pytest.fixture(scope="session", autouse=True)
def fill_actions_after_test(post_run_functions: list):
    post_run_functions.append(finish_executing)
    yield
