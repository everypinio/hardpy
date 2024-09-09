import pytest

import hardpy
from hardpy.pytest_hardpy.utils.dialog_box import BaseWidget
from hardpy.pytest_hardpy.utils.exception import WidgetInfoError


def test_base_widget():
    BaseWidget()
    assert True


def test_text_input_widget():
    hardpy.TextInputWidget()
    assert True


def test_num_input_widget():
    hardpy.NumericInputWidget()
    assert True


def test_radiobutton_widget():
    hardpy.RadiobuttonWidget(fields=["Text", " ", 123, "123", "..", "\\"])
    assert True


def test_radiobutton_empty_widget():
    try:
        hardpy.RadiobuttonWidget(fields=[])
        assert False, "WidgetInfoError was not raised"
    except ValueError as excinfo:
        assert str(excinfo) == "RadiobuttonWidget must have at least one field"


def test_checkbox_widget():
    hardpy.CheckboxWidget(fields=["Text", "123"])
    assert True


def test_checkbox_empty_widget():
    try:
        hardpy.CheckboxWidget(fields=[])
        assert False, "WidgetInfoError was not raised"
    except ValueError as excinfo:
        assert str(excinfo) == "Checkbox must have at least one field"


def test_image_widget_png():
    hardpy.ImageWidget(address="tests/test_dbx_widgets/assets/test.png")
    assert True


def test_image_widget_gif():
    hardpy.ImageWidget(address="tests/test_dbx_widgets/assets/test.gif")
    assert True


def test_image_widget_jpeg():
    hardpy.ImageWidget(address="tests/test_dbx_widgets/assets/test.jpeg")
    assert True


def test_image_widget_pjpg():
    hardpy.ImageWidget(address="tests/test_dbx_widgets/assets/test.pjpg")
    assert True


def test_image_widget_svg():
    hardpy.ImageWidget(address="tests/test_dbx_widgets/assets/test.svg")
    assert True


def test_image_widget_tif():
    hardpy.ImageWidget(address="tests/test_dbx_widgets/assets/test.tif")
    assert True


def test_image_widget_wbmp():
    hardpy.ImageWidget(address="tests/test_dbx_widgets/assets/test.wbmp")
    assert True


def test_image_widget_webp():
    hardpy.ImageWidget(address="tests/test_dbx_widgets/assets/test.webp")
    assert True


def test_image_widget_icon():
    hardpy.ImageWidget(address="tests/test_dbx_widgets/assets/test.icon")
    assert True


def test_image_widget_with_empty_data():
    try:
        hardpy.ImageWidget()
        assert False, "TypeError was not raised"
    except TypeError as excinfo:
        assert (
            str(excinfo)
            == "ImageWidget.__init__() missing 1 required positional argument: 'address'"
        )


def test_image_widget_with_incorrect_width():
    try:
        hardpy.ImageWidget(address="tests/assets/test.png", width=-1)
        assert False, "WidgetInfoError was not raised"
    except WidgetInfoError as excinfo:
        assert str(excinfo) == "HardPy error: Width must be positive"


def test_multistep_widget():
    img_widget = hardpy.ImageWidget(
        address="tests/test_dbx_widgets/assets/test.png", width=50
    )
    steps = [
        hardpy.StepWidget("Step 1", text="Content for step", widget=None),
        hardpy.StepWidget("Step 2", text="Content for step 2", widget=img_widget),
        hardpy.StepWidget("Step 3", text=None, widget=img_widget),
    ]
    hardpy.MultistepWidget(steps)
    assert True


def test_step_widget():
    hardpy.StepWidget(title="Text", text=" ", widget=None)
    assert True


def test_empty_step_widget():
    try:
        hardpy.StepWidget()
        assert False, "WidgetInfoError was not raised"
    except TypeError as excinfo:
        assert (
            str(excinfo)
            == "StepWidget.__init__() missing 3 required positional arguments: 'title', 'text', and 'widget'"
        )
