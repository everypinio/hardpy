import pytest
from driver_example import DriverExample  # type: ignore

from hardpy import (
    CouchdbConfig,
    CouchdbLoader,
    get_current_report,
)


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


@pytest.fixture
def start_params(request):
    """Fixture to access hardpy start parameters."""
    start_params = request.config.getoption("--hardpy-start-arg") or []

    params_dict = {}
    for param in start_params:
        if "=" in param:
            key, value = param.split("=", 1)
            params_dict[key] = value

    return params_dict
