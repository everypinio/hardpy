import pytest
from pydantic import ValidationError

from hardpy import ComparisonOperation as CompOp, StringMeasurement


def test_only_value():
    meas = StringMeasurement(value="a")
    assert meas.value == "a"
    assert meas.result is None


def test_empty_measurement():
    with pytest.raises(ValidationError):
        StringMeasurement()


# measurement logic test
# fmt: off

def test_eq():
    v1 = "a"
    v2 = "b"
    v3 = "A"

    assert StringMeasurement(value=v1, operation=CompOp.EQ, comparison_value=v1).result
    assert not StringMeasurement(value=v1, operation=CompOp.EQ, comparison_value=v2).result
    assert not StringMeasurement(value=v1, operation=CompOp.EQ, comparison_value=v3).result
    assert StringMeasurement(value=v1, operation=CompOp.EQ, casesensitive=False, comparison_value=v3).result

def test_ne():
    v1 = "a"
    v2 = "b"
    v3 = "A"

    assert not StringMeasurement(value=v1, operation=CompOp.NE, comparison_value=v1).result
    assert StringMeasurement(value=v1, operation=CompOp.NE, comparison_value=v2).result
    assert StringMeasurement(value=v1, operation=CompOp.NE, comparison_value=v3).result
    assert not StringMeasurement(value=v1, operation=CompOp.NE, casesensitive=False, comparison_value=v3).result

def test_other_operations():
    string_operators = {CompOp.EQ, CompOp.NE}
    excess_operators = [member.value for member in CompOp if member not in string_operators]

    for _operator in excess_operators:
        with pytest.raises(ValidationError):
            StringMeasurement(value="a", operation=_operator, comparison_value="b")

# validation tests
def test_eq_validator():
    with pytest.raises(ValidationError):
        StringMeasurement(value="a", operation=CompOp.EQ)


def test_ne_validator():
    with pytest.raises(ValidationError):
        StringMeasurement(value="a", operation=CompOp.NE)
