import pytest

from hardpy import (
    CouchdbConfig,
    CouchdbLoader,
    get_current_report,
)


def save_report_to_couchdb() -> None:  # noqa: D103
    report = get_current_report()
    if report:
        loader = CouchdbLoader(CouchdbConfig())
        loader.load(report)


@pytest.fixture(scope="session", autouse=True)
def fill_actions_after_test(post_run_functions: list):  # noqa: ANN201, D103
    post_run_functions.append(save_report_to_couchdb)
    yield  # noqa: PT022
