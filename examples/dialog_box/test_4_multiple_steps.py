import pytest

from hardpy import (
    DialogBox,
    HTMLComponent,
    ImageComponent,
    MultistepWidget,
    StepWidget,
    run_dialog_box,
)

pytestmark = pytest.mark.module_name("Multiple steps dialog box")


test_html = """
<!DOCTYPE html>
<html>
<body>

<h1>Test HTML Page</h1>

<p>It is testing page.</p>
<p>You can put anything on it.</p>

</body>
</html>
"""


@pytest.mark.case_name("Multistep")
def test_multiple_steps():
    steps = [
        StepWidget("Step 1", text="Content for step"),
        StepWidget(
            "Step 2",
            text="Content for step 2",
            image=ImageComponent(address="assets/test.png", width=100),
        ),
        StepWidget(
            "Step 3",
            text=None,
            html=HTMLComponent(
                html=test_html,
                is_raw_html=True,
            ),
        ),
    ]
    dbx = DialogBox(
        dialog_text="Follow the steps and click Confirm",
        widget=MultistepWidget(steps),
    )
    response = run_dialog_box(dbx)
    assert response


@pytest.mark.case_name("Multistep with image")
def test_multiple_steps_with_main_image():
    steps = [
        StepWidget("Step 1", text="Content for step"),
        StepWidget(
            "Step 2",
            text="Content for step 2",
            image=ImageComponent(address="assets/test.png", width=100),
        ),
        StepWidget(
            "Step 3",
            text=None,
            image=ImageComponent(address="assets/test.png", width=50),
        ),
        StepWidget(
            "Step 4",
            text=None,
            html=HTMLComponent(
                html=test_html,
                is_raw_html=True,
            ),
        ),
        StepWidget(
            "Step 5",
            text=None,
            image=ImageComponent(address="assets/test.png", width=50),
            html=HTMLComponent(
                html=test_html,
                is_raw_html=True,
            ),
        ),
    ]
    dbx = DialogBox(
        dialog_text="Follow the steps and click Confirm",
        widget=MultistepWidget(steps),
        image=ImageComponent(address="assets/test.png", width=50),
    )
    response = run_dialog_box(dbx)
    assert response


@pytest.mark.case_name("Multistep with html")
def test_multiple_steps_with_main_html():
    steps = [
        StepWidget("Step 1", text="Content for step"),
        StepWidget(
            "Step 2",
            text="Content for step 2",
            image=ImageComponent(address="assets/test.png", width=100),
        ),
        StepWidget(
            "Step 3",
            text=None,
            image=ImageComponent(address="assets/test.png", width=50),
        ),
        StepWidget(
            "Step 4",
            text=None,
            html=HTMLComponent(
                html=test_html,
                is_raw_html=True,
            ),
        ),
        StepWidget(
            "Step 5",
            text=None,
            image=ImageComponent(address="assets/test.png", width=50),
            html=HTMLComponent(
                html=test_html,
                is_raw_html=True,
            ),
        ),
    ]
    dbx = DialogBox(
        dialog_text="Follow the steps and click Confirm",
        widget=MultistepWidget(steps),
        html=HTMLComponent(
            html=test_html,
            is_raw_html=True,
        ),
    )
    response = run_dialog_box(dbx)
    assert response


@pytest.mark.case_name("Multistep with html and image")
def test_multiple_steps_with_main_html_and_main_image():
    steps = [
        StepWidget("Step 1", text="Content for step"),
        StepWidget(
            "Step 2",
            text="Content for step 2",
            image=ImageComponent(address="assets/test.png", width=100),
        ),
        StepWidget(
            "Step 3",
            text=None,
            image=ImageComponent(address="assets/test.png", width=50),
        ),
        StepWidget(
            "Step 4",
            text=None,
            html=HTMLComponent(
                html=test_html,
                is_raw_html=True,
            ),
        ),
        StepWidget(
            "Step 5",
            text=None,
            image=ImageComponent(address="assets/test.png", width=50),
            html=HTMLComponent(
                html=test_html,
                is_raw_html=True,
            ),
        ),
    ]
    dbx = DialogBox(
        dialog_text="Follow the steps and click Confirm",
        widget=MultistepWidget(steps),
        image=ImageComponent(address="assets/test.png", width=50),
        html=HTMLComponent(
            html=test_html,
            is_raw_html=True,
        ),
    )
    response = run_dialog_box(dbx)
    assert response


@pytest.mark.case_name("Multistep with pass_fail")
def test_multiple_steps_with_pass_fail():
    steps = [
        StepWidget("Step 1", text="Content for step"),
        StepWidget(
            "Step 2",
            text="Content for step 2",
            image=ImageComponent(address="assets/test.png", width=100),
        ),
        StepWidget(
            "Step 3",
            text=None,
            html=HTMLComponent(
                html=test_html,
                is_raw_html=True,
            ),
        ),
    ]
    dbx = DialogBox(
        dialog_text="Follow the steps and click Pass or Fail",
        widget=MultistepWidget(steps),
        pass_fail=True,
    )
    response = run_dialog_box(dbx)
    assert response.result
    assert response.data
