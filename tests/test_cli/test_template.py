from pathlib import Path

from hardpy.cli.template import TemplateGenerator
from hardpy.common.config import (
    HardpyConfig,
)

db_user = "dev1"
db_password = "dev1"
db_host = "localhost1"
db_port = 5985

socket_host = "localhost1"
socket_port = 6526


def test_create_file_method(tmp_path: Path):
    config = {}
    generator = TemplateGenerator(config)  # type: ignore
    file_path = tmp_path / "test_file.txt"
    content = "Hello, World!"
    generator.create_file(file_path, content)
    assert file_path.exists()
    assert file_path.read_text() == content


def test_docker_compose_yaml_default_content():
    template_generator = TemplateGenerator(HardpyConfig())
    docker_compose_yaml = template_generator.docker_compose_yaml
    assert "5984:5984" in docker_compose_yaml


def test_docker_compose_yaml_not_default_content():
    config = HardpyConfig()
    config.database.port = db_port
    template_generator = TemplateGenerator(config)
    docker_compose_yaml = template_generator.docker_compose_yaml
    assert f"{db_port}:5984" in docker_compose_yaml


def test_couchdb_ini_default_content():
    template_generator = TemplateGenerator(HardpyConfig())
    couchdb_ini = template_generator.couchdb_ini
    expected_lines = [";port = 5984", ";bind_address = localhost"]

    assert all(line in couchdb_ini for line in expected_lines)


def test_couchdb_ini_not_default_content():
    config = HardpyConfig()
    config.database.port = db_port
    config.database.host = db_host
    template_generator = TemplateGenerator(config)
    couchdb_ini = template_generator.couchdb_ini
    expected_lines = f""";port = {db_port}
;bind_address = {db_host}"""

    assert expected_lines in couchdb_ini


def test_pytest_ini_default_content():
    template_generator = TemplateGenerator(HardpyConfig())
    pytest_ini = template_generator.pytest_ini
    assert "addopts = --hardpy-pt" in pytest_ini


def test_pytest_ini_not_default_content():
    config = HardpyConfig()
    config.database.port = db_port
    config.database.host = db_host
    config.socket.port = socket_port
    config.socket.host = socket_host
    template_generator = TemplateGenerator(config)
    pytest_ini = template_generator.pytest_ini
    assert (
        f"""--hardpy-db-url http://dev:dev@{db_host}:{db_port}/
          --hardpy-sh {socket_host}
          --hardpy-sp {socket_port}"""
        in pytest_ini
    )
