import pytest

from hardpy import (
    CouchdbConfig,
    CouchdbLoader,
    get_current_report,
    set_operator_message,
)


def finish_executing():
    report = get_current_report()
    try:
        if report:
            loader = CouchdbLoader(CouchdbConfig(port=5986))
            loader.load(report)
            set_operator_message(
                msg="Saving report was successful",
                title="Operator message",
            )
    except RuntimeError as e:
        set_operator_message(
            msg="The report was not recorded with error " + str(e) + ".",
            title="Operator message",
        )


def test_end_message():
    set_operator_message(
        msg="Testing completed",
        title="Operator message",
    )


def test_1_message():
    set_operator_message(
        msg="Testing 1",
        title="Operator message",
    )


def test_2_message():
    set_operator_message(
        msg="Testing 2",
        title="Operator message",
    )


@pytest.fixture(scope="session", autouse=True)
def fill_actions_after_test(post_run_functions: list):
    post_run_functions.append(finish_executing)
    post_run_functions.append(test_end_message)
    yield


@pytest.fixture(scope="session", autouse=True)
def fill_other_actions_after_test(post_run_functions: list):
    post_run_functions.append(test_1_message)
    post_run_functions.append(test_2_message)
    yield
