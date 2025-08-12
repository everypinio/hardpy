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
        from hardpy import DuplicateSerialNumberError

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
            with pytest.raises(DuplicateSerialNumberError):
                hardpy.set_dut_serial_number(second_serial_number)
    """,
    )

    result = pytester.runpytest(*hardpy_opts)
    result.assert_outcomes(passed=1)


def test_dut_part_number(pytester: Pytester, hardpy_opts: list[str]):
    pytester.makepyfile(
        f"""
        {func_test_header}
        from hardpy import DuplicatePartNumberError

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
            with pytest.raises(DuplicatePartNumberError):
                hardpy.set_dut_part_number(second_part_number)
    """,
    )

    result = pytester.runpytest(*hardpy_opts)
    result.assert_outcomes(passed=1)


def test_empty_dut_serial_number(pytester: Pytester, hardpy_opts: list[str]):
    pytester.makepyfile(
        f"""
        {func_test_header}
        from hardpy import DuplicateSerialNumberError

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
        from hardpy import DuplicateSerialNumberError

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


def test_stand_name(pytester: Pytester, hardpy_opts: list[str]):
    pytester.makepyfile(
        f"""
        {func_test_header}
        from hardpy import DuplicateTestStandNameError

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
            with pytest.raises(DuplicateTestStandNameError):
                hardpy.set_stand_name(second_name)
    """,
    )
    result = pytester.runpytest(*hardpy_opts)
    result.assert_outcomes(passed=1)


def test_stand_location(pytester: Pytester, hardpy_opts: list[str]):
    pytester.makepyfile(
        f"""
        {func_test_header}
        from hardpy import DuplicateTestStandLocationError

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
            with pytest.raises(DuplicateTestStandLocationError):
                hardpy.set_stand_location(second_location)
    """,
    )
    result = pytester.runpytest(*hardpy_opts)
    result.assert_outcomes(passed=1)


def test_stand_duplicate_number(pytester: Pytester, hardpy_opts: list[str]):
    pytester.makepyfile(
        f"""
        {func_test_header}
        from hardpy import DuplicateTestStandNumberError

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
            with pytest.raises(DuplicateTestStandNumberError):
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


def test_incorrect_configdata(pytester: Pytester, hardpy_opts: list[str]):
    pytester.makepyfile(
        f"""
        {func_test_header}
        def test_incorrect_configdata():
            config = ConfigData(
                db_host="test-db",
                db_user="test-user",
                db_pswd="test-password",
                db_port=1234,
                web_host="test-host",
                web_port=5678,
                tests_dir="/path/to/tests",
            )
            report = hardpy.get_current_report()
            assert report
    """,
    )
    result = pytester.runpytest(*hardpy_opts)
    result.assert_outcomes(failed=1)


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


def test_hardpy_start_param(pytester: Pytester, hardpy_opts: list[str]):
    """Test that --hardpy-start-param passes key=value parameters correctly."""
    pytester.makepyfile(
        f"""
        {func_test_header}
        def test_start_param_access(request):
            start_params = request.config.getoption("--hardpy-start-param") or []
            params_dict = {{}}
            for param in start_params:
                if "=" in param:
                    k, v = param.split("=", 1)
                    params_dict[k] = v
            assert "test_mode" in params_dict
            assert params_dict["test_mode"] == "debug"
            assert "retry_count" in params_dict
            assert params_dict["retry_count"] == "3"
            assert "device_id" in params_dict
            assert params_dict["device_id"] == "DUT-007"
            report = hardpy.get_current_report()
            assert report is not None
        """,
    )

    result = pytester.runpytest(
        *hardpy_opts,
        "--hardpy-start-param", "test_mode=debug",
        "--hardpy-start-param", "retry_count=3",
        "--hardpy-start-param", "device_id=DUT-007",
    )

    result.assert_outcomes(passed=1)
