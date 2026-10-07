from __future__ import annotations

import json
from typing import TYPE_CHECKING

from hardpy.hardpy_panel.json_storage_data import read_json_storage_rows

if TYPE_CHECKING:
    from pathlib import Path

DOC_ID = "0.0.0.0_8000"


def _write_doc(storage_dir: Path, name: str, doc: dict | None = None) -> None:
    doc = {"_id": name, "name": name, "status": "passed"} if doc is None else doc
    (storage_dir / f"{name}.json").write_text(json.dumps(doc))


def _ids(result: dict) -> list[str]:
    return [row["id"] for row in result["rows"]]


def test_json_storage_rows_missing_dir(tmp_path: Path) -> None:
    result = read_json_storage_rows(tmp_path / "missing", DOC_ID)

    assert result == {"rows": [], "total_rows": 0, "history_total": 0}


def test_json_storage_rows_all_history_without_limit(tmp_path: Path) -> None:
    _write_doc(tmp_path, DOC_ID)
    for timestamp in ("1000", "3000", "2000"):
        _write_doc(tmp_path, timestamp)

    result = read_json_storage_rows(tmp_path, DOC_ID)

    assert _ids(result) == [DOC_ID, "3000", "2000", "1000"]
    assert result["total_rows"] == 4
    assert result["history_total"] == 3


def test_json_storage_rows_history_limit(tmp_path: Path) -> None:
    _write_doc(tmp_path, DOC_ID)
    for timestamp in range(1000, 1020):
        _write_doc(tmp_path, str(timestamp))

    result = read_json_storage_rows(tmp_path, DOC_ID, history_limit=5)

    assert _ids(result) == [DOC_ID, "1019", "1018", "1017", "1016", "1015"]
    assert result["total_rows"] == 21
    assert result["history_total"] == 20


def test_json_storage_rows_zero_limit_returns_current_only(tmp_path: Path) -> None:
    _write_doc(tmp_path, DOC_ID)
    _write_doc(tmp_path, "1000")

    result = read_json_storage_rows(tmp_path, DOC_ID, history_limit=0)

    assert _ids(result) == [DOC_ID]
    assert result["history_total"] == 1


def test_json_storage_rows_sorts_timestamps_numerically(tmp_path: Path) -> None:
    _write_doc(tmp_path, "999")
    _write_doc(tmp_path, "1000")

    result = read_json_storage_rows(tmp_path, DOC_ID, history_limit=1)

    assert _ids(result) == ["1000"]


def test_json_storage_rows_skips_invalid_file(tmp_path: Path) -> None:
    _write_doc(tmp_path, DOC_ID)
    (tmp_path / "1000.json").write_text("{not json")

    result = read_json_storage_rows(tmp_path, DOC_ID)

    assert _ids(result) == [DOC_ID]
    assert result["history_total"] == 1


def test_json_storage_rows_row_format(tmp_path: Path) -> None:
    _write_doc(tmp_path, DOC_ID, {"_id": DOC_ID, "_rev": "3-abc", "status": "run"})

    row = read_json_storage_rows(tmp_path, DOC_ID)["rows"][0]

    assert row == {
        "id": DOC_ID,
        "key": DOC_ID,
        "value": {"rev": "3-abc"},
        "doc": {"_id": DOC_ID, "_rev": "3-abc", "status": "run"},
    }
