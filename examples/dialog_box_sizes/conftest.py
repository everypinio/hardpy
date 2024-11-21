import pytest

from hardpy import (
    get_current_report,
    set_operator_message,
)


def finish_executing():
    report = get_current_report()

    if report.status == "passed": # type: ignore
        set_operator_message(
            "Тестирование завершилось успешно. Ошибок не обнаружено.",
        )
        set_operator_message(
            "Маркируйте плату согласно инструкции раздела 'Маркировка' ",
            "в hardpy_encoder/README.md.",
        )

    elif report.status == "failed": # type: ignore
        set_operator_message(
            "Тестирование провалено. Обнаружены ошибки.",
        )


@pytest.fixture(scope="session", autouse=True)
def fill_actions_after_test(post_run_functions: list):
    post_run_functions.append(finish_executing)
    yield