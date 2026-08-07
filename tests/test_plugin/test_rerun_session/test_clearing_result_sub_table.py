from pytest import Pytester


def test_clearing_test_stand(
    pytester: Pytester,
    jig_opts: list[str],
    jig_opts_repeat: list[str],
):
    pytester.makepyfile(
        """
        import pytest
        import jig

        def test_passed():
            report = jig.get_current_report()
            test_stand = report.test_stand
            assert test_stand.hw_id is not None, "HW id must be set by default."
            assert test_stand.timezone is not None, "Timezone must be set by default."
            assert test_stand.location is None, "Location is empty by default."
            assert test_stand.name is None, "Name is empty by default."
            assert test_stand.revision is None, "Revision is empty by default."
            assert test_stand.number is None, "Number is empty by default."
            assert test_stand.instruments == [], "Instruments is empty by default."
            assert test_stand.info == {}, "Info is empty by default."

            jig.set_stand_name("stand_1")
            jig.set_stand_info({"calibration_date": "2023-01-15"})
            jig.set_stand_location("Moon")
            jig.set_stand_number(3)
            jig.set_stand_revision("HW1.0")
            instrument = jig.Instrument(
                    name="Oscilloscope",
                    revision="1.2",
                    serial_number="4235098",
                    part_number="E012",
                    number=1,
                    info={"model": "DSO-X 2024A", "bandwidth": "200MHz"}
                )
            jig.set_instrument(instrument)
    """,
    )
    result = pytester.runpytest(*jig_opts)
    result.assert_outcomes(passed=1)

    result = pytester.runpytest(*jig_opts_repeat)
    result.assert_outcomes(passed=1)


def test_clearing_dut(
    pytester: Pytester,
    jig_opts: list[str],
    jig_opts_repeat: list[str],
):
    pytester.makepyfile(
        """
        import pytest
        import jig

        def test_passed():
            report = jig.get_current_report()
            dut = report.dut
            assert dut.name is None, "Name is empty by default."
            assert dut.type is None, "Type is empty by default."
            assert dut.serial_number is None, "Serial number is empty by default."
            assert dut.part_number is None, "Part number is empty by default."
            assert dut.revision is None, "Revision is empty by default."
            assert dut.sub_units == [], "Sub units is empty by default."
            assert dut.info == {}, "Info is empty by default."

            jig.set_dut_name("DUT_1")
            jig.set_dut_type("PCBA")
            jig.set_dut_serial_number("1234")
            jig.set_dut_part_number("part_1")
            jig.set_dut_revision("HW1.0")
            sub_unit = jig.SubUnit(
                serial_number="12345",
                part_number="part_number_1",
                name="Test Device",
                type="PCBA",
                revision="REV1.0",
                info={"sw_version": "1.0"},
            )
            jig.set_dut_sub_unit(sub_unit)
            jig.set_dut_info({"sw_version": "1.0.0"})
    """,
    )
    result = pytester.runpytest(*jig_opts)
    result.assert_outcomes(passed=1)

    result = pytester.runpytest(*jig_opts_repeat)
    result.assert_outcomes(passed=1)


def test_clearing_process(
    pytester: Pytester,
    jig_opts: list[str],
    jig_opts_repeat: list[str],
):
    pytester.makepyfile(
        """
        import pytest
        import jig

        def test_passed():
            report = jig.get_current_report()
            process = report.process
            assert process.name is None, "Name is empty by default."
            assert process.number is None, "Number is empty by default."
            assert process.info == {}, "Info is empty by default."

            jig.set_process_name("Acceptance Test")
            jig.set_process_number(1)
            jig.set_process_info({"stage": "production"})
    """,
    )
    result = pytester.runpytest(*jig_opts)
    result.assert_outcomes(passed=1)

    result = pytester.runpytest(*jig_opts_repeat)
    result.assert_outcomes(passed=1)


def test_clearing_modules(
    pytester: Pytester,
    jig_opts: list[str],
    jig_opts_repeat: list[str],
):
    pytester.makepyfile(
        """
        import pytest
        import jig

        def test_passed():
            report = jig.get_current_report()
            modules = report.modules
            module_name = "test_clearing_modules"
            assert modules[module_name].artifact == {}, "Artifact is empty by default."

            jig.set_module_artifact({"some_artifact": "1"})
    """,
    )
    result = pytester.runpytest(*jig_opts)
    result.assert_outcomes(passed=1)

    result = pytester.runpytest(*jig_opts_repeat)
    result.assert_outcomes(passed=1)
