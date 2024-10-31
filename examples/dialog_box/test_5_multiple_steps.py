import pytest

from hardpy import DialogBox, ImageWidget, MultistepWidget, StepWidget, run_dialog_box

pytestmark = pytest.mark.module_name("Multiple steps dialog box")


def test_multiple_steps_small_100_long_text():
    img_widget = ImageWidget(address="assets/test.png", width=100)
    steps = [
        StepWidget(
            "Step 1",
            text="Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. ",  # noqa: E501
            widget=None,
        ),
        StepWidget(
            "Step 2",
            text="Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. ",  # noqa: E501
            widget=img_widget,
        ),
        StepWidget("Step 3", text=None, widget=img_widget),
    ]
    dbx = DialogBox(
        dialog_text="Follow the steps and click Confirm",
        widget=MultistepWidget(steps),
    )
    response = run_dialog_box(dbx)
    assert response


def test_multiple_steps_small_100():
    img_widget = ImageWidget(address="assets/test.png", width=100)
    steps = [
        StepWidget(
            "Step 1",
            text="Content for step.",
            widget=None,
        ),
        StepWidget(
            "Step 2",
            text="Content for step.",
            widget=img_widget,
        ),
        StepWidget("Step 3", text=None, widget=img_widget),
    ]
    dbx = DialogBox(
        dialog_text="Follow the steps and click Confirm",
        widget=MultistepWidget(steps),
    )
    response = run_dialog_box(dbx)
    assert response


def test_multiple_steps_big_100_long_text():
    img_widget = ImageWidget(address="assets/sample_1920x1280.gif", width=100)
    steps = [
        StepWidget(
            "Step 1",
            text="Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. ",  # noqa: E501
            widget=None,
        ),
        StepWidget(
            "Step 2",
            text="Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. ",  # noqa: E501
            widget=img_widget,
        ),
        StepWidget("Step 3", text=None, widget=img_widget),
    ]
    dbx = DialogBox(
        dialog_text="Follow the steps and click Confirm",
        widget=MultistepWidget(steps),
    )
    response = run_dialog_box(dbx)
    assert response


def test_multiple_steps_big_100():
    img_widget = ImageWidget(address="assets/sample_1920x1280.gif", width=100)
    steps = [
        StepWidget(
            "Step 1",
            text="Content for step. ",
            widget=None,
        ),
        StepWidget(
            "Step 2",
            text="Content for step. ",
            widget=img_widget,
        ),
        StepWidget("Step 3", text=None, widget=img_widget),
    ]
    dbx = DialogBox(
        dialog_text="Follow the steps and click Confirm",
        widget=MultistepWidget(steps),
    )
    response = run_dialog_box(dbx)
    assert response


def test_multiple_steps_small_20_long_text():
    img_widget = ImageWidget(address="assets/test.png", width=20)
    steps = [
        StepWidget(
            "Step 1",
            text="Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. ",  # noqa: E501
            widget=None,
        ),
        StepWidget(
            "Step 2",
            text="Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. ",  # noqa: E501
            widget=img_widget,
        ),
        StepWidget("Step 3", text=None, widget=img_widget),
    ]
    dbx = DialogBox(
        dialog_text="Follow the steps and click Confirm",
        widget=MultistepWidget(steps),
    )
    response = run_dialog_box(dbx)
    assert response


def test_multiple_steps_small_20():
    img_widget = ImageWidget(address="assets/test.png", width=20)
    steps = [
        StepWidget(
            "Step 1",
            text="Content for step.",
            widget=None,
        ),
        StepWidget(
            "Step 2",
            text="Content for step.",
            widget=img_widget,
        ),
        StepWidget("Step 3", text=None, widget=img_widget),
    ]
    dbx = DialogBox(
        dialog_text="Follow the steps and click Confirm",
        widget=MultistepWidget(steps),
    )
    response = run_dialog_box(dbx)
    assert response


def test_multiple_steps_big_20_long_text():
    img_widget = ImageWidget(address="assets/sample_1920x1280.gif", width=20)
    steps = [
        StepWidget(
            "Step 1",
            text="Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. ",  # noqa: E501
            widget=None,
        ),
        StepWidget(
            "Step 2",
            text="Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. ",  # noqa: E501
            widget=img_widget,
        ),
        StepWidget("Step 3", text=None, widget=img_widget),
    ]
    dbx = DialogBox(
        dialog_text="Follow the steps and click Confirm",
        widget=MultistepWidget(steps),
    )
    response = run_dialog_box(dbx)
    assert response


def test_multiple_steps_big_20_mixed():
    img_widget = ImageWidget(address="assets/sample_1920x1280.gif", width=20)
    steps = [
        StepWidget(
            "Step 1",
            text="Content for step. ",
            widget=None,
        ),
        StepWidget(
            "Step 2",
            text="Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. ",  # noqa: E501
            widget=img_widget,
        ),
        StepWidget("Step 3", text=None, widget=img_widget),
    ]
    dbx = DialogBox(
        dialog_text="Follow the steps and click Confirm",
        widget=MultistepWidget(steps),
    )
    response = run_dialog_box(dbx)
    assert response


def test_multiple_steps_small_200_long_text():
    img_widget = ImageWidget(address="assets/test.png", width=200)
    steps = [
        StepWidget(
            "Step 1",
            text="Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. ",  # noqa: E501
            widget=None,
        ),
        StepWidget(
            "Step 2",
            text="Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. ",  # noqa: E501
            widget=img_widget,
        ),
        StepWidget("Step 3", text=None, widget=img_widget),
    ]
    dbx = DialogBox(
        dialog_text="Follow the steps and click Confirm",
        widget=MultistepWidget(steps),
    )
    response = run_dialog_box(dbx)
    assert response


def test_multiple_steps_small_200():
    img_widget = ImageWidget(address="assets/test.png", width=200)
    steps = [
        StepWidget(
            "Step 1",
            text="Content for step.",
            widget=None,
        ),
        StepWidget(
            "Step 2",
            text="Content for step.",
            widget=img_widget,
        ),
        StepWidget("Step 3", text=None, widget=img_widget),
    ]
    dbx = DialogBox(
        dialog_text="Follow the steps and click Confirm",
        widget=MultistepWidget(steps),
    )
    response = run_dialog_box(dbx)
    assert response


def test_multiple_steps_big_200_long_text():
    img_widget = ImageWidget(address="assets/sample_1920x1280.gif", width=200)
    steps = [
        StepWidget(
            "Step 1",
            text="Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. ",  # noqa: E501
            widget=None,
        ),
        StepWidget(
            "Step 2",
            text="Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. ",  # noqa: E501
            widget=img_widget,
        ),
        StepWidget("Step 3", text=None, widget=img_widget),
    ]
    dbx = DialogBox(
        dialog_text="Follow the steps and click Confirm",
        widget=MultistepWidget(steps),
    )
    response = run_dialog_box(dbx)
    assert response


def test_multiple_steps_big_200_mixed():
    img_widget = ImageWidget(address="assets/sample_1920x1280.gif", width=200)
    steps = [
        StepWidget(
            "Step 1",
            text="Content for step. ",
            widget=None,
        ),
        StepWidget(
            "Step 2",
            text="Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. ",  # noqa: E501
            widget=img_widget,
        ),
        StepWidget("Step 3", text=None, widget=img_widget),
    ]
    dbx = DialogBox(
        dialog_text="Follow the steps and click Confirm",
        widget=MultistepWidget(steps),
    )
    response = run_dialog_box(dbx)
    assert response


def test_multiple_steps_long_200_long_text():
    img_widget = ImageWidget(address="assets/long_image.png", width=200)
    steps = [
        StepWidget(
            "Step 1",
            text="Content for step. ",
            widget=None,
        ),
        StepWidget(
            "Step 2",
            text="Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. ",  # noqa: E501
            widget=img_widget,
        ),
        StepWidget("Step 3", text=None, widget=img_widget),
    ]
    dbx = DialogBox(
        dialog_text="Follow the steps and click Confirm",
        widget=MultistepWidget(steps),
    )
    response = run_dialog_box(dbx)
    assert response
