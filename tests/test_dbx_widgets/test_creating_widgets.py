import pytest

import hardpy
from hardpy.pytest_hardpy.utils.dialog_box import BaseWidget
from hardpy.pytest_hardpy.utils.exception import WidgetInfoError


def test_base_widget():
    widget = BaseWidget()
    assert widget.convert_data() is True


def test_text_input_widget():
    widget = hardpy.TextInputWidget()
    assert widget.convert_data("Text") == "Text"


def test_num_input_widget():
    widget = hardpy.NumericInputWidget()
    assert widget.convert_data(0) == 0


def test_radiobutton_widget():
    widget = hardpy.RadiobuttonWidget(fields=["Text", " ", 123, "123", "..", "\\"])
    assert widget.convert_data("Text") == "Text"


def test_checkbox_widget():
    widget = hardpy.CheckboxWidget(fields=["Text", "123"])
    assert set(widget.convert_data('{"Text", "123"}')) == {
        "Text",
        "123",
    }


def test_image_widget_png():
    widget = hardpy.ImageWidget(address="tests/test_dbx_widgets/assets/test.png")
    assert widget.convert_data() is True


def test_image_widget_gif():
    widget = hardpy.ImageWidget(address="tests/test_dbx_widgets/assets/test.gif")
    assert widget.convert_data() is True


def test_image_widget_jpeg():
    widget = hardpy.ImageWidget(address="tests/test_dbx_widgets/assets/test.jpeg")
    assert widget.convert_data() is True


def test_image_widget_pjpg():
    widget = hardpy.ImageWidget(address="tests/test_dbx_widgets/assets/test.pjpg")
    assert widget.convert_data() is True


def test_image_widget_svg():
    widget = hardpy.ImageWidget(address="tests/test_dbx_widgets/assets/test.svg")
    assert widget.convert_data() is True


def test_image_widget_tif():
    widget = hardpy.ImageWidget(address="tests/test_dbx_widgets/assets/test.tif")
    assert widget.convert_data() is True


def test_image_widget_wbmp():
    widget = hardpy.ImageWidget(address="tests/test_dbx_widgets/assets/test.wbmp")
    assert widget.convert_data() is True


def test_image_widget_webp():
    widget = hardpy.ImageWidget(address="tests/test_dbx_widgets/assets/test.webp")
    assert widget.convert_data() is True


def test_image_widget_icon():
    widget = hardpy.ImageWidget(address="tests/test_dbx_widgets/assets/test.icon")
    assert widget.convert_data() is True


def test_image_widget_with_empty_data():
    with pytest.raises(WidgetInfoError) as excinfo:
        hardpy.ImageWidget()
    assert str(excinfo.value) == "HardPy error: Width must be positive"


def test_image_widget_with_incorrect_width():
    with pytest.raises(WidgetInfoError) as excinfo:
        hardpy.ImageWidget(address="tests/assets/test.png", width=-1)
    assert str(excinfo.value) == "HardPy error: Width must be positive"


def test_multistep_widget():
    img_widget = hardpy.ImageWidget(address="tests/assets/test.png", width=50)
    steps = [
        hardpy.StepWidget("Step 1", text="Content for step", widget=None),
        hardpy.StepWidget("Step 2", text="Content for step 2", widget=img_widget),
        hardpy.StepWidget("Step 3", text=None, widget=img_widget),
    ]
    widget = hardpy.MultistepWidget(steps)
    assert widget.convert_data("") is True


def test_step_widget():
    widget = hardpy.StepWidget(title="Text", text=" ", widget=None)
    assert widget.convert_data("") is True
