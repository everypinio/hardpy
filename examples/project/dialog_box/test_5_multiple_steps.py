import pytest
from hardpy import run_dialog_box
from hardpy.pytest_hardpy.utils.dialog_box import (
    DialogBoxWidget,
    DialogBoxWidgetType,
    DialogBox,
    MultistepInfo,
)


@pytest.mark.case_name("Multistep")
def test_multiple_steps():
    dbx = DialogBox(
        dialog_text="Multistep",
        widget=DialogBoxWidget(
            DialogBoxWidgetType.MULTISTEP,
            MultistepInfo(fields=["one", "two", "three"]),
        ),
    )
    response = run_dialog_box(dbx)
    assert response is None