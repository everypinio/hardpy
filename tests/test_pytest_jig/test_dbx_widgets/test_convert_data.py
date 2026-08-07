from math import inf

import jig
from jig.pytest_jig.utils.dialog_box import BaseWidget


def test_base_widget():
    widget = BaseWidget()
    assert widget.convert_data() is True


def test_text_input_widget():
    widget = jig.TextInputWidget()
    assert widget.convert_data("Text") == "Text"
    assert widget.convert_data(" ") == " "
    assert widget.convert_data("1") == "1"


def test_num_input_widget():
    widget = jig.NumericInputWidget()
    assert widget.convert_data("0") == 0
    assert widget.convert_data("1") == 1
    assert widget.convert_data("-1") == -1
    assert widget.convert_data("0.1") == 0.1
    assert widget.convert_data("-inf") == -inf
    assert widget.convert_data("inf") == inf
    assert widget.convert_data("1e15") == 1e15


def test_radiobutton_widget():
    widget = jig.RadiobuttonWidget(fields=["Text"])
    assert widget.convert_data("Text") == "Text"
    assert widget.convert_data(" ") == " "
    assert widget.convert_data("123") == "123"
    assert widget.convert_data("..") == ".."
    assert widget.convert_data("\\") == "\\"


def test_checkbox_widget():
    widget = jig.CheckboxWidget(fields=["Text", "123"])
    assert widget.convert_data('{"Text", "123"}') == {
        "Text",
        "123",
    }


def test_multistep_widget():
    steps = [
        jig.StepWidget("Step 1", text="Content for step"),
    ]
    widget = jig.MultistepWidget(steps)
    assert widget.convert_data("") is True


def test_step_widget():
    widget = jig.StepWidget(title="Text", text=" ")
    assert widget.convert_data("") is True
