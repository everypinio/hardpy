from pathlib import Path

import pytest

from hardpy.cli.template import TemplateGenerator
from hardpy.common.config import (
    DatabaseConfig,
    FrontendConfig,
    HardpyConfig,
    SocketConfig,
)


def test_create_file_method(tmp_path: Path):
    config = {}
    generator = TemplateGenerator(config)  # type: ignore
    file_path = tmp_path / "test_file.txt"
    content = "Hello, World!"
    generator.create_file(file_path, content)
    assert file_path.exists()
    assert file_path.read_text() == content


def test_docker_compose_yaml_property():
    config = HardpyConfig(
        title="Test HardPy Config",
        tests_dir="my_tests",
        database=DatabaseConfig(user="db_user", password="db_password"),  # noqa: S106
        frontend=FrontendConfig(host="fe_host", port=3000),
        socket=SocketConfig(host="socket_host", port=4000),
    )
    generator = TemplateGenerator(config)
    docker_compose_yaml = generator.docker_compose_yaml
    assert "5984:5984" in docker_compose_yaml


def test_couchdb_ini_property():
    config = HardpyConfig(
        title="Test HardPy Config",
        tests_dir="my_tests",
        database=DatabaseConfig(user="db_user", password="db_password"),  # noqa: S106
        frontend=FrontendConfig(host="fe_host", port=3000),
        socket=SocketConfig(host="socket_host", port=4000),
    )
    generator = TemplateGenerator(config)
    couchdb_ini = generator.couchdb_ini
    assert ";port = 5984" in couchdb_ini
    assert ";bind_address = localhost" in couchdb_ini


def test_pytest_ini_property():
    config = HardpyConfig(
        title="Test HardPy Config",
        tests_dir="my_tests",
        database=DatabaseConfig(user="db_user", password="db_password"),  # noqa: S106
        frontend=FrontendConfig(host="fe_host", port=3000),
        socket=SocketConfig(host="socket_host", port=4000),
    )
    generator = TemplateGenerator(config)
    pytest_ini = generator.pytest_ini
    assert "addopts = --hardpy-pt" in pytest_ini


def test_test_1_property():
    config = {}  # mock config
    generator = TemplateGenerator(config)  # type: ignore
    test_1_py = generator.test_1_py
    assert "import hardpy" in test_1_py


def test_conftest_py_property():
    config = {}  # mock config
    generator = TemplateGenerator(config)  # type: ignore
    conftest_py = generator.conftest_py
    assert "def fill_actions_after_test" in conftest_py
