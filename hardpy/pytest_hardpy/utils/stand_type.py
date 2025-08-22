# Copyright (c) 2025 Everypin
# GNU General Public License v3.0 (see LICENSE or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import annotations

from pydantic import model_validator

from hardpy.pytest_hardpy.db.schema.v1 import (
    IBaseMeasurement as BaseMeasurementModel,
    Instrument as InstrumentModel,
    NumericMeasurement as NumericMeasurementModel,
    SubUnit as SubUnitModel,
)
from hardpy.pytest_hardpy.utils.const import ComparisonOperation as CompOp


class Instrument(InstrumentModel):
    """Test stand instrument (equipment)."""


class SubUnit(SubUnitModel):
    """Sub unit of DUT."""


class BaseMeasurement(BaseMeasurementModel):
    """Base class for all measurements."""


class NumericMeasurement(NumericMeasurementModel):
    """Represents a measurement with value and comparison operation."""

    @model_validator(mode="after")
    def validate_operation_requirements(self) -> NumericMeasurement:
        """Validate field requirements based on selected operation."""
        if (
            self.operation
            in (CompOp.EQ, CompOp.NE, CompOp.GT, CompOp.LT, CompOp.GE, CompOp.LE)
            and self.comparison_value is None
        ):
            msg = f"Comparison_value required for {self.operation} operation"
            raise ValueError(msg)

        if self.operation in (
            CompOp.GTLT,
            CompOp.GELE,
            CompOp.GELT,
            CompOp.GTLE,
            CompOp.LTGT,
            CompOp.LEGE,
            CompOp.LEGT,
            CompOp.LTGE,
        ) and (self.lower_limit is None or self.upper_limit is None):
            msg = "lower_limit and upper_limit required for range operations"
            raise ValueError(msg)

        return self

    def check_condition(self) -> bool:  # noqa: C901,PLR0912
        """Evaluate the measurement based on the selected operation."""
        res = False
        match self.operation:
            case CompOp.EQ:
                res = self.value == self.comparison_value
            case CompOp.NE:
                res = self.value != self.comparison_value
            case CompOp.GT:
                res = self.value > self.comparison_value
            case CompOp.LT:
                res = self.value < self.comparison_value
            case CompOp.GE:
                res = self.value >= self.comparison_value
            case CompOp.LE:
                res = self.value <= self.comparison_value
            case CompOp.GTLT:
                res = self.value > self.lower_limit and self.value < self.upper_limit
            case CompOp.GELE:
                res = self.value >= self.lower_limit and self.value <= self.upper_limit
            case CompOp.GELT:
                res = self.value >= self.lower_limit and self.value < self.upper_limit
            case CompOp.GTLE:
                res = self.value > self.lower_limit and self.value <= self.upper_limit
            case CompOp.LTGT:
                res = self.value < self.lower_limit and self.value > self.upper_limit
            case CompOp.LEGE:
                res = self.value <= self.lower_limit and self.value >= self.upper_limit
            case CompOp.LEGT:
                res = self.value <= self.lower_limit and self.value > self.upper_limit
            case CompOp.LTGE:
                res = self.value < self.lower_limit and self.value >= self.upper_limit
        return res
