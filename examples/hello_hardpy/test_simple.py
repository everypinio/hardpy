import pytest

from uuid import uuid4

import hardpy
from hardpy import set_dut_sub_unit, SubUnit


def test_dut_serial_number():
    report = hardpy.get_current_report()
    assert report.dut.sub_units == [], "Sub units is not empty before start."

    serial_number = str(uuid4())[:6]
    part_number = "part_number_1"
    name = "Test Device"
    type = "PCBA"
    revision = "REV1.0"
    info = {
        "sw_version": "1.0",
    }
    sub_unit = SubUnit(
        serial_number=serial_number,
        part_number=part_number,
        name=name,
        type=type,
        revision=revision,
        info=info,
    )
    hardpy.set_dut_sub_unit(sub_unit)
    report = hardpy.get_current_report()
    assert serial_number == report.dut.sub_units[0].serial_number
    assert part_number == report.dut.sub_units[0].part_number
    assert name == report.dut.sub_units[0].name
    assert type == report.dut.sub_units[0].type
    assert revision == report.dut.sub_units[0].revision
    assert info == report.dut.sub_units[0].info

    serial_number_2 = str(uuid4())[:6]
    part_number_2 = "part_number_2"
    name_2 = "Test Device 2"
    type_2 = "PCBA"
    revision_2 = "REV2.0"
    info_2 = {
        "sw_version": "1.1",
    }

    sub_unit_2 = SubUnit(
        serial_number=serial_number_2,
        part_number=part_number_2,
        name=name_2,
        type=type_2,
        revision=revision_2,
        info=info_2,
    )
    hardpy.set_dut_sub_unit(sub_unit_2)
    report = hardpy.get_current_report()
    assert serial_number_2 == report.dut.sub_units[1].serial_number
    assert part_number_2 == report.dut.sub_units[1].part_number
    assert name_2 == report.dut.sub_units[1].name
    assert type_2 == report.dut.sub_units[1].type
    assert revision_2 == report.dut.sub_units[1].revision
    assert info_2 == report.dut.sub_units[1].info
