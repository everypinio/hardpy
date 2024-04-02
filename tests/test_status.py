from pytest import Pytester


status_test_header = """
        import pytest

        from hardpy import get_current_report
        from hardpy.pytest_hardpy.utils.const import TestStatus as Status
        from hardpy.pytest_hardpy.utils import NodeInfo
        """



def test_ready_status(pytester: Pytester, hardpy_opts):
    pytester.makepyfile(
        f"""
        {status_test_header}
        def test_status_ready(request):
            node = NodeInfo(request.node)
            report = get_current_report()
            status = report.modules[node.module_id].cases['test_status_run'].status
            assert Status.READY == status

        def test_status_run(request):
            node = NodeInfo(request.node)
            report = get_current_report()
            read_status = report.modules[node.module_id].cases[node.case_id].status
            assert Status.RUN == read_status

        def test_status_passed(request):
            node = NodeInfo(request.node)
            report = get_current_report()
            read_status = report.modules[node.module_id].cases['test_status_run'].status
            assert Status.PASSED == read_status
    """
    )
    result = pytester.runpytest(*hardpy_opts)
    result.assert_outcomes(passed=3)


def test_fail_status(pytester: Pytester, hardpy_opts):
    pytester.makepyfile(
        f"""
        {status_test_header}
        def test_fail():
            assert False

        def test_status_fail(request):
            node = NodeInfo(request.node)
            report = get_current_report()
            read_status = report.modules[node.module_id].cases['test_fail'].status
            assert Status.FAILED == read_status
            assert True
    """
    )
    result = pytester.runpytest(*hardpy_opts)
    result.assert_outcomes(failed=1, passed=1)


def test_run_status(pytester: Pytester, hardpy_opts):
    pytester.makepyfile(
        f"""
        {status_test_header}
        def test_check_run_status(request):
            report = get_current_report()
            read_status = report.status
            assert Status.RUN == read_status
    """
    )
    result = pytester.runpytest(*hardpy_opts)
    result.assert_outcomes(passed=1)
