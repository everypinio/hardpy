# Copyright (c) 2026 Everypin
# GNU General Public License v3.0 (see LICENSE or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import annotations

from pathlib import Path
from typing import Any, Final

from hardpy.common.config import HardpyConfig, StorageType

DOCS_BASE_URL: Final[str] = "https://everypinio.github.io/hardpy/documentation"
STANDCLOUD_API_KEYS_URL: Final[str] = (
    "https://standcloud.everypin.io/dashboard/organization-profile/"
    "organization-api-keys?utm_source=hardpy_UI"
)


def _mask_api_key(api_key: str) -> str:
    stripped_key = api_key.strip()
    if not stripped_key:
        return ""
    visible_suffix = stripped_key[-4:]
    return f"{'*' * max(len(stripped_key) - 4, 4)}{visible_suffix}"


def _json_storage_dir(config: HardpyConfig, tests_path: Path) -> Path:
    config_storage_path = Path(config.database.storage_path)
    if config_storage_path.is_absolute():
        return config_storage_path / "storage"
    return tests_path / config.database.storage_path / "storage"


def build_storage_status(
    config: HardpyConfig,
    tests_path: Path | None = None,
) -> dict[str, Any]:
    """Build read-only storage diagnostics for the operator panel."""
    stand_cloud = config.stand_cloud
    database = config.database
    resolved_tests_path = tests_path or Path.cwd()

    standcloud_autosync = stand_cloud.autosync
    standcloud_api_key_configured = bool(stand_cloud.api_key.strip())

    if standcloud_autosync and standcloud_api_key_configured:
        standcloud_status = "configured"
    elif standcloud_autosync:
        standcloud_status = "needs_api_key"
    elif standcloud_api_key_configured:
        standcloud_status = "autosync_disabled"
    else:
        standcloud_status = "not_configured"

    if standcloud_status == "configured":
        overall_status = "standcloud_ready"
    elif standcloud_status in {"needs_api_key", "autosync_disabled"}:
        overall_status = "standcloud_needs_attention"
    elif database.storage_type == StorageType.COUCHDB:
        overall_status = "local_database_only"
    else:
        overall_status = "files_only"

    is_couchdb = database.storage_type == StorageType.COUCHDB
    is_json = database.storage_type == StorageType.JSON
    file_storage_dir = _json_storage_dir(config, resolved_tests_path).resolve()

    return {
        "primary": "standcloud",
        "overall_status": overall_status,
        "configured_in": "hardpy.toml",
        "standcloud": {
            "configured": standcloud_status == "configured",
            "autosync": standcloud_autosync,
            "address": stand_cloud.address,
            "api_key_configured": standcloud_api_key_configured,
            "api_key_display": _mask_api_key(stand_cloud.api_key),
            "api_key_url": STANDCLOUD_API_KEYS_URL,
            "status": standcloud_status,
            "docs_url": f"{DOCS_BASE_URL}/hardpy_config/#stand_cloud",
        },
        "local_database": {
            "configured": is_couchdb,
            "type": StorageType.COUCHDB.value,
            "status": "configured" if is_couchdb else "not_configured",
            "management_url": (
                f"http://{database.host}:{database.port}/_utils/" if is_couchdb else ""
            ),
            "docs_url": f"{DOCS_BASE_URL}/database/#couchdb-instance",
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
