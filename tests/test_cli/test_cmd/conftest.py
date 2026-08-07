from __future__ import annotations

import subprocess
from typing import TYPE_CHECKING

import pytest

if TYPE_CHECKING:
    from pathlib import Path

JIG_INIT_CMD = ["jig", "init", "--frontend-port", "8000"]


def pytest_configure(config: pytest.Config) -> None:
    config.addinivalue_line("markers", "manual")


@pytest.fixture
def project_dir(tmp_path: Path) -> Path:
    """Create a test project with necessary test files."""
    subprocess.run([*JIG_INIT_CMD, str(tmp_path)], check=True)

    (tmp_path / "test_simple.py").write_text("""
import time

def test_basic_api_call():
    time.sleep(7)
    assert True
""")
    (tmp_path / "__init__.py").touch()
    return tmp_path


@pytest.fixture
def project_dir_with_ini(tmp_path: Path) -> Path:
    """Create test project with pytest.ini configuration."""
    return _create_test_project_with_ini(tmp_path, "DUT-007")


@pytest.fixture
def project_dir_with_ini_incorrect(tmp_path: Path) -> Path:
    """Create test project with pytest.ini configuration (incorrect)."""
    return _create_test_project_with_ini(tmp_path, "DUT-006")


@pytest.fixture
def project_dir_with_args(tmp_path: Path) -> Path:
    """Create test project with pytest.ini configuration."""
    subprocess.run([*JIG_INIT_CMD, str(tmp_path)], check=True)

    ini_content = """[pytest]
addopts = --jig-pt
        --jig-db-url http://dev:dev@localhost:5984/
"""
    (tmp_path / "pytest.ini").write_text(ini_content)

    (tmp_path / "test_jig_args.py").write_text("""
import jig
import time

def test_ini_parameters(jig_start_args):
    time.sleep(3)
    assert jig_start_args.get("test_mode") == "debug"
    assert jig_start_args.get("device_id") == "DUT-007"
    assert jig_start_args.get("retry_count") == "3"
""")

    (tmp_path / "__init__.py").touch()
    return tmp_path


def _create_test_project_with_ini(tmp_path: Path, device_id: str) -> Path:
    subprocess.run([*JIG_INIT_CMD, str(tmp_path)], check=True)

    ini_content = f"""[pytest]
addopts = --jig-pt
        --jig-db-url http://dev:dev@localhost:5984/
        --jig-start-arg test_mode=debug
        --jig-start-arg device_id={device_id}
        --jig-start-arg retry_count=3
"""
    (tmp_path / "pytest.ini").write_text(ini_content)

    (tmp_path / "test_jig_args.py").write_text("""
import jig

def test_ini_parameters(jig_start_args):
    assert jig_start_args.get("test_mode") == "debug"
    assert jig_start_args.get("device_id") == "DUT-007"
    assert jig_start_args.get("retry_count") == "3"
""")

    (tmp_path / "__init__.py").touch()
    return tmp_path
