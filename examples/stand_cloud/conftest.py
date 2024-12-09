import logging

import pytest
from driver_example import DriverExample  # type: ignore

from hardpy import (
    StandCloudError,
    StandCloudLoader,
    get_current_report,
    set_operator_message,
)


@pytest.fixture(scope="module")
def module_log(request: pytest.FixtureRequest):
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
        loader = StandCloudLoader()
        try:
            loader.healthcheck()
            loader.load(report)
        except StandCloudError as exc:
            set_operator_message(f"{exc}")
            return


@pytest.fixture(scope="session", autouse=True)
def fill_actions_after_test(post_run_functions: list):
    post_run_functions.append(finish_executing)
    yield
