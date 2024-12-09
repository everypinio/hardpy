import hardpy
from hardpy.pytest_hardpy.utils.dialog_box import BaseWidget
from hardpy.pytest_hardpy.utils.exception import WidgetInfoError

assets_path = "tests/test_pytest_hardpy/test_dbx_widgets/assets/"


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
    hardpy.RadiobuttonWidget(fields=["Text", " ", 123, "123", "..", "\\"])  # type: ignore
    assert True


def test_radiobutton_empty_widget():
    try:
        hardpy.RadiobuttonWidget(fields=[])
        msg = "WidgetInfoError was not raised"
        raise AssertionError(msg)
    except ValueError:
        assert True


def test_checkbox_widget():
    hardpy.CheckboxWidget(fields=["Text", "123"])
    assert True


def test_checkbox_empty_widget():
    try:
        hardpy.CheckboxWidget(fields=[])
        msg = "WidgetInfoError was not raised"
        raise AssertionError(msg)
    except ValueError:
        assert True


def test_image_widget_png():
    hardpy.ImageComponent(address=f"{assets_path}test.png")
    assert True


def test_image_widget_gif():
    hardpy.ImageComponent(address=f"{assets_path}test.gif")
    assert True


def test_image_widget_jpeg():
    hardpy.ImageComponent(address=f"{assets_path}test.jpeg")
    assert True


def test_image_widget_pjpg():
    hardpy.ImageComponent(address=f"{assets_path}test.pjpg")
    assert True


def test_image_widget_svg():
    hardpy.ImageComponent(address=f"{assets_path}test.svg")
    assert True


def test_image_widget_tif():
    hardpy.ImageComponent(address=f"{assets_path}test.tif")
    assert True


def test_image_widget_wbmp():
    hardpy.ImageComponent(address=f"{assets_path}test.wbmp")
    assert True


def test_image_widget_webp():
    hardpy.ImageComponent(address=f"{assets_path}test.webp")
    assert True


def test_image_widget_icon():
    hardpy.ImageComponent(address=f"{assets_path}test.icon")
    assert True


def test_image_widget_with_empty_data():
    try:
        hardpy.ImageComponent()  # type: ignore
        msg = "TypeError was not raised"
        raise AssertionError(msg)
    except TypeError:
        assert True


def test_image_widget_with_incorrect_width():
    try:
        hardpy.ImageComponent(address="123.png", width=-1)
        msg = "WidgetInfoError was not raised"
        raise AssertionError(msg)
    except WidgetInfoError:
        assert True


def test_multistep_widget():
    img_widget = hardpy.ImageComponent(
        address=f"{assets_path}/test.png",
        width=50,
    )
    steps = [
        hardpy.StepWidget("Step 1", text="Content for step"),
        hardpy.StepWidget("Step 2", text="Content for step 2", image=img_widget),
        hardpy.StepWidget("Step 3", text=None, image=img_widget),
    ]
    hardpy.MultistepWidget(steps)
    assert True


def test_step_widget():
    hardpy.StepWidget(title="Text", text=" ")
    assert True


def test_empty_step_widget():
    try:
        hardpy.StepWidget()  # type: ignore
        msg = "WidgetInfoError was not raised"
        raise AssertionError(msg)
    except TypeError:
        assert True
