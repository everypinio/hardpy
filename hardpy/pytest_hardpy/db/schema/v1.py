# Copyright (c) 2024 Everypin
# GNU General Public License v3.0 (see LICENSE or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import annotations

from abc import ABC
from collections.abc import Mapping  # noqa: TC003
from typing import ClassVar

from pydantic import BaseModel, ConfigDict, Field

from hardpy.pytest_hardpy.utils import (
    ChartType,
    ComparisonOperation as CompOp,
    Group,
    MeasurementType,
    TestStatus as Status,
)


class IBaseResult(BaseModel):
    """Base class for all result models."""

    model_config = ConfigDict(extra="forbid")

    status: Status
    stop_time: int | None
    start_time: int | None
    name: str


class CaseStateStore(IBaseResult):
    """Test case description."""

    assertion_msg: str | None = None
    msg: dict | None = None
    measurements: list[NumericMeasurement | StringMeasurement] = []
    chart: Chart | None = None
    attempt: int = 0
    group: Group
    dialog_box: dict = {}


class CaseRunStore(IBaseResult):
    """Test case description with artifact."""

    assertion_msg: str | None = None
    msg: dict | None = None
    measurements: list[NumericMeasurement | StringMeasurement] = []
    chart: Chart | None = None
    attempt: int = 0
    group: Group
    artifact: dict = {}


class ModuleStateStore(IBaseResult):
    """Test module description."""

    cases: dict[str, CaseStateStore] = {}
    group: Group


class ModuleRunStore(IBaseResult):
    """Test module description."""

    cases: dict[str, CaseRunStore] = {}
    group: Group
    artifact: dict = {}


class Dut(BaseModel):
    """Device under test description."""

    model_config = ConfigDict(extra="forbid")

    name: str | None = None
    type: str | None = None
    serial_number: str | None = None
    part_number: str | None = None
    revision: str | None = None
    sub_units: list[SubUnit] = []
    info: Mapping[str, str | int | float] = {}


class SubUnit(BaseModel):
    """Sub unit of DUT description."""

    model_config = ConfigDict(extra="forbid")

    name: str | None = None
    type: str | None = None
    serial_number: str | None = None
    part_number: str | None = None
    revision: str | None = None
    info: Mapping[str, str | int | float] = {}


class Instrument(BaseModel):
    """Instrument (power supply, oscilloscope and others) description."""

    model_config = ConfigDict(extra="forbid")

    name: str | None = None
    revision: str | None = None
    number: int | None = None
    comment: str | None = None
    info: Mapping[str, str | int | float] = {}


class TestStand(BaseModel):
    """Test stand description."""

    model_config = ConfigDict(extra="forbid")

    hw_id: str | None = None
    name: str | None = None
    revision: str | None = None
    timezone: str | None = None
    location: str | None = None
    number: int | None = None
    drivers: dict = {}  # deprecated, remove in v2
    instruments: list[Instrument] = []
    info: Mapping[str, str | int | float] = {}


class Process(BaseModel):
    """Production process description."""

    model_config = ConfigDict(extra="forbid")

    name: str | None = None
    number: int | None = None
    info: Mapping[str, str | int | float] = {}


class IBaseMeasurement(BaseModel, ABC):
    """Base class for all measurement models."""

    model_config = ConfigDict(extra="allow")

    type: MeasurementType
    name: str | None = Field(default=None)
    operation: CompOp | None = Field(default=None)
    result: bool | None = Field(default_factory=lambda: None)


class NumericMeasurement(IBaseMeasurement):
    """Numeric measurement description."""

    model_config = ConfigDict(extra="forbid")

    type: MeasurementType = Field(default=MeasurementType.NUMERIC)
    value: int | float
    name: str | None = Field(default=None)
    unit: str | None = Field(default=None)

    comparison_value: float | int | None = Field(default=None)

    lower_limit: float | int | None = Field(default=None)
    upper_limit: float | int | None = Field(default=None)


class StringMeasurement(IBaseMeasurement):
    """String measurement description."""

    model_config = ConfigDict(extra="forbid")

    type: MeasurementType = Field(default=MeasurementType.STRING)
    value: str
    name: str | None = Field(default=None)
    casesensitive: bool = Field(default=True)

    comparison_value: str | None = Field(default=None)


class Chart(BaseModel):
    """Chart description."""

    model_config = ConfigDict(extra="forbid")

    type: ChartType = Field(default=ChartType.LINE)
    title: str | None = Field(default=None)
    x_label: str | None = Field(default=None)
    y_label: str | None = Field(default=None)
    marker_name: list[str | None] = Field(default=[])
    x_data: list[list[int | float]] = Field(default_factory=lambda: [])  # noqa: PIE807
    y_data: list[list[int | float]] = Field(default_factory=lambda: [])  # noqa: PIE807


class OperatorData(BaseModel):
    """Operator data from operator panel."""

    model_config = ConfigDict(extra="forbid")

    dialog: str | None = None


class ResultStateStore(IBaseResult):
    """Test run description."""

    model_config = ConfigDict(extra="forbid")

    rev: str = Field(..., alias="_rev")
    id: str = Field(..., alias="_id")

    progress: int
    test_stand: TestStand
    dut: Dut
    process: Process
    modules: dict[str, ModuleStateStore] = {}
    user: str | None = None
    batch_serial_number: str | None = None
    caused_dut_failure_id: str | None = None
    error_code: int | None = None
    operator_msg: dict = {}
    alert: str
    operator_data: OperatorData


class ResultRunStore(IBaseResult):
    """Test run description."""

    model_config = ConfigDict(extra="forbid")
    # Create the new schema class with version update
    # when you change this class or fields in this class.
    __version__: ClassVar[int] = 1

    rev: str = Field(..., alias="_rev")
    id: str = Field(..., alias="_id")

    test_stand: TestStand
    dut: Dut
    process: Process
    modules: dict[str, ModuleRunStore] = {}
    user: str | None = None
    batch_serial_number: str | None = None
    caused_dut_failure_id: str | None = None
    error_code: int | None = None
    artifact: dict = {}
