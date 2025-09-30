from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from pytest import Pytester

func_test_header = """
        from uuid import uuid4

        import pytest

        import hardpy
        from hardpy.pytest_hardpy.utils import NodeInfo
        """


def test_dut_serial_number(pytester: Pytester, hardpy_opts: list[str]):
    pytester.makepyfile(
        f"""
        {func_test_header}
        from hardpy import DuplicateParameterError

        def test_dut_serial_number():
            report = hardpy.get_current_report()
            assert (
                report.dut.serial_number is None
            ), "Serial number is not empty before start."

            serial_number = str(uuid4())[:6]
            hardpy.set_dut_serial_number(serial_number)
            report = hardpy.get_current_report()
            assert serial_number == report.dut.serial_number

            second_serial_number = "incorrect serial number"
            with pytest.raises(DuplicateParameterError):
                hardpy.set_dut_serial_number(second_serial_number)
    """,
    )

    result = pytester.runpytest(*hardpy_opts)
    result.assert_outcomes(passed=1)


def test_dut_part_number(pytester: Pytester, hardpy_opts: list[str]):
    pytester.makepyfile(
        f"""
        {func_test_header}
        from hardpy import DuplicateParameterError

        def test_dut_part_number():
            report = hardpy.get_current_report()
            assert (
                report.dut.part_number is None
            ), "Part number is not empty before start."

            part_number = str(uuid4())[:6]
            hardpy.set_dut_part_number(part_number)
            report = hardpy.get_current_report()
            assert part_number == report.dut.part_number

            second_part_number = "incorrect part number"
            with pytest.raises(DuplicateParameterError):
                hardpy.set_dut_part_number(second_part_number)
    """,
    )

    result = pytester.runpytest(*hardpy_opts)
    result.assert_outcomes(passed=1)


def test_empty_dut_serial_number(pytester: Pytester, hardpy_opts: list[str]):
    pytester.makepyfile(
        f"""
        {func_test_header}
        from hardpy import DuplicateParameterError

        def test_empty_dut_serial_number():
            report = hardpy.get_current_report()
            assert (
                report.dut.serial_number is None
            ), "Serial number is not empty before start."

            serial_number = None
            hardpy.set_dut_serial_number(serial_number)
            report = hardpy.get_current_report()
            assert serial_number == report.dut.serial_number
    """,
    )

    result = pytester.runpytest(*hardpy_opts)
    result.assert_outcomes(failed=1)


def test_clean_dut_serial_number(pytester: Pytester, hardpy_opts: list[str]):
    pytester.makepyfile(
        f"""
        {func_test_header}
        from hardpy import DuplicateParameterError

        def test_clean_dut_serial_number():
            report = hardpy.get_current_report()
            assert (
                report.dut.serial_number is None
            ), "Serial number is not empty before start."
    """,
    )

    result = pytester.runpytest(*hardpy_opts)
    result.assert_outcomes(passed=1)


def test_dut_info(pytester: Pytester, hardpy_opts: list[str]):
    pytester.makepyfile(
        f"""
        {func_test_header}
        def test_dut_info():
            report = hardpy.get_current_report()
            assert report.dut.info == dict(), "The dut info is not empty."

            info = {{"batch": "test_batch", "board_rev": "rev_1"}}
            hardpy.set_dut_info(info)
            report = hardpy.get_current_report()
            assert info == report.dut.info

            info = {{"manufacturer": "Everypin", "sw_version": "0.1"}}
            info_before_write = report.dut.info | info
            hardpy.set_dut_info(info)
            report = hardpy.get_current_report()
            assert info_before_write == report.dut.info
    """,
    )
    result = pytester.runpytest(*hardpy_opts)
    result.assert_outcomes(passed=1)


def test_empty_dut_info(pytester: Pytester, hardpy_opts: list[str]):
    pytester.makepyfile(
        f"""
        {func_test_header}
        def test_empty_dut_info():
            report = hardpy.get_current_report()
            assert report.dut.info == dict(), "The dut info is not empty."

            info = {{}}
            hardpy.set_dut_info(info)
            report = hardpy.get_current_report()
            assert info == report.dut.info

            info = {{}}
            info_before_write = report.dut.info | info
            hardpy.set_dut_info(info)
            report = hardpy.get_current_report()
            assert info_before_write == report.dut.info
    """,
    )
    result = pytester.runpytest(*hardpy_opts)
    result.assert_outcomes(passed=1)


def test_dut_sub_unit(pytester: Pytester, hardpy_opts: list[str]):
    pytester.makepyfile(
        f"""
        {func_test_header}
        from hardpy import set_dut_sub_unit, SubUnit

        def test_sub_unit():
            report = hardpy.get_current_report()
            assert report.dut.sub_units == [], "Sub units are not empty before start."

            serial_number = str(uuid4())[:6]
            part_number = "part_number_1"
            name = "Test Device"
            type = "PCBA"
            revision = "REV1.0"
            info = {{"sw_version": "1.0"}}
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

            sub_unit_2 = SubUnit(
                serial_number=serial_number_2,
                part_number=part_number_2,
                name=name_2,
                type=type_2,
                revision=revision_2,
            )
            hardpy.set_dut_sub_unit(sub_unit_2)
            report = hardpy.get_current_report()
            assert serial_number_2 == report.dut.sub_units[1].serial_number
            assert part_number_2 == report.dut.sub_units[1].part_number
            assert name_2 == report.dut.sub_units[1].name
            assert type_2 == report.dut.sub_units[1].type
            assert revision_2 == report.dut.sub_units[1].revision
            assert {{}} == report.dut.sub_units[1].info
    """,
    )

    result = pytester.runpytest(*hardpy_opts)
    result.assert_outcomes(passed=1)


def test_stand_name(pytester: Pytester, hardpy_opts: list[str]):
    pytester.makepyfile(
        f"""
        {func_test_header}
        from hardpy import DuplicateParameterError

        def test_stand_name():
            report = hardpy.get_current_report()
            assert (
                report.test_stand.name is None
            ), "Test stand name is not empty before start."

            name = str(uuid4())[:6]
            hardpy.set_stand_name(name)
            report = hardpy.get_current_report()
            assert name == report.test_stand.name

            second_name = "incorrect name"
            with pytest.raises(DuplicateParameterError):
                hardpy.set_stand_name(second_name)
    """,
    )
    result = pytester.runpytest(*hardpy_opts)
    result.assert_outcomes(passed=1)


def test_stand_location(pytester: Pytester, hardpy_opts: list[str]):
    pytester.makepyfile(
        f"""
        {func_test_header}
        from hardpy import DuplicateParameterError

        def test_stand_location():
            report = hardpy.get_current_report()
            assert (
                report.test_stand.location is None
            ), "Test stand location is not empty before start."

            location = "Moon"
            hardpy.set_stand_location(location)
            report = hardpy.get_current_report()
            assert location == report.test_stand.location

            second_location = "incorrect location"
            with pytest.raises(DuplicateParameterError):
                hardpy.set_stand_location(second_location)
    """,
    )
    result = pytester.runpytest(*hardpy_opts)
    result.assert_outcomes(passed=1)


def test_stand_duplicate_number(pytester: Pytester, hardpy_opts: list[str]):
    pytester.makepyfile(
        f"""
        {func_test_header}
        from hardpy import DuplicateParameterError

        def test_stand_number():
            report = hardpy.get_current_report()
            assert (
                report.test_stand.number is None
            ), "Test stand number is not empty before start."

            stand_number = 1
            hardpy.set_stand_number(stand_number)
            report = hardpy.get_current_report()
            assert stand_number == report.test_stand.number

            second_number = 2
            with pytest.raises(DuplicateParameterError):
                hardpy.set_stand_number(second_number)
    """,
    )
    result = pytester.runpytest(*hardpy_opts)
    result.assert_outcomes(passed=1)


def test_stand_incorrect_number(pytester: Pytester, hardpy_opts: list[str]):
    pytester.makepyfile(
        f"""
        {func_test_header}
        from hardpy import TestStandNumberError

        def test_stand_negative_number():
            stand_number = -1
            with pytest.raises(TestStandNumberError):
                hardpy.set_stand_number(stand_number)

        def test_stand_float_number():
            stand_number = 1.1
            with pytest.raises(TestStandNumberError):
                hardpy.set_stand_number(stand_number)

        def test_stand_str_number():
            stand_number = "1"
            with pytest.raises(TestStandNumberError):
                hardpy.set_stand_number(stand_number)
    """,
    )
    result = pytester.runpytest(*hardpy_opts)
    result.assert_outcomes(passed=3)


def test_stand_info(pytester: Pytester, hardpy_opts: list[str]):
    pytester.makepyfile(
        f"""
        {func_test_header}
        def test_stand_info():
            report = hardpy.get_current_report()
            assert report.test_stand == dict(), "The test stand info is not empty."

            info = {{"adssf"}}
            hardpy.set_stand_info(info)
            report = hardpy.get_current_report()
            assert info == report.test_stand

            info = {{"sgdfssgd"}}
            stand_info_before_write = report.test_stand | info
            hardpy.set_stand_info(info)
            report = hardpy.get_current_report()
            assert stand_info_before_write == report.test_stand
    """,
    )
    result = pytester.runpytest(*hardpy_opts)
    result.assert_outcomes(failed=1)


def test_drivers(pytester: Pytester, hardpy_opts: list[str]):
    pytester.makepyfile(
        f"""
        {func_test_header}
        def test_drivers():
            report = hardpy.get_current_report()
            assert report.test_stand.drivers == dict(), "The drivers data is not empty."

            drivers = {{"driver_1": "driver info"}}
            hardpy.set_driver_info(drivers)
            report = hardpy.get_current_report()
            assert drivers == report.test_stand.drivers

            drivers = {{
                "driver_2": {{
                    "state": "active",
                    "port": 8000,
                }}
            }}
            drivers_before_write = report.test_stand.drivers | drivers
            hardpy.set_driver_info(drivers)
            report = hardpy.get_current_report()
            assert drivers_before_write == report.test_stand.drivers
    """,
    )
    result = pytester.runpytest(*hardpy_opts)
    result.assert_outcomes(passed=1)


def test_empty_drivers_data(pytester: Pytester, hardpy_opts: list[str]):
    pytester.makepyfile(
        f"""
        {func_test_header}
        def test_empty_drivers_data():
            report_before = hardpy.get_current_report()
            drivers = {{}}
            hardpy.set_driver_info(drivers)
            report_after = hardpy.get_current_report()
            assert report_before.test_stand.drivers == report_after.test_stand.drivers
    """,
    )
    result = pytester.runpytest(*hardpy_opts)
    result.assert_outcomes(passed=1)


def test_incorrect_drivers_data(pytester: Pytester, hardpy_opts: list[str]):
    pytester.makepyfile(
        f"""
        {func_test_header}
        def test_incorrect_drivers_data():
            report = hardpy.get_current_report()
            assert report.drivers == dict(), "The drivers data is not empty."

            drivers = {{"sdfdkjshfkjs"}}
            hardpy.set_driver_info(drivers)
            report = hardpy.get_current_report()
            assert drivers == report.drivers

            drivers = {{
                "driver_2": {{"dfkjhgdkhkjgf"
                }}
            }}
            drivers_before_write = report.drivers | drivers
            hardpy.set_driver_info(drivers)
            report = hardpy.get_current_report()
            assert drivers_before_write == report.drivers
    """,
    )
    result = pytester.runpytest(*hardpy_opts)
    result.assert_outcomes(failed=1)


def test_module_artifact(pytester: Pytester, hardpy_opts: list[str]):
    pytester.makepyfile(
        f"""
        {func_test_header}
        def test_module_artifact(request):
            node = NodeInfo(request.node)

            report = hardpy.get_current_report()
            empty_artifact = report.modules[node.module_id].artifact
            assert empty_artifact == dict(), "The test module artifact is not empty."

            artifact_data = {{"data_str": "789DATA"}}
            hardpy.set_module_artifact(artifact_data)
            report = hardpy.get_current_report()
            read_artifact = report.modules[node.module_id].artifact
            assert artifact_data == read_artifact

            artifact_data = {{
                "data_int": 12345, "data_dict": {{"test_key": "456DATA"}}
            }}
            artifact_before_write = read_artifact | artifact_data
            hardpy.set_module_artifact(artifact_data)
            report = hardpy.get_current_report()
            read_artifact = report.modules[node.module_id].artifact
            assert read_artifact == artifact_before_write
    """,
    )
    result = pytester.runpytest(*hardpy_opts)
    result.assert_outcomes(passed=1)


def test_empty_module_artifact_data(pytester: Pytester, hardpy_opts: list[str]):
    pytester.makepyfile(
        f"""
        {func_test_header}
        def test_empty_module_artifact_data(request):
            node = NodeInfo(request.node)

            report = hardpy.get_current_report()
            empty_artifact = report.modules[node.module_id].artifact
            assert empty_artifact == dict(), "The test module artifact is not empty."

            artifact_data = {{}}
            hardpy.set_module_artifact(artifact_data)
            report = hardpy.get_current_report()
            read_artifact = report.modules[node.module_id].artifact
            assert artifact_data == read_artifact

            artifact_data = {{}}
            artifact_before_write = read_artifact | artifact_data
            hardpy.set_module_artifact(artifact_data)
            report = hardpy.get_current_report()
            read_artifact = report.modules[node.module_id].artifact
            assert read_artifact == artifact_before_write
    """,
    )
    result = pytester.runpytest(*hardpy_opts)
    result.assert_outcomes(passed=1)


def test_incorrect_module_artifact_data(pytester: Pytester, hardpy_opts: list[str]):
    pytester.makepyfile(
        f"""
        {func_test_header}
        def test_incorrect_module_artifact_data(request):
            node = NodeInfo(request.node)

            report = hardpy.get_current_report()
            empty_artifact = report.modules[node.module_id].artifact
            assert empty_artifact == dict(), "The test module artifact is not empty."

            artifact_data = {{"ashdgajghj"}}
            hardpy.set_module_artifact(artifact_data)
            report = hardpy.get_current_report()
            read_artifact = report.modules[node.module_id].artifact
            assert artifact_data == read_artifact

            artifact_data = {{"ashdgajghj"}}
            artifact_before_write = read_artifact | artifact_data
            hardpy.set_module_artifact(artifact_data)
            report = hardpy.get_current_report()
            read_artifact = report.modules[node.module_id].artifact
            assert read_artifact == artifact_before_write
    """,
    )
    result = pytester.runpytest(*hardpy_opts)
    result.assert_outcomes(failed=1)


def test_case_artifact(pytester: Pytester, hardpy_opts: list[str]):
    pytester.makepyfile(
        f"""
        {func_test_header}
        def test_case_artifact(request):
            node = NodeInfo(request.node)

            report = hardpy.get_current_report()
            empty_artifact = report.modules[node.module_id].cases[node.case_id].artifact
            assert empty_artifact == dict(), "The test case artifact is not empty."

            artifact_data = {{"data_str": "123DATA"}}
            hardpy.set_case_artifact(artifact_data)
            report = hardpy.get_current_report()
            read_artifact = report.modules[node.module_id].cases[node.case_id].artifact
            assert artifact_data == read_artifact

            artifact_data = {{
                "data_int": 12345, "data_dict": {{"test_key": "456DATA"}}
            }}
            artifact_before_write = read_artifact | artifact_data
            hardpy.set_case_artifact(artifact_data)
            report = hardpy.get_current_report()
            read_artifact = report.modules[node.module_id].cases[node.case_id].artifact
            assert read_artifact == artifact_before_write
    """,
    )
    result = pytester.runpytest(*hardpy_opts)
    result.assert_outcomes(passed=1)


def test_empty_case_artifact_data(pytester: Pytester, hardpy_opts: list[str]):
    pytester.makepyfile(
        f"""
        {func_test_header}
        def test_empty_case_artifact_data(request):
            node = NodeInfo(request.node)

            report = hardpy.get_current_report()
            empty_artifact = report.modules[node.module_id].cases[node.case_id].artifact
            assert empty_artifact == dict(), "The test case artifact is not empty."

            artifact_data = {{}}
            hardpy.set_case_artifact(artifact_data)
            report = hardpy.get_current_report()
            read_artifact = report.modules[node.module_id].cases[node.case_id].artifact
            assert artifact_data == read_artifact

            artifact_data = {{}}
            artifact_before_write = read_artifact | artifact_data
            hardpy.set_case_artifact(artifact_data)
            report = hardpy.get_current_report()
            read_artifact = report.modules[node.module_id].cases[node.case_id].artifact
            assert read_artifact == artifact_before_write
    """,
    )
    result = pytester.runpytest(*hardpy_opts)
    result.assert_outcomes(passed=1)


def test_incorrect_case_artifact_data(pytester: Pytester, hardpy_opts: list[str]):
    pytester.makepyfile(
        f"""
        {func_test_header}
        def test_incorrect_case_artifact_data(request):
            node = NodeInfo(request.node)

            report = hardpy.get_current_report()
            empty_artifact = report.modules[node.module_id].cases[node.case_id].artifact
            assert empty_artifact == dict(), "The test case artifact is not empty."

            artifact_data = {{"kjfdhgskjsfd"}}
            hardpy.set_case_artifact(artifact_data)
            report = hardpy.get_current_report()
            read_artifact = report.modules[node.module_id].cases[node.case_id].artifact
            assert artifact_data == read_artifact

            artifact_data = {{
                "dsjfdkshlajlk"
            }}
            artifact_before_write = read_artifact | artifact_data
            hardpy.set_case_artifact(artifact_data)
            report = hardpy.get_current_report()
            read_artifact = report.modules[node.module_id].cases[node.case_id].artifact
            assert read_artifact == artifact_before_write
    """,
    )
    result = pytester.runpytest(*hardpy_opts)
    result.assert_outcomes(failed=1)


def test_run_artifact(pytester: Pytester, hardpy_opts: list[str]):
    pytester.makepyfile(
        f"""
        {func_test_header}
        def test_run_artifact(request):
            report = hardpy.get_current_report()
            empty_artifact = report.artifact
            assert empty_artifact == dict(), "The test run artifact is not empty."

            artifact_data = {{"data_str": "456DATA"}}
            hardpy.set_run_artifact(artifact_data)
            report = hardpy.get_current_report()
            read_artifact = report.artifact
            assert artifact_data == read_artifact

            artifact_data = {{
                "data_int": 12345, "data_dict": {{"test_key": "456DATA"}}
            }}
            artifact_before_write = read_artifact | artifact_data
            hardpy.set_run_artifact(artifact_data)
            report = hardpy.get_current_report()
            read_artifact = report.artifact
            assert read_artifact == artifact_before_write
    """,
    )
    result = pytester.runpytest(*hardpy_opts)
    result.assert_outcomes(passed=1)


def test_empty_run_artifact_data(pytester: Pytester, hardpy_opts: list[str]):
    pytester.makepyfile(
        f"""
        {func_test_header}
        def test_empty_run_artifact_data(request):
            report = hardpy.get_current_report()
            empty_artifact = report.artifact
            assert empty_artifact == dict(), "The test run artifact is not empty."

            artifact_data = {{}}
            hardpy.set_run_artifact(artifact_data)
            report = hardpy.get_current_report()
            read_artifact = report.artifact
            assert artifact_data == read_artifact

            artifact_data = {{}}
            artifact_before_write = read_artifact | artifact_data
            hardpy.set_run_artifact(artifact_data)
            report = hardpy.get_current_report()
            read_artifact = report.artifact
            assert read_artifact == artifact_before_write
    """,
    )
    result = pytester.runpytest(*hardpy_opts)
    result.assert_outcomes(passed=1)


def test_incorrect_run_artifact_data(pytester: Pytester, hardpy_opts: list[str]):
    pytester.makepyfile(
        f"""
        {func_test_header}
        def test_run_artifact(request):
            report = hardpy.get_current_report()
            empty_artifact = report.artifact
            assert empty_artifact == dict(), "The test run artifact is not empty."

            artifact_data = {{"ghvdfjsshkj"}}
            hardpy.set_run_artifact(artifact_data)
            report = hardpy.get_current_report()
            read_artifact = report.artifact
            assert artifact_data == read_artifact

            artifact_data = {{
                "dsjfdkshlajlk"
            }}
            artifact_before_write = read_artifact | artifact_data
            hardpy.set_run_artifact(artifact_data)
            report = hardpy.get_current_report()
            read_artifact = report.artifact
            assert read_artifact == artifact_before_write
    """,
    )
    result = pytester.runpytest(*hardpy_opts)
    result.assert_outcomes(failed=1)


def test_case_message(pytester: Pytester, hardpy_opts: list[str]):
    pytester.makepyfile(
        f"""
        {func_test_header}
        def test_message(request):
            node = NodeInfo(request.node)

            report = hardpy.get_current_report()
            empty_msg = report.modules[node.module_id].cases[node.case_id].msg
            assert empty_msg is None, "The case message is not empty."

            msg_1 = "Test message 1"
            hardpy.set_message(msg_1)
            report = hardpy.get_current_report()
            msgs = report.modules[node.module_id].cases[node.case_id].msg
            assert msg_1 in msgs.values()

            msg_2 = "Test message 2"
            hardpy.set_message(msg_2)
            report = hardpy.get_current_report()
            msgs = report.modules[node.module_id].cases[node.case_id].msg
            assert msg_1 and msg_2 in msgs.values()
            assert len(msgs.values()) == 2

            msg_3 = "Test message 3"
            key_3 = "msg_3"
            hardpy.set_message(msg_3, msg_key=key_3)
            report = hardpy.get_current_report()
            msgs = report.modules[node.module_id].cases[node.case_id].msg
            assert msg_1 and msg_2 and msg_3 in msgs.values()
            assert len(msgs.values()) == 3

            msg_4 = "Test message 4"
            hardpy.set_message(msg_4, msg_key=key_3)
            report = hardpy.get_current_report()
            msgs = report.modules[node.module_id].cases[node.case_id].msg
            assert msg_1 and msg_2 and msg_4 in msgs.values()
            assert len(msgs.values()) == 3

    """,
    )
    result = pytester.runpytest(*hardpy_opts)
    result.assert_outcomes(passed=1)


def test_empty_case_message(pytester: Pytester, hardpy_opts: list[str]):
    pytester.makepyfile(
        f"""
        {func_test_header}
        def test_message(request):
            node = NodeInfo(request.node)

            report = hardpy.get_current_report()
            empty_msg = report.modules[node.module_id].cases[node.case_id].msg
            assert empty_msg is None, "The case message is not empty."

            msg_1 = None
            hardpy.set_message(msg_1)
            report = hardpy.get_current_report()
            msgs = report.modules[node.module_id].cases[node.case_id].msg
            assert msg_1 in msgs.values()
    """,
    )
    result = pytester.runpytest(*hardpy_opts)
    result.assert_outcomes(passed=1)


def test_operator_message(pytester: Pytester, hardpy_opts: list[str]):
    pytester.makepyfile(
        f"""
        {func_test_header}
        def test_operator_message(request):
            node = NodeInfo(request.node)

            report = hardpy.get_current_report()
            with pytest.raises(AttributeError):
                report.operator_msg

            with pytest.raises(ValueError):
                hardpy.set_operator_message(msg=None)

            with pytest.raises(ValueError):
                hardpy.set_operator_message(msg="a", font_size=0)
    """,
    )
    result = pytester.runpytest(*hardpy_opts)
    result.assert_outcomes(passed=1)


def test_block_operator_message(pytester: Pytester, hardpy_opts: list[str]):
    pytester.makepyfile(
        f"""
        {func_test_header}
        @pytest.mark.timeout(2)
        def test_block_operator_message():
            hardpy.set_operator_message(msg="a")
    """,
    )
    result = pytester.runpytest(*hardpy_opts)
    result.assert_outcomes(failed=1)


def test_non_block_operator_message(pytester: Pytester, hardpy_opts: list[str]):
    pytester.makepyfile(
        f"""
        {func_test_header}
        @pytest.mark.timeout(2)
        def test_non_block_operator_message():
            hardpy.set_operator_message(msg="a", block=False)
    """,
    )
    result = pytester.runpytest(*hardpy_opts)
    result.assert_outcomes(passed=1)


def test_incorrect_couchdbconfig_data(pytester: Pytester, hardpy_opts: list[str]):
    pytester.makepyfile(
        f"""
        {func_test_header}
        def test_incorrect_couchdbconfig_data():
            config = CouchdbConfig(
                db_name="my_database",
                user="my_user",
                password="my_password",
                host="my_host",
                port=12345,
            )
            report = hardpy.get_current_report()
            assert report
    """,
    )
    result = pytester.runpytest(*hardpy_opts)
    result.assert_outcomes(failed=1)


def test_hardpy_start_arg(pytester: Pytester, hardpy_opts: list[str]):
    """Test that --hardpy-start-arg passes key=value arguments correctly."""
    pytester.makepyfile(
        f"""
        {func_test_header}
        def test_start_arg_access(request, hardpy_start_args):
            assert hardpy_start_args.get("test_mode") == "debug"
            assert hardpy_start_args.get("retry_count") == "3"
            assert hardpy_start_args.get("device_id") == "DUT-007"
            report = hardpy.get_current_report()
            assert report is not None
        """,
    )

    result = pytester.runpytest(
        *hardpy_opts,
        "--hardpy-start-arg",
        "test_mode=debug",
        "--hardpy-start-arg",
        "retry_count=3",
        "--hardpy-start-arg",
        "device_id=DUT-007",
    )
    result.assert_outcomes(passed=1)


def test_user_name(pytester: Pytester, hardpy_opts: list[str]):
    pytester.makepyfile(
        f"""
        {func_test_header}
        from hardpy import DuplicateParameterError

        def test_user_name():
            report = hardpy.get_current_report()
            assert report.user is None, "User name is not empty before start."

            name = "test_user"
            hardpy.set_user_name(name)
            report = hardpy.get_current_report()
            assert name == report.user

            second_name = "another_user"
            with pytest.raises(DuplicateParameterError):
                hardpy.set_user_name(second_name)
    """,
    )
    result = pytester.runpytest(*hardpy_opts)
    result.assert_outcomes(passed=1)


def test_batch_serial_number(pytester: Pytester, hardpy_opts: list[str]):
    pytester.makepyfile(
        f"""
        {func_test_header}
        from hardpy import DuplicateParameterError

        def test_batch_serial_number():
            report = hardpy.get_current_report()
            assert report.batch_serial_number is None, "Batch serial number is not empty before start."

            serial_number = "BATCH-123"
            hardpy.set_batch_serial_number(serial_number)
            report = hardpy.get_current_report()
            assert serial_number == report.batch_serial_number

            second_serial = "BATCH-456"
            with pytest.raises(DuplicateParameterError):
                hardpy.set_batch_serial_number(second_serial)
    """,
    )
    result = pytester.runpytest(*hardpy_opts)
    result.assert_outcomes(passed=1)


def test_dut_name(pytester: Pytester, hardpy_opts: list[str]):
    pytester.makepyfile(
        f"""
        {func_test_header}
        from hardpy import DuplicateParameterError

        def test_dut_name():
            report = hardpy.get_current_report()
            assert report.dut.name is None, "DUT name is not empty before start."

            name = "Test Device"
            hardpy.set_dut_name(name)
            report = hardpy.get_current_report()
            assert name == report.dut.name

            second_name = "Another Device"
            with pytest.raises(DuplicateParameterError):
                hardpy.set_dut_name(second_name)
    """,
    )
    result = pytester.runpytest(*hardpy_opts)
    result.assert_outcomes(passed=1)


def test_dut_type(pytester: Pytester, hardpy_opts: list[str]):
    pytester.makepyfile(
        f"""
        {func_test_header}
        from hardpy import DuplicateParameterError

        def test_dut_type():
            report = hardpy.get_current_report()
            assert report.dut.type is None, "DUT type is not empty before start."

            dut_type = "PCBA"
            hardpy.set_dut_type(dut_type)
            report = hardpy.get_current_report()
            assert dut_type == report.dut.type

            second_type = "Module"
            with pytest.raises(DuplicateParameterError):
                hardpy.set_dut_type(second_type)
    """,
    )
    result = pytester.runpytest(*hardpy_opts)
    result.assert_outcomes(passed=1)


def test_dut_revision(pytester: Pytester, hardpy_opts: list[str]):
    pytester.makepyfile(
        f"""
        {func_test_header}
        from hardpy import DuplicateParameterError

        def test_dut_revision():
            report = hardpy.get_current_report()
            assert report.dut.revision is None, "DUT revision is not empty before start."

            revision = "REV1.0"
            hardpy.set_dut_revision(revision)
            report = hardpy.get_current_report()
            assert revision == report.dut.revision

            second_rev = "REV2.0"
            with pytest.raises(DuplicateParameterError):
                hardpy.set_dut_revision(second_rev)
    """,
    )
    result = pytester.runpytest(*hardpy_opts)
    result.assert_outcomes(passed=1)


def test_stand_revision(pytester: Pytester, hardpy_opts: list[str]):
    pytester.makepyfile(
        f"""
        {func_test_header}
        from hardpy import DuplicateParameterError

        def test_stand_revision():
            report = hardpy.get_current_report()
            assert report.test_stand.revision is None, "Stand revision is not empty before start."

            revision = "HW1.0"
            hardpy.set_stand_revision(revision)
            report = hardpy.get_current_report()
            assert revision == report.test_stand.revision

            second_rev = "HW2.0"
            with pytest.raises(DuplicateParameterError):
                hardpy.set_stand_revision(second_rev)
    """,
    )
    result = pytester.runpytest(*hardpy_opts)
    result.assert_outcomes(passed=1)


def test_instruments(pytester: Pytester, hardpy_opts: list[str]):
    pytester.makepyfile(
        f"""
        {func_test_header}
        def test_instruments():
            report = hardpy.get_current_report()
            instruments = getattr(report.test_stand, 'instruments', None)
            assert instruments in (None, []), f"Expected empty instruments, got {{instruments}}"

            instrument1 = hardpy.Instrument(
                name="Power Supply",
                revision="1.0",
                serial_number="1234",
                part_number="ps_1",
                number=1,
                comment="Main power source"
            )
            hardpy.set_instrument(instrument1)

            report = hardpy.get_current_report()
            instruments = report.test_stand.instruments
            assert instruments is not None
            assert len(instruments) == 1

            first_instrument = instruments[0]
            if hasattr(first_instrument, 'name'):
                assert first_instrument.name == "Power Supply"
            else:
                assert first_instrument['name'] == "Power Supply"

            instrument2 = hardpy.Instrument(
                name="Multimeter",
                revision="2.1",
                serial_number="5678",
                part_number="mm_1",
                number=2,
                info={{'model': '34461A', 'channels': 1}}
            )
            hardpy.set_instrument(instrument2)

            report = hardpy.get_current_report()
            instruments = report.test_stand.instruments
            assert len(instruments) == 2

            second_instrument = instruments[1]
            if hasattr(second_instrument, 'name'):
                assert second_instrument.name == "Multimeter"
                assert second_instrument.info['model'] == "34461A"
            else:
                assert second_instrument['name'] == "Multimeter"
                assert second_instrument['info']['model'] == "34461A"
        """,
    )
    result = pytester.runpytest(*hardpy_opts)
    result.assert_outcomes(passed=1)


def test_process_name(pytester: Pytester, hardpy_opts: list[str]):
    pytester.makepyfile(
        f"""
        {func_test_header}
        from hardpy import DuplicateParameterError

        def test_process_name():
            report = hardpy.get_current_report()
            assert report.process.name is None, "Process name is not empty before start."

            name = "Acceptance Test"
            hardpy.set_process_name(name)
            report = hardpy.get_current_report()
            assert name == report.process.name

            second_name = "Production Test"
            with pytest.raises(DuplicateParameterError):
                hardpy.set_process_name(second_name)
    """,
    )
    result = pytester.runpytest(*hardpy_opts)
    result.assert_outcomes(passed=1)


def test_process_number(pytester: Pytester, hardpy_opts: list[str]):
    pytester.makepyfile(
        f"""
        {func_test_header}
        from hardpy import DuplicateParameterError

        def test_process_number():
            report = hardpy.get_current_report()
            assert report.process.number is None, "Process number is not empty before start."

            number = 1
            hardpy.set_process_number(number)
            report = hardpy.get_current_report()
            assert number == report.process.number

            second_number = 2
            with pytest.raises(DuplicateParameterError):
                hardpy.set_process_number(second_number)
    """,
    )
    result = pytester.runpytest(*hardpy_opts)
    result.assert_outcomes(passed=1)


def test_process_info(pytester: Pytester, hardpy_opts: list[str]):
    pytester.makepyfile(
        f"""
        {func_test_header}
        def test_process_info():
            report = hardpy.get_current_report()
            assert report.process.info == dict(), "Process info is not empty before start."

            info = {{"stage": "production", "version": "1.0"}}
            hardpy.set_process_info(info)
            report = hardpy.get_current_report()
            assert info == report.process.info

            additional_info = {{"operator": "john.doe"}}
            expected_info = info | additional_info
            hardpy.set_process_info(additional_info)
            report = hardpy.get_current_report()
            assert expected_info == report.process.info
    """,
    )
    result = pytester.runpytest(*hardpy_opts)
    result.assert_outcomes(passed=1)


def test_numeric_measurement(pytester: Pytester, hardpy_opts: list[str]):
    pytester.makepyfile(
        f"""
        {func_test_header}
        def test_measurement(request):
            node = NodeInfo(request.node)
            module_id = node.module_id
            case_id = node.case_id

            report = hardpy.get_current_report()
            measurements = report.modules[module_id].cases[case_id].measurements
            assert measurements == [], "The case measurement is not empty."

            meas1 = hardpy.NumericMeasurement(value=1)
            index_1 = hardpy.set_case_measurement(meas1)
            report = hardpy.get_current_report()
            measurements = report.modules[module_id].cases[case_id].measurements
            assert len(measurements) == 1
            assert meas1.value == measurements[index_1].value
            assert meas1.result is None

            meas2 = hardpy.NumericMeasurement(
                value=2,
                operation=hardpy.ComparisonOperation.EQ,
                comparison_value=2
            )
            index_2 = hardpy.set_case_measurement(meas2)
            report = hardpy.get_current_report()
            measurements = report.modules[module_id].cases[case_id].measurements
            assert len(measurements) == 2
            assert meas2.operation == measurements[index_2].operation
            assert meas2.comparison_value == measurements[index_2].comparison_value
            assert measurements[index_2].lower_limit is None
            assert measurements[index_2].upper_limit is None
            assert meas2.result

            meas3 = hardpy.NumericMeasurement(
                value=5,
                operation=hardpy.ComparisonOperation.GTLT,
                lower_limit=1,
                upper_limit=4
            )
            index_3 = hardpy.set_case_measurement(meas3)
            report = hardpy.get_current_report()
            measurements = report.modules[module_id].cases[case_id].measurements
            assert len(measurements) == 3
            assert meas3.operation == measurements[index_3].operation
            assert measurements[index_3].comparison_value is None
            assert meas3.lower_limit == measurements[index_3].lower_limit
            assert meas3.upper_limit == measurements[index_3].upper_limit
            assert not meas3.result
    """,
    )
    result = pytester.runpytest(*hardpy_opts)
    result.assert_outcomes(passed=1)


def test_string_measurement(pytester: Pytester, hardpy_opts: list[str]):
    pytester.makepyfile(
        f"""
        {func_test_header}
        def test_measurement(request):
            node = NodeInfo(request.node)
            module_id = node.module_id
            case_id = node.case_id

            report = hardpy.get_current_report()
            measurements = report.modules[module_id].cases[case_id].measurements
            assert measurements == [], "The case measurement is not empty."

            meas1 = hardpy.StringMeasurement(value="a")
            hardpy.set_case_measurement(meas1)
            report = hardpy.get_current_report()
            measurements = report.modules[module_id].cases[case_id].measurements
            assert len(measurements) == 1
            assert meas1.value == measurements[0].value
            assert meas1.result is None

            meas2 = hardpy.StringMeasurement(
                value="b",
                operation=hardpy.ComparisonOperation.EQ,
                comparison_value="b"
            )
            hardpy.set_case_measurement(meas2)
            report = hardpy.get_current_report()
            measurements = report.modules[module_id].cases[case_id].measurements
            assert len(measurements) == 2
            assert meas2.operation == measurements[1].operation
            assert meas2.comparison_value == measurements[1].comparison_value
            assert meas2.result

            meas3 = hardpy.StringMeasurement(
                value="A",
                operation=hardpy.ComparisonOperation.NE,
                casesensitive=False,
                comparison_value="a"
            )
            hardpy.set_case_measurement(meas3)
            report = hardpy.get_current_report()
            measurements = report.modules[module_id].cases[case_id].measurements
            assert len(measurements) == 3
            assert meas3.operation == measurements[2].operation
            assert measurements[2].comparison_value == measurements[2].comparison_value
            assert not meas3.result
    """,
    )
    result = pytester.runpytest(*hardpy_opts)
    result.assert_outcomes(passed=1)


def test_set_case_chart(pytester: Pytester, hardpy_opts: list[str]):
    pytester.makepyfile(
        f"""
        {func_test_header}
        def test_set_case_chart(request):
            node = NodeInfo(request.node)
            module_id = node.module_id
            case_id = node.case_id

            report = hardpy.get_current_report()
            chart_data = report.modules[module_id].cases[case_id].chart
            assert chart_data == None, "The chart is not empty."

            chart = hardpy.Chart(
                type=hardpy.ChartType.LINE,
                title="title",
                x_label="x_label",
                y_label="y_label",
                marker_name=["marker_name", None],
                x_data=[[1, 2], [1, 2]],
                y_data=[[3, 4], [3, 4]]
            )
            hardpy.set_case_chart(chart)
            report = hardpy.get_current_report()
            chart_data = report.modules[module_id].cases[case_id].chart
            assert chart_data.type == chart.type
            assert chart_data.title == chart.title
            assert chart_data.x_label == chart.x_label
            assert chart_data.y_label == chart.y_label
            assert chart_data.marker_name == chart.marker_name
            assert chart_data.x_data == chart.x_data
            assert chart_data.y_data == chart.y_data

            chart_2 = hardpy.Chart(
                type=hardpy.ChartType.LINE,
                title="title",
                x_label="x_label",
                y_label="y_label",
                marker_name=["marker_name", None],
                x_data=[[1, 2], [1, 2]],
                y_data=[[3, 4], [3, 4]]
            )
            with pytest.raises(hardpy.DuplicateParameterError):
                hardpy.set_case_chart(chart_2)
    """,
    )
    result = pytester.runpytest(*hardpy_opts)
    result.assert_outcomes(passed=1)


def test_get_current_attempt(pytester: Pytester, hardpy_opts: list):
    pytester.makepyfile(
        f"""{func_test_header}

        def test_a():
            assert hardpy.get_current_attempt() == 1

        @pytest.mark.attempt(2)
        def test_b():
            attempt = hardpy.get_current_attempt()
            if attempt == 2:
                return
            assert False
    """,
    )
    result = pytester.runpytest(*hardpy_opts)
    result.assert_outcomes(passed=2)
