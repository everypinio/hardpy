import pytest
import hardpy
from hardpy.pytest_hardpy.pytest_call import (
    DialogBoxData,
    DialogBoxWidget,
    DialogBoxWidgetType,
)


@pytest.mark.case_name("Test base dialog box")
def test_base_dialog_box():
    info = DialogBoxData(
        title_bar="My first dialog box",
        dialog_text="Enjoy this dialog box",
        widget_info=None,
    )
    response = hardpy.run_dialog_box(info)
    assert response == "ok"


@pytest.mark.case_name("Test dialog box with text input")
def test_dialog_box_with_text_input():
    info = DialogBoxData(
        title_bar="My first dialog box",
        dialog_text="Тут введите текст",
        widget_info=DialogBoxWidget(
            widget_type=DialogBoxWidgetType.TEXT_INPUT, widget_info="widget_text дошел"
        ),
    )
    response = hardpy.run_dialog_box(info)
    assert response == "ok"


@pytest.mark.case_name("Test dialog box with num input")
def test_dialog_box_with_num_input():
    info = DialogBoxData(
        title_bar="My first dialog box",
        dialog_text="Тут введите число",
        widget_info=DialogBoxWidget(
            widget_type=DialogBoxWidgetType.NUMERIC_INPUT,
            widget_info="чиселко введите, будьте добры",
        ),
    )
    response = hardpy.run_dialog_box(info)
    assert response == "ok"
