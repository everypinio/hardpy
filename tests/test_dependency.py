from pytest import Pytester


status_test_header = """
        import pytest

        from hardpy import get_current_report
        from hardpy.pytest_hardpy.utils.const import TestStatus as Status
        from hardpy.pytest_hardpy.utils import NodeInfo
        """


def test_dependency(pytester: Pytester, hardpy_opts):
    pytester.makepyfile(
        f"""
        {status_test_header}
        def test_one():
            assert True

        @pytest.dependency("test_one")
        def test_two(request):
            assert True

        def test_three():
            # Тест 3 - отрицательный
            assert False

        def test_four(request):
            # Тест 4 зависит от теста 3
            pytest.dependency("test_three")
            assert True

        def test_five(request):
            # Тест 5 зависит от теста 4
            pytest.dependency("test_four")
            assert True
    """
    )
    result = pytester.runpytest(*hardpy_opts)
    result.assert_outcomes(passed=3)
