import pytest
import hardpy


# hardpy run

# hardpy start --arg test_mode=debug --arg device_id=DUT-007 --arg retry_count=3

pytestmark = pytest.mark.module_name("HardPy template")

def test_with_start_args(hardpy_start_args):

    if hardpy_start_args.get("test_mode") == "debug":
        hardpy.set_message("Running in debug mode")

    device_id = hardpy_start_args.get("device_id")
    if device_id:
        hardpy.set_message(f"Testing device: {device_id}")
        hardpy.set_case_artifact({"device_id": device_id})
    else:
        hardpy.set_message("No device ID provided")
