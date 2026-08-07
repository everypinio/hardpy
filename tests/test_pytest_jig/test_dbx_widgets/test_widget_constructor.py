import jig
from jig.pytest_jig.utils.dialog_box import BaseWidget
from jig.pytest_jig.utils.exception import WidgetInfoError

assets_path = "tests/test_pytest_jig/test_dbx_widgets/assets/"


def test_base_widget():
    BaseWidget()
    assert True


def test_text_input_widget():
    jig.TextInputWidget()
    assert True


def test_num_input_widget():
    jig.NumericInputWidget()
    assert True


def test_radiobutton_widget():
    jig.RadiobuttonWidget(fields=["Text", " ", 123, "123", "..", "\\"])  # type: ignore
    assert True


def test_radiobutton_empty_widget():
    try:
        jig.RadiobuttonWidget(fields=[])
        msg = "WidgetInfoError was not raised"
        raise AssertionError(msg)
    except ValueError:
        assert True


def test_checkbox_widget():
    jig.CheckboxWidget(fields=["Text", "123"])
    assert True


def test_checkbox_empty_widget():
    try:
        jig.CheckboxWidget(fields=[])
        msg = "WidgetInfoError was not raised"
        raise AssertionError(msg)
    except ValueError:
        assert True


def test_image_widget_png():
    jig.ImageComponent(address=f"{assets_path}test.png")
    assert True


def test_image_widget_gif():
    jig.ImageComponent(address=f"{assets_path}test.gif")
    assert True


def test_image_widget_jpeg():
    jig.ImageComponent(address=f"{assets_path}test.jpeg")
    assert True


def test_image_widget_pjpg():
    jig.ImageComponent(address=f"{assets_path}test.pjpg")
    assert True


def test_image_widget_svg():
    jig.ImageComponent(address=f"{assets_path}test.svg")
    assert True


def test_image_widget_tif():
    jig.ImageComponent(address=f"{assets_path}test.tif")
    assert True


def test_image_widget_wbmp():
    jig.ImageComponent(address=f"{assets_path}test.wbmp")
    assert True


def test_image_widget_webp():
    jig.ImageComponent(address=f"{assets_path}test.webp")
    assert True


def test_image_widget_icon():
    jig.ImageComponent(address=f"{assets_path}test.icon")
    assert True


def test_image_widget_with_empty_data():
    try:
        jig.ImageComponent()  # type: ignore
        msg = "TypeError was not raised"
        raise AssertionError(msg)
    except TypeError:
        assert True


def test_image_widget_with_incorrect_width():
    try:
        jig.ImageComponent(address="123.png", width=-1)
        msg = "WidgetInfoError was not raised"
        raise AssertionError(msg)
    except WidgetInfoError:
        assert True


def test_multistep_widget():
    img_widget = jig.ImageComponent(
        address=f"{assets_path}/test.png",
        width=50,
    )
    steps = [
        jig.StepWidget("Step 1", text="Content for step"),
        jig.StepWidget("Step 2", text="Content for step 2", image=img_widget),
        jig.StepWidget("Step 3", text=None, image=img_widget),
    ]
    jig.MultistepWidget(steps)
    assert True


def test_step_widget():
    jig.StepWidget(title="Text", text=" ")
    assert True


def test_empty_step_widget():
    try:
        jig.StepWidget()  # type: ignore
        msg = "WidgetInfoError was not raised"
        raise AssertionError(msg)
    except TypeError:
        assert True
