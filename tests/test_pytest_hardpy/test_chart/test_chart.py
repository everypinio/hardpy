import pytest
from pydantic import ValidationError

from hardpy import Chart, ChartType


def test_empty_chart():
    chart = Chart()
    assert chart.type == ChartType.LINE
    assert chart.title is None
    assert chart.x_label is None
    assert chart.y_label is None
    assert chart.marker_name == []
    assert chart.x_data == []
    assert chart.y_data == []


def test_full_chart():
    chart = Chart(
        type=ChartType.LINE,
        title="title",
        x_label="x_label",
        y_label="y_label",
        marker_name=["marker_name", None],
        x_data=[[1, 2], [1, 2]],
        y_data=[[3, 4], [3, 4]],
    )

    assert chart.type == ChartType.LINE
    assert chart.title == "title"
    assert chart.x_label == "x_label"
    assert chart.y_label == "y_label"
    assert chart.marker_name == ["marker_name", None]
    assert chart.x_data == [[1, 2], [1, 2]]
    assert chart.y_data == [[3, 4], [3, 4]]


def test_type_validator():
    with pytest.raises(ValidationError):
        Chart(marker_name=["a"], x_data=[1, 2], y_data=[[1, 2]])
    with pytest.raises(ValidationError):
        Chart(marker_name=["a"], x_data=[[1, 2]], y_data=[1, 2])
    with pytest.raises(ValidationError):
        Chart(marker_name=[["a"]], x_data=[[1, 2]], y_data=[[1, 2]])


def test_len_validator():
    with pytest.raises(ValidationError):
        Chart(marker_name=["a"], x_data=[[]], y_data=[[]])
    with pytest.raises(ValidationError):
        Chart(marker_name=[], x_data=[[1]], y_data=[[1]])
    with pytest.raises(ValidationError):
        Chart(marker_name=["a", "b"], x_data=[[1, 2]], y_data=[[1, 2]])
    with pytest.raises(ValidationError):
        Chart(marker_name=["a"], x_data=[[1, 2], [0, 1]], y_data=[[1, 2]])
    with pytest.raises(ValidationError):
        Chart(marker_name=["a"], x_data=[[1, 2]], y_data=[[1, 2], [0, 1]])
    with pytest.raises(ValidationError):
        Chart(marker_name=["a", "b"], x_data=[[1, 2]], y_data=[[1, 2, 3]])
    with pytest.raises(ValidationError):
        Chart(marker_name=["a", "b"], x_data=[[1, 2, 3]], y_data=[[1, 2]])
    with pytest.raises(ValidationError):
        Chart(marker_name=["a", "b", "c"], x_data=[[1, 2]], y_data=[[1, 2]])

def test_add_series():
    chart = Chart()
    chart.add_series(x_data=[1, 2], y_data=[1, 2])
    assert chart.x_data == [[1, 2]]
    assert chart.y_data == [[1, 2]]
    assert chart.marker_name == [None]

    with pytest.raises(ValueError):  # noqa: PT011
        chart.add_series(x_data=[1, 2, 3], y_data=[1, 2])
    with pytest.raises(ValueError):  # noqa: PT011
        chart.add_series(x_data=[], y_data=[])
