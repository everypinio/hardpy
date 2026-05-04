# Copyright (c) 2026 Everypin
# GNU General Public License v3.0 (see LICENSE or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import annotations

from pathlib import Path
from typing import Any, Final

import requests
from requests.exceptions import RequestException

from hardpy.common.config import HardpyConfig, StorageType

DOCS_BASE_URL: Final[str] = "https://everypinio.github.io/hardpy/documentation"
STANDCLOUD_API_KEYS_URL: Final[str] = (
    "https://standcloud.everypin.io/dashboard/organization-profile/"
    "organization-api-keys?utm_source=hardpy_UI"
)
COUCHDB_UNAVAILABLE_MESSAGE: Final[str] = (
    "CouchDB is not available. Reports cannot be stored."
)


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


def _standcloud_status(
    *,
    autosync: bool,
    api_key_configured: bool,
    check_enabled: bool,
) -> str:
    if not check_enabled:
        return "check_disabled"
    if autosync and api_key_configured:
        return "configured"
    if autosync:
        return "needs_api_key"
    if api_key_configured:
        return "autosync_disabled"
    return "not_configured"


def _overall_storage_status(
    *,
    standcloud_visible: bool,
    standcloud_check_enabled: bool,
    standcloud_status: str,
    storage_type: StorageType,
) -> str:
    if standcloud_visible and standcloud_check_enabled:
        if standcloud_status == "configured":
            return "standcloud_ready"
        return "standcloud_needs_attention"
    if storage_type == StorageType.COUCHDB:
        return "local_database_only"
    return "files_only"


def _local_database_status(*, is_couchdb: bool, couchdb_available: bool) -> str:
    if is_couchdb and couchdb_available:
        return "configured"
    if is_couchdb:
        return "connection_failed"
    return "not_configured"


def build_storage_status(
    config: HardpyConfig,
    tests_path: Path | None = None,
    *,
    check_connections: bool = False,
) -> dict[str, Any]:
    """Build read-only storage diagnostics for the operator panel."""
    stand_cloud = config.stand_cloud
    database = config.database
    storage_menu = config.frontend.reports_storage_menu
    resolved_tests_path = tests_path or Path.cwd()

    standcloud_visible = storage_menu.show_standcloud
    standcloud_check_enabled = storage_menu.check_standcloud
    standcloud_autosync = stand_cloud.autosync
    standcloud_api_key_configured = bool(stand_cloud.api_key.strip())
    standcloud_status = _standcloud_status(
        autosync=standcloud_autosync,
        api_key_configured=standcloud_api_key_configured,
        check_enabled=standcloud_check_enabled,
    )
    overall_status = _overall_storage_status(
        standcloud_visible=standcloud_visible,
        standcloud_check_enabled=standcloud_check_enabled,
        standcloud_status=standcloud_status,
        storage_type=database.storage_type,
    )

    is_couchdb = database.storage_type == StorageType.COUCHDB
    is_json = database.storage_type == StorageType.JSON
    file_storage_dir = _json_storage_dir(config, resolved_tests_path).resolve()
    couchdb_available = True
    if is_couchdb and check_connections:
        couchdb_available = _is_couchdb_available(database.url)

    local_database_message = ""
    if is_couchdb and not couchdb_available:
        overall_status = "storage_error"
        local_database_message = COUCHDB_UNAVAILABLE_MESSAGE

    local_database_status = _local_database_status(
        is_couchdb=is_couchdb,
        couchdb_available=couchdb_available,
    )
    local_storage_type = (
        StorageType.COUCHDB.value if is_couchdb else StorageType.JSON.value
    )

    return {
        "primary": "standcloud",
        "overall_status": overall_status,
        "configured_in": "hardpy.toml",
        "local_storage": {
            "type": local_storage_type,
        },
        "standcloud": {
            "visible": standcloud_visible,
            "check_enabled": standcloud_check_enabled,
            "configured": standcloud_status == "configured",
            "autosync": standcloud_autosync,
            "address": stand_cloud.address,
            "api_key_configured": standcloud_api_key_configured,
            "api_key_url": STANDCLOUD_API_KEYS_URL,
            "status": standcloud_status,
            "docs_url": f"{DOCS_BASE_URL}/hardpy_config/#stand_cloud",
        },
        "local_database": {
            "configured": is_couchdb,
            "type": StorageType.COUCHDB.value,
            "status": local_database_status,
            "management_url": (
                f"http://{database.host}:{database.port}/_utils/" if is_couchdb else ""
            ),
            "docs_url": f"{DOCS_BASE_URL}/database/#couchdb-instance",
            "message": local_database_message,
        },
        "files": {
            "visible": is_json,
            "configured": is_json,
            "type": StorageType.JSON.value,
            "status": "configured" if is_json else "hidden",
            "folder_path": str(file_storage_dir),
            "folder_url": file_storage_dir.as_uri(),
            "docs_url": f"{DOCS_BASE_URL}/hardpy_config/#storage_type",
        },
    }
