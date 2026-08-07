"""Dialog boxes, one per widget type, and operator messages."""

import pytest
from simulated_device import SimulatedDevice  # type: ignore[import-not-found]

from hardpy import (
    CheckboxWidget,
    ComparisonOperation as CompOp,
    DialogBox,
    ErrorCode,
    HTMLComponent,
    ImageComponent,
    MultistepWidget,
    NumericInputWidget,
    NumericMeasurement,
    RadiobuttonWidget,
    StepWidget,
    StringMeasurement,
    TextInputWidget,
    run_dialog_box,
    set_case_artifact,
    set_case_measurement,
)

pytestmark = pytest.mark.module_name("Operator interaction")

AMBIENT_TEMPERATURE_LIMITS_C = (15.0, 30.0)
REQUIRED_ACCESSORIES = ["Antenna", "Power cable"]
VISUAL_INSPECTION_ERROR_CODE = 101


@pytest.mark.case_name("Visual inspection")
def test_visual_inspection():
    """Ask the operator to judge the board, with pass and fail buttons."""
    dialog_box = DialogBox(
        title_bar="Visual inspection",
        dialog_text="Compare the board with the reference picture.",
        image=ImageComponent(address="assets/test.png", width=50),
        pass_fail=True,
    )
    response = run_dialog_box(dialog_box)

    assert response.result, ErrorCode(
        VISUAL_INSPECTION_ERROR_CODE,
        "The operator rejected the board",
    )


@pytest.mark.case_name("Serial number")
def test_serial_number(device: SimulatedDevice):
    """Read a string from the operator."""
    dialog_box = DialogBox(
        title_bar="Serial number",
        dialog_text="Type the serial number printed on the label.",
        widget=TextInputWidget(),
    )
    typed_serial_number = run_dialog_box(dialog_box)

    measurement = StringMeasurement(
        name="Typed serial number",
        value=typed_serial_number,
        operation=CompOp.EQ,
        comparison_value=device.serial_number,
        casesensitive=False,
    )
    set_case_measurement(measurement)

    assert measurement.result, f"Expected {device.serial_number}"


@pytest.mark.case_name("Ambient temperature")
def test_ambient_temperature():
    """Read a number from the operator."""
    lower_limit, upper_limit = AMBIENT_TEMPERATURE_LIMITS_C
    dialog_box = DialogBox(
        title_bar="Ambient temperature",
        dialog_text="Enter the temperature shown by the bench thermometer.",
        widget=NumericInputWidget(),
    )
    temperature = run_dialog_box(dialog_box)

    measurement = NumericMeasurement(
        name="Ambient temperature",
        value=temperature,
        unit="°C",
        operation=CompOp.GELE,
        lower_limit=lower_limit,
        upper_limit=upper_limit,
    )
    set_case_measurement(measurement)

    assert measurement.result, f"Temperature {temperature} °C is outside the limits"


@pytest.mark.case_name("Connector type")
def test_connector_type():
    """Let the operator pick one option."""
    dialog_box = DialogBox(
        title_bar="Connector type",
        dialog_text="Select the connector mounted on the board.",
        widget=RadiobuttonWidget(fields=["SMA", "U.FL", "None"]),
    )
    connector = run_dialog_box(dialog_box)
    set_case_artifact({"connector": connector})

    assert connector != "None", "The board has no connector"


@pytest.mark.case_name("Accessories")
def test_accessories():
    """Let the operator pick several options."""
    dialog_box = DialogBox(
        title_bar="Accessories",
        dialog_text="Check every accessory present in the box.",
        widget=CheckboxWidget(fields=[*REQUIRED_ACCESSORIES, "Quick start guide"]),
    )
    checked = run_dialog_box(dialog_box)
    missing = sorted(set(REQUIRED_ACCESSORIES) - set(checked))
    set_case_artifact({"accessories": checked})

    assert not missing, f"Missing accessories: {', '.join(missing)}"


@pytest.mark.case_name("Bench preparation")
def test_bench_preparation():
    """Walk the operator through several steps in a single dialog."""
    dialog_box = DialogBox(
        title_bar="Bench preparation",
        dialog_text="Follow the steps before the next module.",
        widget=MultistepWidget(
            steps=[
                StepWidget(
                    title="Connect the power supply",
                    text="Set the supply to 3.3 V and connect it to J1.",
                ),
                StepWidget(
                    title="Check the reference picture",
                    text=None,
                    image=ImageComponent(address="assets/test.png", width=50),
                ),
                StepWidget(
                    title="Read the procedure",
                    text="The full procedure is available in the test plan.",
                    html=HTMLComponent(
                        html="<p>Document <b>TP-4471</b>, revision 3.</p>",
                        width=100,
                    ),
                ),
            ],
        ),
    )

    assert run_dialog_box(dialog_box), "The operator did not finish the steps"
