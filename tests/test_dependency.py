from pytest import Pytester


status_test_header = """
        import pytest
        """


def test_case_dependency_from_passed(pytester: Pytester, hardpy_opts):
    # test_1.py
    pytester.makepyfile(
        test_1="""
        import pytest

        def test_one():
            assert True

        @pytest.mark.case_dependency("test_1::test_one")
        def test_two():
            assert True
    """
    )
    result = pytester.runpytest(*hardpy_opts)
    result.assert_outcomes(passed=2)


def test_case_incorrect_dependency(pytester: Pytester, hardpy_opts):
    # test_1.py
    pytester.makepyfile(
        test_1="""
        import pytest

        def test_one():
            assert True

        @pytest.mark.case_dependency("test_11::test_one")
        def test_two():
            assert True
    """
    )
    result = pytester.runpytest(*hardpy_opts)
    result.assert_outcomes(passed=2)


def test_case_dependency_from_failed(pytester: Pytester, hardpy_opts):
    # test_1.py
    pytester.makepyfile(
        test_1="""
        import pytest

        def test_three():
            assert False

        @pytest.mark.case_dependency("test_1::test_three")
        def test_four():
            assert False
    """
    )
    result = pytester.runpytest(*hardpy_opts)
    result.assert_outcomes(failed=1, skipped=1)


def test_case_dependency_from_skipped(pytester: Pytester, hardpy_opts):
    # test_1.py
    pytester.makepyfile(
        test_1="""
        import pytest

        def test_three():
            assert False

        @pytest.mark.case_dependency("test_1::test_three")
        def test_four():
            assert False

        @pytest.mark.case_dependency("test_1::test_four")
        def test_five():
            assert True 
    """
    )
    result = pytester.runpytest(*hardpy_opts)
    result.assert_outcomes(failed=1, skipped=2)


def test_case_dependency_from_not_skipped(pytester: Pytester, hardpy_opts):
    # test_1.py
    pytester.makepyfile(
        test_1="""
        import pytest

        def test_one():
            assert True

        @pytest.mark.case_dependency("test_1::test_one")
        def test_two():
            assert True

        @pytest.mark.case_dependency("test_1::test_two")
        def test_five():
            assert True 
    """
    )
    result = pytester.runpytest(*hardpy_opts)
    result.assert_outcomes(passed=3)


def test_case_dependency(pytester: Pytester, hardpy_opts):
    # test_1.py
    pytester.makepyfile(
        test_1="""
        import pytest

        def test_one():
            assert True

        @pytest.mark.case_dependency("test_1::test_one")
        def test_two():
            assert True

        def test_three():
            assert False

        @pytest.mark.case_dependency("test_1::test_three")
        def test_four():
            assert False

        @pytest.mark.case_dependency("test_1::test_four")
        def test_five():
            assert True 
    """
    )
    result = pytester.runpytest(*hardpy_opts)
    result.assert_outcomes(passed=2, failed=1, skipped=2)


def test_module_dependency(pytester: Pytester, hardpy_opts):
    # test_1.py
    pytester.makepyfile(
        test_1="""
        import pytest

        def test_one():
            assert True

        @pytest.mark.case_dependency("test_1::test_one")
        def test_two():
            assert True

        def test_three():
            assert False

        @pytest.mark.case_dependency("test_1::test_three")
        def test_four():
            assert False

        @pytest.mark.case_dependency("test_1::test_four")
        def test_five():
            assert True 
    """
    )
    pytester.makepyfile(
        test_2="""
        import pytest

        pytestmark = pytest.mark.module_dependency("test_1::test_one")

        def test_one():
            assert True

        def test_two():
            assert True

        def test_three():
            assert True
    """
    )
    pytester.makepyfile(
        test_3="""
        import pytest

        pytestmark = pytest.mark.module_dependency("test_1::test_three")

        def test_one():
            assert True

        def test_two():
            assert True

        def test_three():
            assert True
    """
    )
    pytester.makepyfile(
        test_4="""
        import pytest

        pytestmark = pytest.mark.module_dependency("test_1::test_five")

        def test_one():
            assert True

        def test_two():
            assert True

        def test_three():
            assert True
    """
    )
    result = pytester.runpytest(*hardpy_opts)
    result.assert_outcomes(passed=5, failed=1, skipped=8)
