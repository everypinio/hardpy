# Copyright (c) 2026 Everypin
# GNU General Public License v3.0 (see LICENSE or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import annotations

from pathlib import Path
from typing import Any

import requests
from requests.exceptions import RequestException

from hardpy.common.config import HardpyConfig, StorageType


def build_storage_status(
    config: HardpyConfig,
    tests_path: Path | None = None,
    *,
    check_connections: bool = False,
) -> dict[str, Any]:
    """Build read-only storage diagnostics for the operator panel."""
    database = config.database
    resolved_tests_path = tests_path or Path.cwd()

    standcloud_status = _standcloud_status(config)
    overall_status = _overall_storage_status(config, standcloud_status)

    is_couchdb = database.storage_type == StorageType.COUCHDB
    file_storage_dir = _json_storage_dir(config, resolved_tests_path).resolve()
    couchdb_available = True
    if is_couchdb and check_connections:
        couchdb_available = _is_couchdb_available(database.url)

    if is_couchdb and not couchdb_available:
        overall_status = "storage_error"

    local_database_status = _local_database_status(config, couchdb_available)

    return {
        "overall_status": overall_status,
        "standcloud": {
            "status": standcloud_status,
        },
        "local_database": {
            "status": local_database_status,
        },
        "files": {
            "folder_path": str(file_storage_dir),
            "folder_url": file_storage_dir.as_uri(),
        },
    }


def _json_storage_dir(config: HardpyConfig, tests_path: Path) -> Path:
    config_storage_path = Path(config.database.storage_path)
    if config_storage_path.is_absolute():
        return config_storage_path / "storage"
    return tests_path / config.database.storage_path / "storage"


def _is_couchdb_available(url: str) -> bool:
    try:
        response = requests.get(url, timeout=1)
    except RequestException:
        return False
    return response.ok


def _standcloud_status(config: HardpyConfig) -> str:
    stand_cloud = config.stand_cloud
    storage_menu = config.frontend.reports_storage_menu
    api_key_configured = bool(stand_cloud.api_key.strip())

    if not storage_menu.check_standcloud:
        return "check_disabled"
    if stand_cloud.autosync and api_key_configured:
        return "configured"
    if stand_cloud.autosync:
        return "needs_api_key"
    if api_key_configured:
        return "autosync_disabled"
    return "not_configured"


def _overall_storage_status(config: HardpyConfig, standcloud_status: str) -> str:
    storage_menu = config.frontend.reports_storage_menu
    if storage_menu.show_standcloud and storage_menu.check_standcloud:
        if standcloud_status == "configured":
            return "standcloud_ready"
        return "standcloud_needs_attention"
    if config.database.storage_type == StorageType.COUCHDB:
        return "local_database_only"
    return "files_only"


def _local_database_status(config: HardpyConfig, couchdb_available: bool) -> str:
    is_couchdb = config.database.storage_type == StorageType.COUCHDB
    if is_couchdb and couchdb_available:
        return "configured"
    if is_couchdb:
        return "connection_failed"
    return "not_configured"
