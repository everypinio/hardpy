from pytest import Pytester


status_test_header = """
        import pytest
        """


def test_case_dependency_from_passed(pytester: Pytester, hardpy_opts):
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


def test_case_dependency_from_incorrect_1(pytester: Pytester, hardpy_opts):
    pytester.makepyfile(
        test_1="""
        import pytest

        @pytest.mark.case_dependency("kuhfkhgf::qwqw")
        def test_one():
            assert True
    """
    )
    result = pytester.runpytest(*hardpy_opts)
    result.assert_outcomes()


def test_case_dependency_from_incorrect_2(pytester: Pytester, hardpy_opts):
    pytester.makepyfile(
        test_1="""
        import pytest

        @pytest.mark.case_dependency("kuhfkhgf")
        def test_one():
            assert True
    """
    )
    result = pytester.runpytest(*hardpy_opts)
    result.assert_outcomes()


def test_case_dependency_from_incorrect_3(pytester: Pytester, hardpy_opts):
    pytester.makepyfile(
        test_1="""
        import pytest

        @pytest.mark.case_dependency(":::")
        def test_one():
            assert True
    """
    )
    result = pytester.runpytest(*hardpy_opts)
    result.assert_outcomes()


def test_case_dependency_from_failed(pytester: Pytester, hardpy_opts):
    pytester.makepyfile(
        test_1="""
        import pytest

        def test_one():
            assert False

        @pytest.mark.case_dependency("test_1::test_one")
        def test_two():
            assert False
    """
    )
    result = pytester.runpytest(*hardpy_opts)
    result.assert_outcomes(failed=1, skipped=1)


def test_case_dependency_from_skipped(pytester: Pytester, hardpy_opts):
    pytester.makepyfile(
        test_1="""
        import pytest

        def test_one():
            assert False

        @pytest.mark.case_dependency("test_1::test_one")
        def test_two():
            assert False

        @pytest.mark.case_dependency("test_1::test_two")
        def test_three():
            assert True
    """
    )
    result = pytester.runpytest(*hardpy_opts)
    result.assert_outcomes(failed=1, skipped=2)


def test_case_dependency_from_not_skipped(pytester: Pytester, hardpy_opts):
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


def test_module_dependency_from_passed(pytester: Pytester, hardpy_opts):
    pytester.makepyfile(
        test_1="""
        import pytest

        def test_one():
            assert True
    """
    )
    pytester.makepyfile(
        test_2="""
        import pytest

        pytestmark = pytest.mark.module_dependency("test_1::test_one")

        def test_one():
            assert True
    """
    )
    result = pytester.runpytest(*hardpy_opts)
    result.assert_outcomes(passed=2)


def test_module_dependency_from_incorrect_1(pytester: Pytester, hardpy_opts):
    pytester.makepyfile(
        test_2="""
        import pytest

        pytestmark = pytest.mark.module_dependency("kuhfkhgf::fghdjshfj")

        def test_one():
            assert True
    """
    )
    result = pytester.runpytest(*hardpy_opts)
    result.assert_outcomes()


def test_module_dependency_from_incorrect_2(pytester: Pytester, hardpy_opts):
    pytester.makepyfile(
        test_2="""
        import pytest

        pytestmark = pytest.mark.module_dependency("kuhfkhgf")

        def test_one():
            assert True
    """
    )
    result = pytester.runpytest(*hardpy_opts)
    result.assert_outcomes()


def test_module_dependency_from_incorrect_3(pytester: Pytester, hardpy_opts):
    pytester.makepyfile(
        test_1="""
        import pytest

        def test_one():
            assert True
    """
    )
    pytester.makepyfile(
        test_2="""
        import pytest

        pytestmark = pytest.mark.module_dependency("test_1::fghdjshfj")

        def test_one():
            assert True
    """
    )
    result = pytester.runpytest(*hardpy_opts)
    result.assert_outcomes()


def test_module_dependency_from_incorrect_4(pytester: Pytester, hardpy_opts):
    pytester.makepyfile(
        test_1="""
        import pytest

        def test_one():
            assert True
    """
    )
    pytester.makepyfile(
        test_2="""
        import pytest

        pytestmark = pytest.mark.module_dependency(":::")

        def test_one():
            assert True
    """
    )
    result = pytester.runpytest(*hardpy_opts)
    result.assert_outcomes()


def test_module_dependency_from_incorrect_5(pytester: Pytester, hardpy_opts):
    pytester.makepyfile(
        test_1="""
        import pytest

        def test_one():
            assert True
    """
    )
    pytester.makepyfile(
        test_2="""
        import pytest

        pytestmark = pytest.mark.module_dependency("asfddaa::test_one")

        def test_one():
            assert True
    """
    )
    result = pytester.runpytest(*hardpy_opts)
    result.assert_outcomes()


def test_case_dependency_from_module(pytester: Pytester, hardpy_opts):
    pytester.makepyfile(
        test_1="""
        import pytest

        def test_one():
            assert False
    """
    )
    pytester.makepyfile(
        test_2="""
        import pytest

        pytestmark = pytest.mark.module_dependency("test_1")

        def test_one():
            assert True
    """
    )
    result = pytester.runpytest(*hardpy_opts)
    result.assert_outcomes(failed=1, skipped=1)


def test_case_dependency_from_big_module(pytester: Pytester, hardpy_opts):
    pytester.makepyfile(
        test_1="""
        import pytest

        def test_one():
            assert False

        def test_two():
            assert True

        def test_three():
            assert True
    """
    )
    pytester.makepyfile(
        test_2="""
        import pytest

        pytestmark = pytest.mark.module_dependency("test_1")

        def test_one():
            assert True

        def test_two():
            assert True

        def test_three():
            assert True
    """
    )
    result = pytester.runpytest(*hardpy_opts)
    result.assert_outcomes(passed=2, failed=1, skipped=3)


def test_module_dependency_from_failed(pytester: Pytester, hardpy_opts):
    pytester.makepyfile(
        test_1="""
        import pytest

        def test_one():
            assert False
    """
    )
    pytester.makepyfile(
        test_2="""
        import pytest

        pytestmark = pytest.mark.module_dependency("test_1::test_one")

        def test_one():
            assert True
    """
    )
    result = pytester.runpytest(*hardpy_opts)
    result.assert_outcomes(failed=1, skipped=1)


def test_module_dependency_from_skipped(pytester: Pytester, hardpy_opts):
    pytester.makepyfile(
        test_1="""
        import pytest

        def test_one():
            assert False
    """
    )
    pytester.makepyfile(
        test_2="""
        import pytest

        pytestmark = pytest.mark.module_dependency("test_1::test_one")

        def test_one():
            assert True
    """
    )
    pytester.makepyfile(
        test_3="""
        import pytest

        pytestmark = pytest.mark.module_dependency("test_2::test_one")

        def test_one():
            assert True
    """
    )
    result = pytester.runpytest(*hardpy_opts)
    result.assert_outcomes(failed=1, skipped=2)


def test_module_dependency_from_not_skipped(pytester: Pytester, hardpy_opts):
    pytester.makepyfile(
        test_1="""
        import pytest

        def test_one():
            assert True
    """
    )
    pytester.makepyfile(
        test_2="""
        import pytest

        pytestmark = pytest.mark.module_dependency("test_1::test_one")

        def test_one():
            assert True
    """
    )
    pytester.makepyfile(
        test_3="""
        import pytest

        pytestmark = pytest.mark.module_dependency("test_2::test_one")

        def test_one():
            assert True
    """
    )
    result = pytester.runpytest(*hardpy_opts)
    result.assert_outcomes(passed=3)


def test_module_dependency(pytester: Pytester, hardpy_opts):
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
