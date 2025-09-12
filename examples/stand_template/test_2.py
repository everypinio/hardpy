import pytest
from utils import ProjectErrorCode, SystemDriver

from hardpy import ErrorCode, Group

pytestmark = [
    pytest.mark.module_name("Test run information"),
    pytest.mark.module_group(Group.SETUP),
]


@pytest.mark.case_name("System driver connect")
@pytest.mark.critical
def test_system_driver_connect(system_driver: SystemDriver):
    is_connected = system_driver.connect()
    assert is_connected, ErrorCode(
        ProjectErrorCode.SYSTEM_DRIVER_NOT_CONNECTED,
        "System driver not connected",
    )
