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


@pytest.fixture(scope="session", autouse=True)
def fill_actions_after_test(post_run_functions: list):
    post_run_functions.append(finish_executing)
    set_operator_message(
        msg="Testing was successful",
        title="Operator message",
    )
    set_operator_message(
        msg="Press the X button\nPress the X button\nPress the X button\nPress the X button\nPress the X button\nPress the X button\nPress the X button\nPress the X button\nPress the X button\nPress the X button\nPress the X button\nPress the X button\nPress the X button\nPress the X button\nPress the X button\nPress the X button\nPress the X button\nPress the X button\nPress the X button\nPress the X button\nPress the X button\nPress the X button\nPress the X button\nPress the X button\nPress the X button\nPress the X button\nPress the X button\nPress the X button\nPress the X button\nPress the X button\nPress the X button\nPress the X button\nPress the X button\nPress the X button\nPress the X button\n",  # noqa: E501
        title="Operator message",
    )
    yield
