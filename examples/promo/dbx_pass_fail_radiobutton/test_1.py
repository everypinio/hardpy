import pytest

from hardpy import (
    DialogBox,
    RadiobuttonWidget,
    run_dialog_box,
    set_message,
)

pytestmark = pytest.mark.module_name("Production Test - Operator Configuration")


@pytest.mark.case_name("Voltage Range Selection Test")
def test_voltage_range_selection():
    dbx = DialogBox(
        dialog_text='Select "230V" as operating voltage range and confirm with Pass.',
        title_bar="Operating Voltage Configuration",
        widget=RadiobuttonWidget(fields=["115V", "230V", "400V"]),
        pass_fail=True,
    )
    response = run_dialog_box(dbx)
    set_message(f"Test Result: {response.result}, Selected Voltage: {response.data}")
    assert response.result
    assert response.data == "230V", "Incorrect voltage range selected"
