# Copyright (c) 2026 Everypin
# GNU General Public License v3.0 (see LICENSE or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import annotations

import json
import logging
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from pathlib import Path

logger = logging.getLogger(__name__)


def read_json_storage_rows(
    storage_dir: Path,
    doc_id: str,
    history_limit: int | None = None,
) -> dict[str, Any]:
    """Read the current run document and test history from JSON statestore.

    The statestore directory contains the current run document `<doc_id>.json`
    and one history document per finished run, named by its millisecond timestamp.
    The operator panel polls this data, so reading and returning every history
    document on each call gets slow as the history grows.

    Args:
        storage_dir: path to the statestore directory
        doc_id: current run document id
        history_limit: maximum number of newest history documents to return,
            all history documents if None

    Returns:
        dict[str, Any]: rows in CouchDB `_all_docs` format, total number of
            documents and total number of history documents
    """
    if not storage_dir.exists():
        return {"rows": [], "total_rows": 0, "history_total": 0}

    current_file = storage_dir / f"{doc_id}.json"
    history_files = [
        path for path in storage_dir.glob("*.json") if path.name != current_file.name
    ]
    history_files.sort(key=_history_sort_key, reverse=True)
    history_total = len(history_files)
    if history_limit is not None:
        history_files = history_files[:history_limit]

    files = [current_file, *history_files] if current_file.exists() else history_files

    rows = []
    for json_file in files:
        data = _read_json_file(json_file)
        if data is None:
            continue
        row_id = data.get("_id", json_file.stem)
        rows.append(
            {
                "id": row_id,
                "key": row_id,
                "value": {"rev": data.get("_rev", "1-0")},
                "doc": data,
            },
        )

    total_rows = history_total + (1 if current_file.exists() else 0)
    return {"rows": rows, "total_rows": total_rows, "history_total": history_total}


def _history_sort_key(path: Path) -> int:
    # history documents are named by millisecond timestamp, fall back to mtime
    if path.stem.isdigit():
        return int(path.stem)
    try:
        return int(path.stat().st_mtime * 1000)
    except OSError:
        return 0


def _read_json_file(json_file: Path) -> dict | None:
    try:
        with json_file.open("r") as f:
            return json.load(f)
    except (OSError, json.JSONDecodeError) as exc:
        logger.warning(f"Error reading {json_file}: {exc}")
        return None
