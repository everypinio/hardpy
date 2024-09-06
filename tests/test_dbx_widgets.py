import pytest

import hardpy
from hardpy.pytest_hardpy.utils.dialog_box import BaseWidget
from hardpy.pytest_hardpy.utils.exception import WidgetInfoError


def test_base_widget_convert_data():
    widget = BaseWidget()
    assert widget.convert_data() is True


def test_text_input_widget_convert_data():
    widget = hardpy.TextInputWidget()
    assert widget.convert_data("Text") == "Text"
    assert widget.convert_data(" ") == " "
    assert widget.convert_data(123) == 123
    assert widget.convert_data("123") == "123"


def test_num_input_widget_convert_data():
    widget = hardpy.NumericInputWidget()
    assert widget.convert_data(0) == 0
    assert widget.convert_data(123.777) == 123.777
    assert widget.convert_data(123) == 123
    assert widget.convert_data("123") == 123


def test_radiobutton_widget_convert_data():
    widget = hardpy.RadiobuttonWidget(fields=["Text", " ", 123, "123", "..", "\\"])
    assert widget.convert_data("Text") == "Text"
    assert widget.convert_data(" ") == " "
    assert widget.convert_data(123) == 123
    assert widget.convert_data("123") == "123"
    assert widget.convert_data("..") == ".."
    assert widget.convert_data("\\") == "\\"


def test_checkbox_widget_convert_data():
    widget = hardpy.CheckboxWidget(fields=["Text", "123"])
    assert set(widget.convert_data('{"Text", "123"}')) == {
        "Text",
        "123",
    }


def test_image_widget_convert_data():
    widget = hardpy.ImageWidget(address="tests/assets/test.png")
    assert widget.convert_data() is True


def test_image_widget_convert_data_with_incorrect_width():
    with pytest.raises(WidgetInfoError) as excinfo:
        widget = hardpy.ImageWidget(address="tests/assets/test.png", width=-50)
        widget.convert_data()
    assert str(excinfo.value) == "HardPy error: Width must be positive"


def test_multistep_widget_convert_data():
    img_widget = hardpy.ImageWidget(address="tests/assets/test.png", width=50)
    steps = [
        hardpy.StepWidget("Step 1", text="Content for step", widget=None),
        hardpy.StepWidget("Step 2", text="Content for step 2", widget=img_widget),
        hardpy.StepWidget("Step 3", text=None, widget=img_widget),
    ]
    widget = hardpy.MultistepWidget(steps)
    assert widget.convert_data("") is True


def test_multistep_widget_convert_data_2():
    with pytest.raises(WidgetInfoError) as excinfo:
        img_widget = hardpy.ImageWidget(address="tests/assets/test.png", width=-50)
        steps = [
            hardpy.StepWidget("Step 1", text="Content for step", widget=None),
            hardpy.StepWidget("Step 2", text="Content for step 2", widget=img_widget),
            hardpy.StepWidget("Step 3", text=None, widget=img_widget),
        ]
        widget = hardpy.MultistepWidget(steps)
        widget.convert_data("")

    assert str(excinfo.value) == "HardPy error: Width must be positive"


def test_step_widget_convert_data():
    widget = hardpy.StepWidget(title="Text", text=" ", widget=None)
    assert widget.convert_data("") is True
