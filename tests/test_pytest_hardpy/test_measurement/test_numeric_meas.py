import pytest
from pydantic import ValidationError

from hardpy import ComparisonOperation as CompOp, NumericMeasurement


def test_only_value():
    meas = NumericMeasurement(value=5)
    assert meas.value == 5
    assert meas.result is None


def test_empty_measurement():
    with pytest.raises(ValidationError):
        NumericMeasurement()


# measurement logic test
# fmt: off

def test_eq():
    v1 = 1
    v2 = 2

    assert NumericMeasurement(value=v1, operation=CompOp.EQ, comparison_value=v1).result
    assert not NumericMeasurement(value=v1, operation=CompOp.EQ, comparison_value=v2).result

def test_ne():
    v1 = 1
    v2 = 2

    assert NumericMeasurement(value=v1, operation=CompOp.NE, comparison_value=v2).result
    assert not NumericMeasurement(value=v1, operation=CompOp.NE, comparison_value=v1).result

def test_gt():
    v1 = 1
    v2 = 2

    assert NumericMeasurement(value=v2, operation=CompOp.GT, comparison_value=v1).result
    assert not NumericMeasurement(value=v1, operation=CompOp.GT, comparison_value=v1).result
    assert not NumericMeasurement(value=v1, operation=CompOp.GT, comparison_value=v2).result

def test_ge():
    v1 = 1
    v2 = 2

    assert NumericMeasurement(value=v1, operation=CompOp.GE, comparison_value=v1).result
    assert NumericMeasurement(value=v2, operation=CompOp.GE, comparison_value=v1)
    assert not NumericMeasurement(value=v1, operation=CompOp.GE, comparison_value=v2).result

def test_lt():
    v1 = 1
    v2 = 2

    assert NumericMeasurement(value=v1, operation=CompOp.LT, comparison_value=v2).result
    assert not NumericMeasurement(value=v1, operation=CompOp.LT, comparison_value=v1).result
    assert not NumericMeasurement(value=v2, operation=CompOp.LT, comparison_value=v1).result

def test_le():
    v1 = 1
    v2 = 2

    assert NumericMeasurement(value=v1, operation=CompOp.LE, comparison_value=v1).result
    assert NumericMeasurement(value=v1, operation=CompOp.LE, comparison_value=v2)
    assert not NumericMeasurement(value=v2, operation=CompOp.LE, comparison_value=v1).result

def test_gtlt():
    v1 = 1
    v2 = 2
    v3 = 3

    assert NumericMeasurement(value=v2, operation=CompOp.GTLT, lower_limit=v1, upper_limit=v3).result
    assert not NumericMeasurement(value=v2, operation=CompOp.GTLT, lower_limit=v2, upper_limit=v3).result
    assert not NumericMeasurement(value=v2, operation=CompOp.GTLT, lower_limit=v1, upper_limit=v2).result
    assert not NumericMeasurement(value=v3, operation=CompOp.GTLT, lower_limit=v1, upper_limit=v2).result
    assert not NumericMeasurement(value=v1, operation=CompOp.GTLT, lower_limit=v2, upper_limit=v3).result

def test_gele():
    v1 = 1
    v2 = 2
    v3 = 3

    assert NumericMeasurement(value=v2, operation=CompOp.GELE, lower_limit=v1, upper_limit=v3).result
    assert NumericMeasurement(value=v2, operation=CompOp.GELE, lower_limit=v2, upper_limit=v3).result
    assert NumericMeasurement(value=v2, operation=CompOp.GELE, lower_limit=v1, upper_limit=v2).result
    assert not NumericMeasurement(value=v3, operation=CompOp.GELE, lower_limit=v1, upper_limit=v2).result
    assert not NumericMeasurement(value=v1, operation=CompOp.GELE, lower_limit=v2, upper_limit=v3).result

def test_gelt():
    v1 = 1
    v2 = 2
    v3 = 3

    assert NumericMeasurement(value=v2, operation=CompOp.GELT, lower_limit=v1, upper_limit=v3).result
    assert NumericMeasurement(value=v2, operation=CompOp.GELT, lower_limit=v2, upper_limit=v3).result
    assert not NumericMeasurement(value=v2, operation=CompOp.GELT, lower_limit=v1, upper_limit=v2).result
    assert not NumericMeasurement(value=v3, operation=CompOp.GELT, lower_limit=v1, upper_limit=v2).result
    assert not NumericMeasurement(value=v1, operation=CompOp.GELT, lower_limit=v2, upper_limit=v3).result

def test_gtle():
    v1 = 1
    v2 = 2
    v3 = 3

    assert NumericMeasurement(value=v2, operation=CompOp.GTLE, lower_limit=v1, upper_limit=v3).result
    assert not NumericMeasurement(value=v2, operation=CompOp.GTLE, lower_limit=v2, upper_limit=v3).result
    assert NumericMeasurement(value=v2, operation=CompOp.GTLE, lower_limit=v1, upper_limit=v2).result
    assert not NumericMeasurement(value=v3, operation=CompOp.GTLE, lower_limit=v1, upper_limit=v2).result
    assert not NumericMeasurement(value=v1, operation=CompOp.GTLE, lower_limit=v2, upper_limit=v3).result

def test_ltgt():
    v1 = 1
    v2 = 2
    v3 = 3

    assert not NumericMeasurement(value=v2, operation=CompOp.LTGT, lower_limit=v1, upper_limit=v3).result
    assert not NumericMeasurement(value=v2, operation=CompOp.LTGT, lower_limit=v2, upper_limit=v3).result
    assert not NumericMeasurement(value=v2, operation=CompOp.LTGT, lower_limit=v1, upper_limit=v2).result
    assert NumericMeasurement(value=v3, operation=CompOp.LTGT, lower_limit=v1, upper_limit=v2).result
    assert NumericMeasurement(value=v1, operation=CompOp.LTGT, lower_limit=v2, upper_limit=v3).result

def test_lege():
    v1 = 1
    v2 = 2
    v3 = 3

    assert not NumericMeasurement(value=v2, operation=CompOp.LEGE, lower_limit=v1, upper_limit=v3).result
    assert NumericMeasurement(value=v2, operation=CompOp.LEGE, lower_limit=v2, upper_limit=v3).result
    assert NumericMeasurement(value=v2, operation=CompOp.LEGE, lower_limit=v1, upper_limit=v2).result
    assert NumericMeasurement(value=v3, operation=CompOp.LEGE, lower_limit=v1, upper_limit=v2).result
    assert NumericMeasurement(value=v1, operation=CompOp.LEGE, lower_limit=v2, upper_limit=v3).result

def test_legt():
    v1 = 1
    v2 = 2
    v3 = 3

    assert not NumericMeasurement(value=v2, operation=CompOp.LEGT, lower_limit=v1, upper_limit=v3).result
    assert NumericMeasurement(value=v2, operation=CompOp.LEGT, lower_limit=v2, upper_limit=v3).result
    assert not NumericMeasurement(value=v2, operation=CompOp.LEGT, lower_limit=v1, upper_limit=v2).result
    assert NumericMeasurement(value=v3, operation=CompOp.LEGT, lower_limit=v1, upper_limit=v2).result
    assert NumericMeasurement(value=v1, operation=CompOp.LEGT, lower_limit=v2, upper_limit=v3).result

def test_ltge():
    v1 = 1
    v2 = 2
    v3 = 3

    assert not NumericMeasurement(value=v2, operation=CompOp.LTGE, lower_limit=v1, upper_limit=v3).result
    assert not NumericMeasurement(value=v2, operation=CompOp.LTGE, lower_limit=v2, upper_limit=v3).result
    assert NumericMeasurement(value=v2, operation=CompOp.LTGE, lower_limit=v1, upper_limit=v2).result
    assert NumericMeasurement(value=v3, operation=CompOp.LTGE, lower_limit=v1, upper_limit=v2).result
    assert NumericMeasurement(value=v1, operation=CompOp.LTGE, lower_limit=v2, upper_limit=v3).result

# fmt: on


# validation tests
def test_eq_validator():
    with pytest.raises(ValidationError):
        NumericMeasurement(value=1, operation=CompOp.EQ, lower_limit=1, upper_limit=1)
    with pytest.raises(ValidationError):
        NumericMeasurement(value=1, operation=CompOp.EQ)


def test_ne_validator():
    with pytest.raises(ValidationError):
        NumericMeasurement(value=1, operation=CompOp.NE, lower_limit=1, upper_limit=1)
    with pytest.raises(ValidationError):
        NumericMeasurement(value=1, operation=CompOp.NE)


def test_gt_validator():
    with pytest.raises(ValidationError):
        NumericMeasurement(value=1, operation=CompOp.GT, lower_limit=1, upper_limit=1)
    with pytest.raises(ValidationError):
        NumericMeasurement(value=1, operation=CompOp.GT)


def test_ge_validator():
    with pytest.raises(ValidationError):
        NumericMeasurement(value=1, operation=CompOp.GE, lower_limit=1, upper_limit=1)
    with pytest.raises(ValidationError):
        NumericMeasurement(value=1, operation=CompOp.GE)


def test_lt_validator():
    with pytest.raises(ValidationError):
        NumericMeasurement(value=1, operation=CompOp.LT, lower_limit=1, upper_limit=1)
    with pytest.raises(ValidationError):
        NumericMeasurement(value=1, operation=CompOp.LT)


def test_le_validator():
    with pytest.raises(ValidationError):
        NumericMeasurement(value=1, operation=CompOp.LE, lower_limit=1, upper_limit=1)
    with pytest.raises(ValidationError):
        NumericMeasurement(value=1, operation=CompOp.LE)


def test_gtlt_validator():
    with pytest.raises(ValidationError):
        NumericMeasurement(value=1, operation=CompOp.GTLT, comparison_value=1)
    with pytest.raises(ValidationError):
        NumericMeasurement(value=1, operation=CompOp.GTLT)
    with pytest.raises(ValidationError):
        NumericMeasurement(value=1, operation=CompOp.GTLT, lower_limit=1)
    with pytest.raises(ValidationError):
        NumericMeasurement(value=1, operation=CompOp.GTLT, upper_limit=1)


def test_gele_validator():
    with pytest.raises(ValidationError):
        NumericMeasurement(value=1, operation=CompOp.GELE, comparison_value=1)
    with pytest.raises(ValidationError):
        NumericMeasurement(value=1, operation=CompOp.GELE)
    with pytest.raises(ValidationError):
        NumericMeasurement(value=1, operation=CompOp.GELE, lower_limit=1)
    with pytest.raises(ValidationError):
        NumericMeasurement(value=1, operation=CompOp.GELE, upper_limit=1)


def test_gelt_validator():
    with pytest.raises(ValidationError):
        NumericMeasurement(value=1, operation=CompOp.GELT, comparison_value=1)
    with pytest.raises(ValidationError):
        NumericMeasurement(value=1, operation=CompOp.GELT)
    with pytest.raises(ValidationError):
        NumericMeasurement(value=1, operation=CompOp.GELT, lower_limit=1)
    with pytest.raises(ValidationError):
        NumericMeasurement(value=1, operation=CompOp.GELT, upper_limit=1)


def test_gtle_validator():
    with pytest.raises(ValidationError):
        NumericMeasurement(value=1, operation=CompOp.GTLE, comparison_value=1)
    with pytest.raises(ValidationError):
        NumericMeasurement(value=1, operation=CompOp.GTLE)
    with pytest.raises(ValidationError):
        NumericMeasurement(value=1, operation=CompOp.GTLE, lower_limit=1)
    with pytest.raises(ValidationError):
        NumericMeasurement(value=1, operation=CompOp.GTLE, upper_limit=1)


def test_ltgt_validator():
    with pytest.raises(ValidationError):
        NumericMeasurement(value=1, operation=CompOp.LTGT, comparison_value=1)
    with pytest.raises(ValidationError):
        NumericMeasurement(value=1, operation=CompOp.LTGT)
    with pytest.raises(ValidationError):
        NumericMeasurement(value=1, operation=CompOp.LTGT, lower_limit=1)
    with pytest.raises(ValidationError):
        NumericMeasurement(value=1, operation=CompOp.LTGT, upper_limit=1)


def test_lege_validator():
    with pytest.raises(ValidationError):
        NumericMeasurement(value=1, operation=CompOp.LEGE, comparison_value=1)
    with pytest.raises(ValidationError):
        NumericMeasurement(value=1, operation=CompOp.LEGE)
    with pytest.raises(ValidationError):
        NumericMeasurement(value=1, operation=CompOp.LEGE, lower_limit=1)
    with pytest.raises(ValidationError):
        NumericMeasurement(value=1, operation=CompOp.LEGE, upper_limit=1)


def test_legt_validator():
    with pytest.raises(ValidationError):
        NumericMeasurement(value=1, operation=CompOp.LEGT, comparison_value=1)
    with pytest.raises(ValidationError):
        NumericMeasurement(value=1, operation=CompOp.LEGT)
    with pytest.raises(ValidationError):
        NumericMeasurement(value=1, operation=CompOp.LEGT, lower_limit=1)
    with pytest.raises(ValidationError):
        NumericMeasurement(value=1, operation=CompOp.LEGT, upper_limit=1)


def test_ltge_validator():
    with pytest.raises(ValidationError):
        NumericMeasurement(value=1, operation=CompOp.LTGE, comparison_value=1)
    with pytest.raises(ValidationError):
        NumericMeasurement(value=1, operation=CompOp.LTGE)
    with pytest.raises(ValidationError):
        NumericMeasurement(value=1, operation=CompOp.LTGE, lower_limit=1)
    with pytest.raises(ValidationError):
        NumericMeasurement(value=1, operation=CompOp.LTGE, upper_limit=1)
