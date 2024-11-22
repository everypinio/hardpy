import pytest

from hardpy import (
    BaseWidget,
    DialogBox,
    ImageComponent,
    MultistepWidget,
    StepWidget,
    run_dialog_box,
)

pytestmark = pytest.mark.module_name("Multiple steps dialog box")


def test_small_100_long_text():
    base_widget = BaseWidget(image=ImageComponent(address="assets/test.png", width=100))
    steps = [
        StepWidget(
            "Step 1",
            text="Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. ",  # noqa: E501
            widget=None,
        ),
        StepWidget(
            "Step 2",
            text="Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. ",  # noqa: E501
            widget=base_widget,
        ),
        StepWidget("Step 3", text=None, widget=base_widget),
    ]
    dbx = DialogBox(
        dialog_text="Follow the steps and click Confirm",
        widget=MultistepWidget(steps),
    )
    response = run_dialog_box(dbx)
    assert response


def test_small_100():
    base_widget = BaseWidget(image=ImageComponent(address="assets/test.png", width=100))
    steps = [
        StepWidget(
            "Step 1",
            text="Content for step.",
            widget=None,
        ),
        StepWidget(
            "Step 2",
            text="Content for step.",
            widget=base_widget,
        ),
        StepWidget("Step 3", text=None, widget=base_widget),
    ]
    dbx = DialogBox(
        dialog_text="Follow the steps and click Confirm",
        widget=MultistepWidget(steps),
    )
    response = run_dialog_box(dbx)
    assert response


def test_big_100_long_text():
    base_widget = BaseWidget(
        image=ImageComponent(address="assets/sample_1920x1280.gif", width=100),
    )
    steps = [
        StepWidget(
            "Step 1",
            text="Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. ",  # noqa: E501
            widget=None,
        ),
        StepWidget(
            "Step 2",
            text="Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. ",  # noqa: E501
            widget=base_widget,
        ),
        StepWidget("Step 3", text=None, widget=base_widget),
    ]
    dbx = DialogBox(
        dialog_text="Follow the steps and click Confirm",
        widget=MultistepWidget(steps),
    )
    response = run_dialog_box(dbx)
    assert response


def test_big_100():
    base_widget = BaseWidget(
        image=ImageComponent(address="assets/sample_1920x1280.gif", width=100),
    )
    steps = [
        StepWidget(
            "Step 1",
            text="Content for step. ",
            widget=None,
        ),
        StepWidget(
            "Step 2",
            text="Content for step. ",
            widget=base_widget,
        ),
        StepWidget("Step 3", text=None, widget=base_widget),
    ]
    dbx = DialogBox(
        dialog_text="Follow the steps and click Confirm",
        widget=MultistepWidget(steps),
    )
    response = run_dialog_box(dbx)
    assert response


def test_small_20_long_text():
    base_widget = BaseWidget(image=ImageComponent(address="assets/test.png", width=20))
    steps = [
        StepWidget(
            "Step 1",
            text="Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. ",  # noqa: E501
            widget=None,
        ),
        StepWidget(
            "Step 2",
            text="Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. ",  # noqa: E501
            widget=base_widget,
        ),
        StepWidget("Step 3", text=None, widget=base_widget),
    ]
    dbx = DialogBox(
        dialog_text="Follow the steps and click Confirm",
        widget=MultistepWidget(steps),
    )
    response = run_dialog_box(dbx)
    assert response


def test_small_20():
    base_widget = BaseWidget(image=ImageComponent(address="assets/test.png", width=20))
    steps = [
        StepWidget(
            "Step 1",
            text="Content for step.",
            widget=None,
        ),
        StepWidget(
            "Step 2",
            text="Content for step.",
            widget=base_widget,
        ),
        StepWidget("Step 3", text=None, widget=base_widget),
    ]
    dbx = DialogBox(
        dialog_text="Follow the steps and click Confirm",
        widget=MultistepWidget(steps),
    )
    response = run_dialog_box(dbx)
    assert response


def test_big_20_long_text():
    base_widget = BaseWidget(
        image=ImageComponent(address="assets/sample_1920x1280.gif", width=20),
    )
    steps = [
        StepWidget(
            "Step 1",
            text="Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. ",  # noqa: E501
            widget=None,
        ),
        StepWidget(
            "Step 2",
            text="Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. ",  # noqa: E501
            widget=base_widget,
        ),
        StepWidget("Step 3", text=None, widget=base_widget),
    ]
    dbx = DialogBox(
        dialog_text="Follow the steps and click Confirm",
        widget=MultistepWidget(steps),
    )
    response = run_dialog_box(dbx)
    assert response


def test_big_20_mixed():
    base_widget = BaseWidget(
        image=ImageComponent(address="assets/sample_1920x1280.gif", width=20),
    )
    steps = [
        StepWidget(
            "Step 1",
            text="Content for step. ",
            widget=None,
        ),
        StepWidget(
            "Step 2",
            text="Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. ",  # noqa: E501
            widget=base_widget,
        ),
        StepWidget("Step 3", text=None, widget=base_widget),
    ]
    dbx = DialogBox(
        dialog_text="Follow the steps and click Confirm",
        widget=MultistepWidget(steps),
    )
    response = run_dialog_box(dbx)
    assert response


def test_small_200_long_text():
    base_widget = BaseWidget(image=ImageComponent(address="assets/test.png", width=200))
    steps = [
        StepWidget(
            "Step 1",
            text="Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. ",  # noqa: E501
            widget=None,
        ),
        StepWidget(
            "Step 2",
            text="Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. ",  # noqa: E501
            widget=base_widget,
        ),
        StepWidget("Step 3", text=None, widget=base_widget),
    ]
    dbx = DialogBox(
        dialog_text="Follow the steps and click Confirm",
        widget=MultistepWidget(steps),
    )
    response = run_dialog_box(dbx)
    assert response


def test_small_200():
    base_widget = BaseWidget(image=ImageComponent(address="assets/test.png", width=200))
    steps = [
        StepWidget(
            "Step 1",
            text="Content for step.",
            widget=None,
        ),
        StepWidget(
            "Step 2",
            text="Content for step.",
            widget=base_widget,
        ),
        StepWidget("Step 3", text=None, widget=base_widget),
    ]
    dbx = DialogBox(
        dialog_text="Follow the steps and click Confirm",
        widget=MultistepWidget(steps),
    )
    response = run_dialog_box(dbx)
    assert response


def test_big_200_long_text():
    base_widget = BaseWidget(
        image=ImageComponent(address="assets/sample_1920x1280.gif", width=200),
    )
    steps = [
        StepWidget(
            "Step 1",
            text="Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. ",  # noqa: E501
            widget=None,
        ),
        StepWidget(
            "Step 2",
            text="Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. ",  # noqa: E501
            widget=base_widget,
        ),
        StepWidget("Step 3", text=None, widget=base_widget),
    ]
    dbx = DialogBox(
        dialog_text="Follow the steps and click Confirm",
        widget=MultistepWidget(steps),
    )
    response = run_dialog_box(dbx)
    assert response


def test_big_200_mixed():
    base_widget = BaseWidget(
        image=ImageComponent(address="assets/sample_1920x1280.gif", width=200),
    )
    steps = [
        StepWidget(
            "Step 1",
            text="Content for step. ",
            widget=None,
        ),
        StepWidget(
            "Step 2",
            text="Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. ",  # noqa: E501
            widget=base_widget,
        ),
        StepWidget("Step 3", text=None, widget=base_widget),
    ]
    dbx = DialogBox(
        dialog_text="Follow the steps and click Confirm",
        widget=MultistepWidget(steps),
    )
    response = run_dialog_box(dbx)
    assert response


def test_5mb_200_long_text():
    base_widget = BaseWidget(
        image=ImageComponent(address="assets/test_5_mb.jpg", width=200),
    )
    steps = [
        StepWidget(
            "Step 1",
            text="Content for step. ",
            widget=None,
        ),
        StepWidget(
            "Step 2",
            text="Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. ",  # noqa: E501
            widget=base_widget,
        ),
        StepWidget("Step 3", text=None, widget=base_widget),
    ]
    dbx = DialogBox(
        dialog_text="Follow the steps and click Confirm",
        widget=MultistepWidget(steps),
    )
    response = run_dialog_box(dbx)
    assert response


def test_multiple_steps_different_images():
    base_widget = BaseWidget(image=ImageComponent(address="assets/test.png", width=100))
    base_widget_2 = BaseWidget(
        image=ImageComponent(address="assets/sample_1920x1280.gif", width=100),
    )
    steps = [
        StepWidget("Step 1", text="AAA", widget=None),
        StepWidget("Step 2", text="AAA", widget=base_widget),
        StepWidget("Step 3", text=None, widget=base_widget_2),
    ]
    dbx = DialogBox(dialog_text="BBB", widget=MultistepWidget(steps))
    response = run_dialog_box(dbx)
    assert response


def test_multiple_steps_different_images_in_other_order():
    base_widget = BaseWidget(image=ImageComponent(address="assets/test.png", width=100))
    base_widget_2 = BaseWidget(
        image=ImageComponent(address="assets/sample_1920x1280.gif", width=100),
    )
    steps = [
        StepWidget("Step 1", text="AAA", widget=None),
        StepWidget("Step 2", text="AAA", widget=base_widget_2),
        StepWidget("Step 3", text=None, widget=base_widget),
    ]
    dbx = DialogBox(dialog_text="BBB", widget=MultistepWidget(steps))
    response = run_dialog_box(dbx)
    assert response


def test_multiple_steps_different_images_different_percent():
    base_widget = BaseWidget(image=ImageComponent(address="assets/test.png", width=50))
    base_widget_2 = BaseWidget(
        image=ImageComponent(address="assets/sample_1920x1280.gif", width=100),
    )
    steps = [
        StepWidget("Step 1", text="AAA", widget=None),
        StepWidget("Step 2", text="AAA", widget=base_widget),
        StepWidget("Step 3", text=None, widget=base_widget_2),
    ]
    dbx = DialogBox(
        dialog_text="BBB                                                                                                                              ",  # noqa: E501
        widget=MultistepWidget(steps),
    )
    response = run_dialog_box(dbx)
    assert response


def test_multiple_steps_different_percent():
    base_widget = BaseWidget(image=ImageComponent(address="assets/test.png", width=20))
    base_widget_2 = BaseWidget(
        image=ImageComponent(address="assets/test.png", width=50),
    )
    base_widget_3 = BaseWidget(
        image=ImageComponent(address="assets/test.png", width=100),
    )
    base_widget_4 = BaseWidget(
        image=ImageComponent(address="assets/test.png", width=150),
    )
    base_widget_5 = BaseWidget(
        image=ImageComponent(address="assets/test.png", width=200),
    )
    steps = [
        StepWidget("Step 1", text="AAA", widget=base_widget),
        StepWidget("Step 2", text="AAA", widget=base_widget_2),
        StepWidget("Step 3", text="AAA", widget=base_widget_3),
        StepWidget("Step 4", text="AAA", widget=base_widget_4),
        StepWidget("Step 5", text="AAA", widget=base_widget_5),
    ]
    dbx = DialogBox(dialog_text="BBB", widget=MultistepWidget(steps))
    response = run_dialog_box(dbx)
    assert response


def test_multiple_steps_different_percent_recursion():
    base_widget = BaseWidget(image=ImageComponent(address="assets/test.png", width=20))
    base_widget_2 = BaseWidget(
        image=ImageComponent(address="assets/test.png", width=50),
    )
    base_widget_3 = BaseWidget(
        image=ImageComponent(address="assets/test.png", width=100),
    )
    base_widget_4 = BaseWidget(
        image=ImageComponent(address="assets/test.png", width=150),
    )
    base_widget_5 = BaseWidget(
        image=ImageComponent(address="assets/test.png", width=200),
    )
    steps = [
        StepWidget("Step 1", text="AAA", widget=base_widget_5),
        StepWidget("Step 2", text="AAA", widget=base_widget_4),
        StepWidget("Step 3", text="AAA", widget=base_widget_3),
        StepWidget("Step 4", text="AAA", widget=base_widget_2),
        StepWidget("Step 5", text="AAA", widget=base_widget),
    ]
    dbx = DialogBox(dialog_text="BBB", widget=MultistepWidget(steps))
    response = run_dialog_box(dbx)
    assert response


def test_small_100_long_text_with_line_break():
    base_widget = BaseWidget(image=ImageComponent(address="assets/test.png", width=100))
    steps = [
        StepWidget(
            "Step 1",
            text="""Some text.
            - Point 1
            - Point 2""",
            widget=None,
        ),
        StepWidget(
            "Step 2",
            text="Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. ",  # noqa: E501
            widget=base_widget,
        ),
        StepWidget("Step 3", text=None, widget=base_widget),
    ]
    dbx = DialogBox(
        dialog_text="Follow the steps and click Confirm",
        widget=MultistepWidget(steps),
    )
    response = run_dialog_box(dbx)
    assert response


def test_horizontal_and_vertical_stripes():
    base_widget_1 = BaseWidget(
        image=ImageComponent(address="assets/horizontal_stripe.png", width=100),
    )
    base_widget_2 = BaseWidget(
        image=ImageComponent(address="assets/vertical_stripe.png", width=100),
    )
    steps = [
        StepWidget(
            "Step 1",
            text="""Some text.
            - Point 1
            - Point 2""",
            widget=None,
        ),
        StepWidget(
            "Step 2",
            text="Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. ",  # noqa: E501
            widget=base_widget_1,
        ),
        StepWidget("Step 3", text=None, widget=base_widget_2),
    ]
    dbx = DialogBox(
        dialog_text="Follow the steps and click Confirm",
        widget=MultistepWidget(steps),
    )
    response = run_dialog_box(dbx)
    assert response


def test_vertical_and_horizontal_stripes():
    base_widget_1 = BaseWidget(
        image=ImageComponent(address="assets/vertical_stripe.png", width=100),
    )
    base_widget_2 = BaseWidget(
        image=ImageComponent(address="assets/horizontal_stripe.png", width=100),
    )
    steps = [
        StepWidget(
            "Step 1",
            text="""Some text.
            - Point 1
            - Point 2""",
            widget=None,
        ),
        StepWidget(
            "Step 2",
            text="Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. ",  # noqa: E501
            widget=base_widget_2,
        ),
        StepWidget("Step 3", text=None, widget=base_widget_1),
    ]
    dbx = DialogBox(
        dialog_text="Follow the steps and click Confirm",
        widget=MultistepWidget(steps),
    )
    response = run_dialog_box(dbx)
    assert response


def test_vertical_and_horizontal_stripes_with_small():
    base_widget_1 = BaseWidget(
        image=ImageComponent(address="assets/horizontal_stripe.png", width=100),
    )
    base_widget_2 = BaseWidget(
        image=ImageComponent(address="assets/vertical_stripe.png", width=100),
    )
    base_widget = BaseWidget(image=ImageComponent(address="assets/test.png", width=100))
    steps = [
        StepWidget(
            "Step 1",
            text="""Some text.
            - Point 1
            - Point 2""",
            widget=None,
        ),
        StepWidget(
            "Step 2",
            text="Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. ",  # noqa: E501
            widget=base_widget_2,
        ),
        StepWidget("Step 3", text=None, widget=base_widget_1),
        StepWidget("Step 4", text=None, widget=base_widget),
    ]
    dbx = DialogBox(
        dialog_text="Follow the steps and click Confirm",
        widget=MultistepWidget(steps),
    )
    response = run_dialog_box(dbx)
    assert response


def test_vertical_and_horizontal_stripes_with_small_before_big():
    base_widget_1 = BaseWidget(
        image=ImageComponent(address="assets/horizontal_stripe.png", width=100),
    )
    base_widget_2 = BaseWidget(
        image=ImageComponent(address="assets/vertical_stripe.png", width=100),
    )
    base_widget = BaseWidget(image=ImageComponent(address="assets/test.png", width=100))
    steps = [
        StepWidget("Step 1", text=None, widget=base_widget),
        StepWidget(
            "Step 2",
            text="""Some text.
            - Point 1
            - Point 2""",
            widget=None,
        ),
        StepWidget(
            "Step 3",
            text="Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. ",  # noqa: E501
            widget=base_widget_2,
        ),
        StepWidget("Step 4", text=None, widget=base_widget_1),
    ]
    dbx = DialogBox(
        dialog_text="Follow the steps and click Confirm",
        widget=MultistepWidget(steps),
    )
    response = run_dialog_box(dbx)
    assert response
