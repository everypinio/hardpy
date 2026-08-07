from pathlib import Path

import pytest

from jig.cli.example import EXAMPLES_DIR, ExampleCatalog, ExampleNotFoundError


def create_example(examples_dir: Path, name: str) -> Path:
    example_dir = examples_dir / name
    example_dir.mkdir(parents=True)
    (example_dir / "jig.toml").touch()
    return example_dir


def test_catalog_lists_directories_with_a_config(tmp_path: Path):
    create_example(tmp_path, "second")
    create_example(tmp_path, "first")
    (tmp_path / "without_config").mkdir()

    assert ExampleCatalog(tmp_path).names() == ["first", "second"]


def test_catalog_of_a_missing_directory_is_empty(tmp_path: Path):
    assert ExampleCatalog(tmp_path / "absent").names() == []


def test_catalog_finds_the_example_directory(tmp_path: Path):
    example_dir = create_example(tmp_path, "full_capabilities")

    assert ExampleCatalog(tmp_path).path("full_capabilities") == example_dir


def test_catalog_rejects_an_unknown_example(tmp_path: Path):
    create_example(tmp_path, "known")

    with pytest.raises(ExampleNotFoundError) as exc_info:
        ExampleCatalog(tmp_path).path("unknown")

    assert exc_info.value.available == ["known"]


def test_catalog_rejects_a_directory_without_a_config(tmp_path: Path):
    (tmp_path / "without_config").mkdir()

    with pytest.raises(ExampleNotFoundError):
        ExampleCatalog(tmp_path).path("without_config")


def test_repository_examples_are_found():
    assert "full_capabilities" in ExampleCatalog(EXAMPLES_DIR).names()
