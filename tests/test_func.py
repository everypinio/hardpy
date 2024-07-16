from pytest import Pytester


func_test_header = """
        from uuid import uuid4

        import pytest

        import hardpy
        from hardpy.pytest_hardpy.utils import NodeInfo
        """


def test_dut_serial_number(pytester: Pytester, hardpy_opts):
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
    """
    )

    result = pytester.runpytest(*hardpy_opts)
    result.assert_outcomes(passed=1)


def test_dut_info(pytester: Pytester, hardpy_opts):
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
    """
    )
    result = pytester.runpytest(*hardpy_opts)
    result.assert_outcomes(passed=1)


def test_stand_info(pytester: Pytester, hardpy_opts):
    pytester.makepyfile(
        f"""
        {func_test_header}
        def test_stand_info():
            report = hardpy.get_current_report()
            assert report.test_stand == dict(), "The test stand info is not empty."

            info = {{"name": "Test stand 1"}}
            hardpy.set_stand_info(info)
            report = hardpy.get_current_report()
            assert info == report.test_stand

            info = {{"driver_1": "driver A"}}
            stand_info_before_write = report.test_stand | info
            hardpy.set_stand_info(info)
            report = hardpy.get_current_report()
            assert stand_info_before_write == report.test_stand
    """
    )
    result = pytester.runpytest(*hardpy_opts)
    result.assert_outcomes(passed=1)


def test_drivers(pytester: Pytester, hardpy_opts):
    pytester.makepyfile(
        f"""
        {func_test_header}
        def test_drivers():
            report = hardpy.get_current_report()
            assert report.drivers == dict(), "The drivers data is not empty."

            drivers = {{"driver_1": "driver info"}}
            hardpy.set_driver_info(drivers)
            report = hardpy.get_current_report()
            assert drivers == report.drivers

            drivers = {{
                "driver_2": {{
                    "state": "active",
                    "port": 8000,
                }}
            }}
            drivers_before_write = report.drivers | drivers
            hardpy.set_driver_info(drivers)
            report = hardpy.get_current_report()
            assert drivers_before_write == report.drivers
    """
    )
    result = pytester.runpytest(*hardpy_opts)
    result.assert_outcomes(passed=1)


def test_module_artifact(pytester: Pytester, hardpy_opts):
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
    """
    )
    result = pytester.runpytest(*hardpy_opts)
    result.assert_outcomes(passed=1)


def test_case_artifact(pytester: Pytester, hardpy_opts):
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
    """
    )
    result = pytester.runpytest(*hardpy_opts)
    result.assert_outcomes(passed=1)


def test_run_artifact(pytester: Pytester, hardpy_opts):
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
    """
    )
    result = pytester.runpytest(*hardpy_opts)
    result.assert_outcomes(passed=1)


def test_case_message(pytester: Pytester, hardpy_opts):
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

    """
    )
    result = pytester.runpytest(*hardpy_opts)
    result.assert_outcomes(passed=1)
