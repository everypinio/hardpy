from http import HTTPStatus

import pytest
from driver_example import DriverExample  # type: ignore

from hardpy import (
    StandCloudError,
    StandCloudLoader,
    get_current_report,
    set_operator_message,
)


@pytest.fixture(scope="session")
def driver_example():
    example = DriverExample()
    yield example


def finish_executing():
    report = get_current_report()
    if report:
        try:
            loader = StandCloudLoader()
            response = loader.load(report)
            if response.status_code != HTTPStatus.CREATED:
                set_operator_message(
                    "Report not uploaded to StandCloud, "
                    f"status code: {response.status_code}, text: {response.text}",
                )
        except StandCloudError as exc:
            set_operator_message(f"{exc}")


@pytest.fixture(scope="session", autouse=True)
def fill_actions_after_test(post_run_functions: list):
    post_run_functions.append(finish_executing)
    yield
