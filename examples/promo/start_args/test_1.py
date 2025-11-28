import pytest
import hardpy


# hardpy run

# hardpy start --arg test_station_id=STATION-42 --arg device_serial=DUT-007 --arg test_retry_count=3

pytestmark = pytest.mark.module_name("Production Test - Device Configuration")


def test_device_configuration_validation(hardpy_start_args):
    if hardpy_start_args.get("test_station_id"):
        hardpy.set_message(
            f"Test station initialized: {hardpy_start_args['test_station_id']}"
        )

    device_serial = hardpy_start_args.get("device_serial")
    if device_serial:
        hardpy.set_message(f"Testing device with serial number: {device_serial}")
        hardpy.set_case_artifact({"device_serial_number": device_serial})
    else:
        hardpy.set_message("Warning: No device serial number provided")

    test_retry_count = hardpy_start_args.get("test_retry_count")
    if test_retry_count:
        hardpy.set_message(f"Test retry count configured: {test_retry_count}")
