from pathlib import Path

from pytest import MonkeyPatch

from hardpy.common.config import (
    DatabaseConfig,
    FrontendConfig,
    HardpyConfig,
    ReportsStorageMenuConfig,
    StandCloudConfig,
    StorageType,
)
from hardpy.hardpy_panel import storage_status as storage_status_module
from hardpy.hardpy_panel.storage_status import build_storage_status


def test_storage_status_standcloud_ready() -> None:
    config = HardpyConfig(
        database=DatabaseConfig(storage_type=StorageType.COUCHDB),
        stand_cloud=StandCloudConfig(autosync=True, api_key="1234567890"),
    )

    status = build_storage_status(config)

    assert status["overall_status"] == "standcloud_ready"
    assert status["standcloud"]["visible"] is True
    assert status["standcloud"]["check_enabled"] is True
    assert status["standcloud"]["configured"] is True
    assert status["standcloud"]["api_key_configured"] is True
    assert "api_key_display" not in status["standcloud"]
    assert status["local_storage"]["type"] == "couchdb"
    assert status["local_database"]["configured"] is True
    assert status["local_database"]["management_url"] == "http://localhost:5984/_utils/"
    assert status["files"]["visible"] is False


def test_storage_status_standcloud_needs_api_key() -> None:
    config = HardpyConfig(
        database=DatabaseConfig(storage_type=StorageType.COUCHDB),
        stand_cloud=StandCloudConfig(autosync=True, api_key=""),
    )

    status = build_storage_status(config)

    assert status["overall_status"] == "standcloud_needs_attention"
    assert status["standcloud"]["status"] == "needs_api_key"
    assert status["standcloud"]["configured"] is False
    assert status["local_database"]["configured"] is True


def test_storage_status_json_backend_shows_file_storage() -> None:
    tests_path = Path.cwd() / "example_tests"
    config = HardpyConfig(
        database=DatabaseConfig(storage_type=StorageType.JSON),
        stand_cloud=StandCloudConfig(autosync=False, api_key=""),
    )

    status = build_storage_status(config, tests_path)

    assert status["overall_status"] == "standcloud_needs_attention"
    assert status["standcloud"]["status"] == "not_configured"
    assert status["local_storage"]["type"] == "json"
    assert status["local_database"]["configured"] is False
    assert status["files"]["visible"] is True
    assert status["files"]["configured"] is True
    storage_dir = tests_path / ".hardpy" / "storage"
    assert status["files"]["folder_path"] == str(storage_dir)
    assert status["files"]["folder_url"] == storage_dir.as_uri()


def test_storage_status_can_hide_standcloud_menu() -> None:
    config = HardpyConfig(
        database=DatabaseConfig(storage_type=StorageType.COUCHDB),
        frontend=FrontendConfig(
            reports_storage_menu=ReportsStorageMenuConfig(show_standcloud=False),
        ),
        stand_cloud=StandCloudConfig(autosync=False, api_key=""),
    )

    status = build_storage_status(config)

    assert status["overall_status"] == "local_database_only"
    assert status["standcloud"]["visible"] is False
    assert status["standcloud"]["status"] == "not_configured"


def test_storage_status_can_disable_standcloud_check() -> None:
    config = HardpyConfig(
        database=DatabaseConfig(storage_type=StorageType.COUCHDB),
        frontend=FrontendConfig(
            reports_storage_menu=ReportsStorageMenuConfig(check_standcloud=False),
        ),
        stand_cloud=StandCloudConfig(autosync=False, api_key=""),
    )

    status = build_storage_status(config)

    assert status["overall_status"] == "local_database_only"
    assert status["standcloud"]["visible"] is True
    assert status["standcloud"]["check_enabled"] is False
    assert status["standcloud"]["status"] == "check_disabled"


def test_storage_status_reports_couchdb_connection_failure(
    monkeypatch: MonkeyPatch,
) -> None:
    monkeypatch.setattr(storage_status_module, "_is_couchdb_available", lambda _: False)
    config = HardpyConfig(
        database=DatabaseConfig(storage_type=StorageType.COUCHDB),
        stand_cloud=StandCloudConfig(autosync=False, api_key=""),
    )

    status = build_storage_status(config, check_connections=True)

    assert status["overall_status"] == "storage_error"
    assert status["local_database"]["message"] == (
        "CouchDB is not available. Reports cannot be stored."
    )
    assert status["local_database"]["status"] == "connection_failed"
