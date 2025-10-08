import pytest

from hardpy import DialogBox, ImageComponent, run_dialog_box

pytestmark = pytest.mark.module_name("Base dialog box")


@pytest.mark.case_name("Empty test before")
def test_before():
    assert True


@pytest.mark.case_name("Base dialog box")
def test_base_dialog_box():
    dbx = DialogBox(
        title_bar="Operator check",
        dialog_text="Press the Confirm button",
    )
    response = run_dialog_box(dbx)
    assert response


@pytest.mark.case_name("Pass/Fail dialog box example")
def test_pass_fail_dialog_box():
    """Test case demonstrating pass/fail dialog box functionality."""
    dbx = DialogBox(
        title_bar="Manual Verification Required",
        dialog_text="Please check the test result manually.\n\nIs the LED blinking correctly?\n\nClick PASS if yes, FAIL if no.",
        pass_fail=True,
    )
    result = run_dialog_box(dbx)

    # The result will be True for PASS, False for FAIL
    # For demonstration purposes, we'll accept both outcomes
    if result:
        print("✅ Test PASSED - User clicked PASS")
        assert True
    else:
        print("❌ Test FAILED - User clicked FAIL")
        # In a real test, you might want to fail here:
        # assert False, "User indicated test failed"
        # But for this example, we'll just log it
        assert True  # Accept both outcomes for demo


@pytest.mark.case_name("Pass/Fail dialog box example")
def test_pass_fail_dialog_box_with_image():
    """Test case demonstrating pass/fail dialog box functionality."""
    dbx = DialogBox(
        title_bar="Manual Verification Required",
        dialog_text="Please check the test result manually.\n\nIs the LED blinking correctly?\n\nClick PASS if yes, FAIL if no.",
        pass_fail=True,
        image=ImageComponent(address="assets/test.png", width=100),
    )
    result = run_dialog_box(dbx)

    # The result will be True for PASS, False for FAIL
    # For demonstration purposes, we'll accept both outcomes
    if result:
        print("✅ Test PASSED - User clicked PASS")
        assert True
    else:
        print("❌ Test FAILED - User clicked FAIL")
        # In a real test, you might want to fail here:
        # assert False, "User indicated test failed"
        # But for this example, we'll just log it
        assert True  # Accept both outcomes for demo


@pytest.mark.case_name("Base dialog box with image")
def test_base_dialog_box_with_image():
    dbx = DialogBox(
        title_bar="Operator check",
        dialog_text="Press the Confirm button",
        image=ImageComponent(address="assets/test.png", width=100),
    )
    response = run_dialog_box(dbx)
    assert response


@pytest.mark.case_name("Empty test after")
def test_after():
    assert True
