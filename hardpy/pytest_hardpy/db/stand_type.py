# Copyright (c) 2025 Everypin
# GNU General Public License v3.0 (see LICENSE or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import annotations

from pydantic import model_validator

from hardpy.pytest_hardpy.db.schema.v1 import (
    Chart as ChartModel,
    Instrument as InstrumentModel,
    NumericMeasurement as NumericMeasurementModel,
    StringMeasurement as StringMeasurementModel,
    SubUnit as SubUnitModel,
)
from hardpy.pytest_hardpy.utils.const import ComparisonOperation as CompOp


class Instrument(InstrumentModel):
    """Test stand instrument (equipment)."""


class SubUnit(SubUnitModel):
    """Sub unit of DUT."""


class NumericMeasurement(NumericMeasurementModel):
    """Represents a numeric measurement with value and comparison operation.

    Args:
        value (int | float): The value of the measurement.
        name (str | None): The name of the measurement.
        unit (str | None): The unit of the measurement.
        operation (CompOp | None): The comparison operation to apply.
        comparison_value (int | float | None): The value to compare against.
        lower_limit (int | float | None): The lower limit for range operations.
        upper_limit (int | float | None): The upper limit for range operations.
    """

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

        if self.operation:
            self.result = self._check_condition()

        return self

    def _check_condition(self) -> bool:  # noqa: C901,PLR0912
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
                res = self.value < self.lower_limit or self.value > self.upper_limit
            case CompOp.LEGE:
                res = self.value <= self.lower_limit or self.value >= self.upper_limit
            case CompOp.LEGT:
                res = self.value <= self.lower_limit or self.value > self.upper_limit
            case CompOp.LTGE:
                res = self.value < self.lower_limit or self.value >= self.upper_limit
        return res


class StringMeasurement(StringMeasurementModel):
    """Represents a string measurement with value and comparison operation.

    Args:
        value (str): The value of the measurement.
        name (str | None): The name of the measurement.
        operation (CompOp | None): The comparison operation to apply.
        comparison_value (str | None): The value to compare against.
    """

    @model_validator(mode="after")
    def validate_operation_requirements(self) -> StringMeasurement:
        """Validate field requirements based on selected operation."""
        string_operations = (CompOp.EQ, CompOp.NE)
        if self.operation in string_operations and self.comparison_value is None:
            msg = f"Comparison_value required for {self.operation} operation"
            raise ValueError(msg)

        if self.operation and self.operation not in string_operations:
            msg = f"{self.operation} is not a valid string operation"
            raise ValueError(msg)

        if self.operation:
            self.result = self._check_condition()

        return self

    def _check_condition(self) -> bool:
        """Evaluate the measurement based on the selected operation."""
        res = False
        match self.operation:
            case CompOp.EQ:
                if self.casesensitive:
                    res = self.value == self.comparison_value
                else:
                    res = self.value.lower() == self.comparison_value.lower()
            case CompOp.NE:
                if self.casesensitive:
                    res = self.value != self.comparison_value
                else:
                    res = self.value.lower() != self.comparison_value.lower()
        return res


class Chart(ChartModel):
    """Represents a chart with data and labels.

    Args:
        type (ChartType | None): chart type.
        title (str | None): chart title.
        x_label (str | None): X label.
        y_label (str | None): Y label.
    """

    @model_validator(mode="after")
    def validate_lines(self) -> Chart:
        """Validate field requirements based on selected operation."""
        self._diff_list_len_validator(self.x_data, self.y_data)
        self._diff_list_len_validator(self.x_data, self.marker_name)

        if len(self.x_data):
            for i in range(len(self.x_data)):
                self._diff_list_len_validator(self.x_data[i], self.y_data[i])
                self._empty_list_validator(self.x_data[0])
                self._empty_list_validator(self.marker_name)

        return self

    def add_series(
        self,
        x_data: list[int | float],
        y_data: list[int | float],
        marker_name: str | None = None,
    ) -> None:
        """Add data series to chart.

        Args:
            x_data (list[int | float]): X data.
            y_data (list[int | float]): Y data.
            marker_name (str | None): series marker name.
        """
        self._diff_list_len_validator(x_data, y_data)
        self._empty_list_validator(x_data)
        self.x_data.append(x_data)
        self.y_data.append(y_data)
        self.marker_name.append(marker_name)

    def _diff_list_len_validator(self, data1: list, data2: list) -> None:
        if len(data1) != len(data2):
            msg = "data in single series must have the same length"
            raise ValueError(msg)

    def _empty_list_validator(self, data: list) -> None:
        if len(data) == 0:
            msg = "data series cannot be empty"
            raise ValueError(msg)
