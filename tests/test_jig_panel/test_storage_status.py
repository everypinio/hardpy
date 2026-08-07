from pathlib import Path

from pytest import MonkeyPatch

from jig.common.config import (
    DatabaseConfig,
    FrontendConfig,
    JigConfig,
    ReportsStorageMenuConfig,
    StandCloudConfig,
    StorageType,
)
from jig.jig_panel import storage_status as storage_status_module
from jig.jig_panel.storage_status import build_storage_status


def test_storage_status_standcloud_ready() -> None:
    config = JigConfig(
        database=DatabaseConfig(storage_type=StorageType.COUCHDB),
        stand_cloud=StandCloudConfig(autosync=True, api_key="1234567890"),
    )

    status = build_storage_status(config)

    assert status["overall_status"] == "standcloud_ready"
    assert status["standcloud"]["status"] == "configured"
    assert "visible" not in status["standcloud"]
    assert "check_enabled" not in status["standcloud"]
    assert "configured" not in status["standcloud"]
    assert "api_key_configured" not in status["standcloud"]
    assert "api_key_display" not in status["standcloud"]
    assert "api_key_url" not in status["standcloud"]
    assert "local_storage" not in status
    assert "configured" not in status["local_database"]
    assert "management_url" not in status["local_database"]
    assert "visible" not in status["files"]
    assert "configured" not in status["files"]


def test_storage_status_standcloud_needs_api_key() -> None:
    config = JigConfig(
        database=DatabaseConfig(storage_type=StorageType.COUCHDB),
        stand_cloud=StandCloudConfig(autosync=True, api_key=""),
    )

    status = build_storage_status(config)

    assert status["overall_status"] == "standcloud_needs_attention"
    assert status["standcloud"]["status"] == "needs_api_key"
    assert status["local_database"]["status"] == "configured"


def test_storage_status_json_backend_shows_file_storage() -> None:
    tests_path = Path.cwd() / "example_tests"
    config = JigConfig(
        database=DatabaseConfig(storage_type=StorageType.JSON),
        stand_cloud=StandCloudConfig(autosync=False, api_key=""),
    )

    status = build_storage_status(config, tests_path)

    assert status["overall_status"] == "standcloud_needs_attention"
    assert status["standcloud"]["status"] == "not_configured"
    assert status["local_database"]["status"] == "not_configured"
    storage_dir = tests_path / ".jig" / "storage"
    assert status["files"]["folder_path"] == str(storage_dir)
    assert status["files"]["folder_url"] == storage_dir.as_uri()


def test_storage_status_can_hide_standcloud_menu() -> None:
    config = JigConfig(
        database=DatabaseConfig(storage_type=StorageType.COUCHDB),
        frontend=FrontendConfig(
            reports_storage_menu=ReportsStorageMenuConfig(show_standcloud=False),
        ),
        stand_cloud=StandCloudConfig(autosync=False, api_key=""),
    )

    status = build_storage_status(config)

    assert status["overall_status"] == "local_database_only"
    assert status["standcloud"]["status"] == "not_configured"


def test_storage_status_can_disable_standcloud_check() -> None:
    config = JigConfig(
        database=DatabaseConfig(storage_type=StorageType.COUCHDB),
        frontend=FrontendConfig(
            reports_storage_menu=ReportsStorageMenuConfig(check_standcloud=False),
        ),
        stand_cloud=StandCloudConfig(autosync=False, api_key=""),
    )

    status = build_storage_status(config)

    assert status["overall_status"] == "local_database_only"
    assert status["standcloud"]["status"] == "check_disabled"


def test_storage_status_reports_couchdb_connection_failure(
    monkeypatch: MonkeyPatch,
) -> None:
    monkeypatch.setattr(storage_status_module, "_is_couchdb_available", lambda _: False)
    config = JigConfig(
        database=DatabaseConfig(storage_type=StorageType.COUCHDB),
        stand_cloud=StandCloudConfig(autosync=False, api_key=""),
    )

    status = build_storage_status(config, check_connections=True)

    assert status["overall_status"] == "storage_error"
    assert status["local_database"]["status"] == "connection_failed"
