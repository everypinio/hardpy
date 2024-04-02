from pytest import Pytester

mark_test_header = """
        import pytest

        from hardpy import get_current_report
        from hardpy.pytest_hardpy.utils import NodeInfo

        module_name = "Markers"
        case_name = "Case name"
        pytestmark = pytest.mark.module_name(module_name)
        """

test_default_header = """
        import pytest

        from hardpy import get_current_report
        from hardpy.pytest_hardpy.utils import NodeInfo
        """


def test_module_name(pytester: Pytester, hardpy_opts):
    pytester.makepyfile(
        f"""
        {mark_test_header}
        @pytest.mark.case_name("Module name")
        def test_written_module_name(request):
            node = NodeInfo(request.node)
            report = get_current_report()
            read_module_name = report.modules[node.module_id].name
            assert module_name == read_module_name
    """
    )
    result = pytester.runpytest(*hardpy_opts)
    result.assert_outcomes(passed=1)


def test_case_name(pytester: Pytester, hardpy_opts):
    pytester.makepyfile(
        f"""
        {mark_test_header}
        @pytest.mark.case_name(case_name)
        def test_written_test_name(request):
            node = NodeInfo(request.node)
            report = get_current_report()
            name = report.modules[node.module_id].cases[node.case_id].name
            assert case_name == name
    """
    )
    result = pytester.runpytest(*hardpy_opts)
    result.assert_outcomes(passed=1)


def test_default_case_name(pytester: Pytester, hardpy_opts):
    pytester.makepyfile(
        f"""
        {test_default_header}
        def test_check_default_case_name(request):
            node = NodeInfo(request.node)
            report = get_current_report()
            name = report.modules[node.module_id].cases[node.case_id].name
            assert name == "test_check_default_case_name"
    """
    )
    result = pytester.runpytest(*hardpy_opts)
    result.assert_outcomes(passed=1)



def test_default_module_name(pytester: Pytester, hardpy_opts):
    pytester.makepyfile(
        f"""
        {test_default_header}
        def test_check_default_module_name(request):
            node = NodeInfo(request.node)
            report = get_current_report()
            read_module_name = report.modules[node.module_id].name
            assert read_module_name == "test_default_module_name"
    """
    )
    result = pytester.runpytest(*hardpy_opts)
    result.assert_outcomes(passed=1)
