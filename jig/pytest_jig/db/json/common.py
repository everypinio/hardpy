# Copyright (c) 2026 Everypin
# GNU General Public License v3.0 (see LICENSE or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import annotations

import json
from logging import getLogger
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from pathlib import Path


log = getLogger(__name__)


def update_db(storage_dir: Path, file_path: Path, doc: dict) -> None:
    """Persist in-memory document to JSON file with atomic write."""
    storage_dir.mkdir(parents=True, exist_ok=True)
    temp_file = file_path.with_suffix(".tmp")

    try:
        with temp_file.open("w") as f:
            json.dump(doc, f, indent=2, default=str)
        temp_file.replace(file_path)
    except Exception as exc:
        msg = f"Error writing to storage file: {exc}"
        log.exception(msg)
        if temp_file.exists():
            temp_file.unlink()
        raise


def update_doc(file_path: Path, doc: dict) -> dict:
    """Reload document from JSON file to memory."""
    if file_path.exists():
        try:
            with file_path.open("r") as f:
                doc = json.load(f)
        except json.JSONDecodeError as exc:
            msg = f"Error reading storage file: {exc}"
            log.exception(msg)
        except Exception as exc:
            msg = f"Error reading storage file: {exc}"
            log.exception(msg)
            raise
    return doc
