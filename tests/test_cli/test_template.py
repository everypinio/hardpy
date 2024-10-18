from pathlib import Path

from hardpy.cli.template import TemplateGenerator
from hardpy.common.config import (
    HardpyConfig,
)

db_no_default_host = "localhost1"
db_no_default_port = 5985
socket_no_default_host = "localhost1"
socket_no_default_port = 6526

db_default_host = "localhost"
db_default_port = "5984"
frontend_default_host = "localhost"
frontend_default_port = "8000"
socket_default_host = "localhost"
socket_default_port = "6525"


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
    assert f"{db_default_port}:5984" in docker_compose_yaml


def test_docker_compose_yaml_no_default_content():
    config = HardpyConfig()
    config.database.port = db_no_default_port
    template_generator = TemplateGenerator(config)
    docker_compose_yaml = template_generator.docker_compose_yaml
    assert f"{db_no_default_port}:5984" in docker_compose_yaml


def test_couchdb_ini_default_content():
    template_generator = TemplateGenerator(HardpyConfig())
    couchdb_ini = template_generator.couchdb_ini
    expected_lines = f""";port = {db_default_port}
;bind_address = {db_default_host}"""

    assert expected_lines in couchdb_ini


def test_couchdb_ini_no_default_content():
    config = HardpyConfig()
    config.database.port = db_no_default_port
    config.database.host = db_no_default_host
    template_generator = TemplateGenerator(config)
    couchdb_ini = template_generator.couchdb_ini
    expected_lines = f""";port = {db_no_default_port}
;bind_address = {db_no_default_host}"""

    assert expected_lines in couchdb_ini


def test_pytest_ini_default_content():
    config = HardpyConfig()
    template_generator = TemplateGenerator(config)
    pytest_ini = template_generator.pytest_ini
    assert (
        f"""--hardpy-db-url http://dev:dev@{db_default_host}:{db_default_port}/
          --hardpy-sh {socket_default_host}
          --hardpy-sp {socket_default_port}"""
        in pytest_ini
    )


def test_pytest_ini_no_default_content():
    config = HardpyConfig()
    config.database.port = db_no_default_port
    config.database.host = db_no_default_host
    config.socket.port = socket_no_default_port
    config.socket.host = socket_no_default_host
    template_generator = TemplateGenerator(config)
    pytest_ini = template_generator.pytest_ini
    assert (
        f"""--hardpy-db-url http://dev:dev@{db_no_default_host}:{db_no_default_port}/
          --hardpy-sh {socket_no_default_host}
          --hardpy-sp {socket_no_default_port}"""
        in pytest_ini
    )
