import logging

import pytest

from hardpy import CouchdbLoader, CouchdbConfig, get_current_report, set_operator_msg
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
    try:
        raise ValueError("Test failed")
    except ValueError as e:
        set_operator_msg(msg=str(e), title="Message title")
    report = get_current_report()
    if report:
        loader = CouchdbLoader(CouchdbConfig())
        loader.load(report)


@pytest.fixture(scope="session", autouse=True)
def fill_actions_after_test(post_run_functions: list):
    post_run_functions.append(finish_executing)
    yield
