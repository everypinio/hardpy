import pytest
from hardpy import DialogBox, ImageWidget, MultistepWidget, StepWidget, run_dialog_box

pytestmark = pytest.mark.module_name("Multiple steps dialog box")


# def test_small_100_long_text():
#     img_widget = ImageWidget(address="assets/test.png", width=100)
#     steps = [
#         StepWidget(
#             "Step 1",
#             text="Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. ",  # noqa: E501
#             widget=None,
#         ),
#         StepWidget(
#             "Step 2",
#             text="Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. ",  # noqa: E501
#             widget=img_widget,
#         ),
#         StepWidget("Step 3", text=None, widget=img_widget),
#     ]
#     dbx = DialogBox(
#         dialog_text="Follow the steps and click Confirm",
#         widget=MultistepWidget(steps),
#     )
#     response = run_dialog_box(dbx)
#     assert response


# def test_small_100():
#     img_widget = ImageWidget(address="assets/test.png", width=100)
#     steps = [
#         StepWidget(
#             "Step 1",
#             text="Content for step.",
#             widget=None,
#         ),
#         StepWidget(
#             "Step 2",
#             text="Content for step.",
#             widget=img_widget,
#         ),
#         StepWidget("Step 3", text=None, widget=img_widget),
#     ]
#     dbx = DialogBox(
#         dialog_text="Follow the steps and click Confirm",
#         widget=MultistepWidget(steps),
#     )
#     response = run_dialog_box(dbx)
#     assert response


# def test_big_100_long_text():
#     img_widget = ImageWidget(address="assets/sample_1920x1280.gif", width=100)
#     steps = [
#         StepWidget(
#             "Step 1",
#             text="Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. ",  # noqa: E501
#             widget=None,
#         ),
#         StepWidget(
#             "Step 2",
#             text="Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. ",  # noqa: E501
#             widget=img_widget,
#         ),
#         StepWidget("Step 3", text=None, widget=img_widget),
#     ]
#     dbx = DialogBox(
#         dialog_text="Follow the steps and click Confirm",
#         widget=MultistepWidget(steps),
#     )
#     response = run_dialog_box(dbx)
#     assert response


# def test_big_100():
#     img_widget = ImageWidget(address="assets/sample_1920x1280.gif", width=100)
#     steps = [
#         StepWidget(
#             "Step 1",
#             text="Content for step. ",
#             widget=None,
#         ),
#         StepWidget(
#             "Step 2",
#             text="Content for step. ",
#             widget=img_widget,
#         ),
#         StepWidget("Step 3", text=None, widget=img_widget),
#     ]
#     dbx = DialogBox(
#         dialog_text="Follow the steps and click Confirm",
#         widget=MultistepWidget(steps),
#     )
#     response = run_dialog_box(dbx)
#     assert response


# def test_small_20_long_text():
#     img_widget = ImageWidget(address="assets/test.png", width=20)
#     steps = [
#         StepWidget(
#             "Step 1",
#             text="Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. ",  # noqa: E501
#             widget=None,
#         ),
#         StepWidget(
#             "Step 2",
#             text="Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. ",  # noqa: E501
#             widget=img_widget,
#         ),
#         StepWidget("Step 3", text=None, widget=img_widget),
#     ]
#     dbx = DialogBox(
#         dialog_text="Follow the steps and click Confirm",
#         widget=MultistepWidget(steps),
#     )
#     response = run_dialog_box(dbx)
#     assert response


# def test_small_20():
#     img_widget = ImageWidget(address="assets/test.png", width=20)
#     steps = [
#         StepWidget(
#             "Step 1",
#             text="Content for step.",
#             widget=None,
#         ),
#         StepWidget(
#             "Step 2",
#             text="Content for step.",
#             widget=img_widget,
#         ),
#         StepWidget("Step 3", text=None, widget=img_widget),
#     ]
#     dbx = DialogBox(
#         dialog_text="Follow the steps and click Confirm",
#         widget=MultistepWidget(steps),
#     )
#     response = run_dialog_box(dbx)
#     assert response


# def test_big_20_long_text():
#     img_widget = ImageWidget(address="assets/sample_1920x1280.gif", width=20)
#     steps = [
#         StepWidget(
#             "Step 1",
#             text="Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. ",  # noqa: E501
#             widget=None,
#         ),
#         StepWidget(
#             "Step 2",
#             text="Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. ",  # noqa: E501
#             widget=img_widget,
#         ),
#         StepWidget("Step 3", text=None, widget=img_widget),
#     ]
#     dbx = DialogBox(
#         dialog_text="Follow the steps and click Confirm",
#         widget=MultistepWidget(steps),
#     )
#     response = run_dialog_box(dbx)
#     assert response


# def test_big_20_mixed():
#     img_widget = ImageWidget(address="assets/sample_1920x1280.gif", width=20)
#     steps = [
#         StepWidget(
#             "Step 1",
#             text="Content for step. ",
#             widget=None,
#         ),
#         StepWidget(
#             "Step 2",
#             text="Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. ",  # noqa: E501
#             widget=img_widget,
#         ),
#         StepWidget("Step 3", text=None, widget=img_widget),
#     ]
#     dbx = DialogBox(
#         dialog_text="Follow the steps and click Confirm",
#         widget=MultistepWidget(steps),
#     )
#     response = run_dialog_box(dbx)
#     assert response


# def test_small_200_long_text():
#     img_widget = ImageWidget(address="assets/test.png", width=200)
#     steps = [
#         StepWidget(
#             "Step 1",
#             text="Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. ",  # noqa: E501
#             widget=None,
#         ),
#         StepWidget(
#             "Step 2",
#             text="Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. ",  # noqa: E501
#             widget=img_widget,
#         ),
#         StepWidget("Step 3", text=None, widget=img_widget),
#     ]
#     dbx = DialogBox(
#         dialog_text="Follow the steps and click Confirm",
#         widget=MultistepWidget(steps),
#     )
#     response = run_dialog_box(dbx)
#     assert response


# def test_small_200():
#     img_widget = ImageWidget(address="assets/test.png", width=200)
#     steps = [
#         StepWidget(
#             "Step 1",
#             text="Content for step.",
#             widget=None,
#         ),
#         StepWidget(
#             "Step 2",
#             text="Content for step.",
#             widget=img_widget,
#         ),
#         StepWidget("Step 3", text=None, widget=img_widget),
#     ]
#     dbx = DialogBox(
#         dialog_text="Follow the steps and click Confirm",
#         widget=MultistepWidget(steps),
#     )
#     response = run_dialog_box(dbx)
#     assert response


# def test_big_200_long_text():
#     img_widget = ImageWidget(address="assets/sample_1920x1280.gif", width=200)
#     steps = [
#         StepWidget(
#             "Step 1",
#             text="Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. ",  # noqa: E501
#             widget=None,
#         ),
#         StepWidget(
#             "Step 2",
#             text="Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. ",  # noqa: E501
#             widget=img_widget,
#         ),
#         StepWidget("Step 3", text=None, widget=img_widget),
#     ]
#     dbx = DialogBox(
#         dialog_text="Follow the steps and click Confirm",
#         widget=MultistepWidget(steps),
#     )
#     response = run_dialog_box(dbx)
#     assert response


# def test_big_200_mixed():
#     img_widget = ImageWidget(address="assets/sample_1920x1280.gif", width=200)
#     steps = [
#         StepWidget(
#             "Step 1",
#             text="Content for step. ",
#             widget=None,
#         ),
#         StepWidget(
#             "Step 2",
#             text="Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. ",  # noqa: E501
#             widget=img_widget,
#         ),
#         StepWidget("Step 3", text=None, widget=img_widget),
#     ]
#     dbx = DialogBox(
#         dialog_text="Follow the steps and click Confirm",
#         widget=MultistepWidget(steps),
#     )
#     response = run_dialog_box(dbx)
#     assert response


# def test_5mb_200_long_text():
#     img_widget = ImageWidget(address="assets/test_5_mb.jpg", width=200)
#     steps = [
#         StepWidget(
#             "Step 1",
#             text="Content for step. ",
#             widget=None,
#         ),
#         StepWidget(
#             "Step 2",
#             text="Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. Content for step. ",  # noqa: E501
#             widget=img_widget,
#         ),
#         StepWidget("Step 3", text=None, widget=img_widget),
#     ]
#     dbx = DialogBox(
#         dialog_text="Follow the steps and click Confirm",
#         widget=MultistepWidget(steps),
#     )
#     response = run_dialog_box(dbx)
#     assert response


def test_multiple_steps_different_images():
    img_widget = ImageWidget(address="assets/test.png", width=100)
    img_widget_2 = ImageWidget(address="assets/sample_1920x1280.gif", width=100)
    steps = [
        StepWidget("Step 1", text="AAA", widget=None),
        StepWidget("Step 2", text="AAA", widget=img_widget),
        StepWidget("Step 3", text=None, widget=img_widget_2),
    ]
    dbx = DialogBox(dialog_text="BBB", widget=MultistepWidget(steps))
    response = run_dialog_box(dbx)
    assert response


def test_multiple_steps_different_images_in_other_order():
    img_widget = ImageWidget(address="assets/test.png", width=100)
    img_widget_2 = ImageWidget(address="assets/sample_1920x1280.gif", width=100)
    steps = [
        StepWidget("Step 1", text="AAA", widget=None),
        StepWidget("Step 2", text="AAA", widget=img_widget_2),
        StepWidget("Step 3", text=None, widget=img_widget),
    ]
    dbx = DialogBox(dialog_text="BBB", widget=MultistepWidget(steps))
    response = run_dialog_box(dbx)
    assert response


def test_multiple_steps_different_images_different_percent():
    img_widget = ImageWidget(address="assets/test.png", width=50)
    img_widget_2 = ImageWidget(address="assets/sample_1920x1280.gif", width=100)
    steps = [
        StepWidget("Step 1", text="AAA", widget=None),
        StepWidget("Step 2", text="AAA", widget=img_widget),
        StepWidget("Step 3", text=None, widget=img_widget_2),
    ]
    dbx = DialogBox(dialog_text="BBB", widget=MultistepWidget(steps))
    response = run_dialog_box(dbx)
    assert response


def test_multiple_steps_different_percent():
    img_widget = ImageWidget(address="assets/test.png", width=20)
    img_widget_2 = ImageWidget(address="assets/test.png", width=50)
    img_widget_3 = ImageWidget(address="assets/test.png", width=100)
    img_widget_4 = ImageWidget(address="assets/test.png", width=150)
    img_widget_5 = ImageWidget(address="assets/test.png", width=200)
    steps = [
        StepWidget("Step 1", text="AAA", widget=img_widget),
        StepWidget("Step 2", text="AAA", widget=img_widget_2),
        StepWidget("Step 3", text="AAA", widget=img_widget_3),
        StepWidget("Step 4", text="AAA", widget=img_widget_4),
        StepWidget("Step 5", text="AAA", widget=img_widget_5),
    ]
    dbx = DialogBox(dialog_text="BBB", widget=MultistepWidget(steps))
    response = run_dialog_box(dbx)
    assert response


def test_multiple_steps_different_percent_recursion():
    img_widget = ImageWidget(address="assets/test.png", width=20)
    img_widget_2 = ImageWidget(address="assets/test.png", width=50)
    img_widget_3 = ImageWidget(address="assets/test.png", width=100)
    img_widget_4 = ImageWidget(address="assets/test.png", width=150)
    img_widget_5 = ImageWidget(address="assets/test.png", width=200)
    steps = [
        StepWidget("Step 1", text="AAA", widget=img_widget_5),
        StepWidget("Step 2", text="AAA", widget=img_widget_4),
        StepWidget("Step 3", text="AAA", widget=img_widget_3),
        StepWidget("Step 4", text="AAA", widget=img_widget_2),
        StepWidget("Step 5", text="AAA", widget=img_widget),
    ]
    dbx = DialogBox(dialog_text="BBB", widget=MultistepWidget(steps))
    response = run_dialog_box(dbx)
    assert response


def test_small_100_long_text_with_line_break():
    img_widget = ImageWidget(address="assets/test.png", width=100)
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


def test_horizontal_and_vertical_stripes():
    img_widget_1 = ImageWidget(address="assets/horizontal_stripe.png", width=100)
    img_widget_2 = ImageWidget(address="assets/vertical_stripe.png", width=100)
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
            widget=img_widget_1,
        ),
        StepWidget("Step 3", text=None, widget=img_widget_2),
    ]
    dbx = DialogBox(
        dialog_text="Follow the steps and click Confirm",
        widget=MultistepWidget(steps),
    )
    response = run_dialog_box(dbx)
    assert response


def test_vertical_and_horizontal_stripes():
    img_widget_1 = ImageWidget(address="assets/horizontal_stripe.png", width=100)
    img_widget_2 = ImageWidget(address="assets/vertical_stripe.png", width=100)
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
            widget=img_widget_2,
        ),
        StepWidget("Step 3", text=None, widget=img_widget_1),
    ]
    dbx = DialogBox(
        dialog_text="Follow the steps and click Confirm",
        widget=MultistepWidget(steps),
    )
    response = run_dialog_box(dbx)
    assert response
