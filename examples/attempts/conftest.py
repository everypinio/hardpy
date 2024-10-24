import datetime

import pytest

from hardpy import (
    CouchdbConfig,
    CouchdbLoader,
    get_current_report,
)


class CurrentMinute:
    """Class example."""

    def get_minute(self):
        """Get current minute."""
        current_time = datetime.datetime.now()  # noqa: DTZ005
        return int(current_time.strftime("%M"))


@pytest.fixture
def current_minute():
    current_time = CurrentMinute()
    yield current_time


def finish_executing():
    report = get_current_report()
    if report:
        loader = CouchdbLoader(CouchdbConfig())
        loader.load(report)


@pytest.fixture(scope="session", autouse=True)
def fill_actions_after_test(post_run_functions: list):
    post_run_functions.append(finish_executing)
    yield
