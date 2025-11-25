import pytest

from hardpy import (
    Group,
    Instrument,
    set_instrument,
    set_process_name,
    set_process_number,
    set_stand_name,
    set_stand_number,
    set_stand_revision,
)

pytestmark = [
    pytest.mark.module_name("Test run information"),
    pytest.mark.module_group(Group.SETUP),
]


@pytest.mark.case_name("Process")
def test_process_info():
    process_name = "System Test"
    process_number = 3
    set_process_name(process_name)
    set_process_number(process_number)


@pytest.mark.case_name("Stand")
def test_stand_info():
    stand_name = "System check"
    stand_number = 1
    stand_revision = "HW1.1"
    set_stand_name(stand_name)
    set_stand_number(stand_number)
    set_stand_revision(stand_revision)


@pytest.mark.case_name("Instrument")
def test_instrument_info():
    instrument = Instrument(name="System driver", revision="2.0")
    set_instrument(instrument)


def test_dut_info():
    part_number = "part_number_1"
    type = "PCBA"
    revision = "REV1.0"

