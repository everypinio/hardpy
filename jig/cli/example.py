# Copyright (c) 2026 Everypin
# GNU General Public License v3.0 (see LICENSE or https://www.gnu.org/licenses/gpl-3.0.txt)
"""Launcher for the examples bundled with the repository checkout."""

from __future__ import annotations

from pathlib import Path
from typing import Annotated

import typer

from jig.cli.cli import run as run_panel

EXAMPLES_DIR = Path(__file__).parents[2] / "examples"


class ExampleNotFoundError(Exception):
    """Raised when no example matches the requested name."""

    def __init__(self, name: str, available: list[str]) -> None:
        self.available = available
        super().__init__(f"Example {name} not found.")


class ExampleCatalog:
    """Examples available in a directory.

    An example is a directory containing a `jig.toml` file.
    """

    def __init__(self, examples_dir: Path) -> None:
        self._examples_dir = examples_dir

    def names(self) -> list[str]:
        """Get the names of the available examples.

        Returns:
            list[str]: example names, sorted alphabetically
        """
        if not self._examples_dir.is_dir():
            return []
        return sorted(
            entry.name
            for entry in self._examples_dir.iterdir()
            if self._is_example(entry)
        )

    def path(self, name: str) -> Path:
        """Get the directory of an example.

        Args:
            name (str): example name

        Returns:
            Path: example directory

        Raises:
            ExampleNotFoundError: if the name does not match an example
        """
        example_dir = self._examples_dir / name
        if not self._is_example(example_dir):
            raise ExampleNotFoundError(name, self.names())
        return example_dir

    def _is_example(self, example_dir: Path) -> bool:
        return (example_dir / "jig.toml").is_file()


def main(
    name: Annotated[
        str | None,
        typer.Argument(help="Name of a directory in the examples folder."),
    ] = None,
    verbose: Annotated[
        bool,
        typer.Option(help="Print test collection output and Jig logs."),
    ] = False,
) -> None:
    """Run the Jig operator panel for an example.

    The available examples are listed when no name is given.

    Args:
        name (str | None): example name
        verbose (bool): print test collection output and Jig logs
    """
    catalog = ExampleCatalog(EXAMPLES_DIR)

    if name is None:
        _print_available(catalog.names())
        return

    try:
        example_dir = catalog.path(name)
    except ExampleNotFoundError as exc:
        print(str(exc))
        _print_available(exc.available)
        raise typer.Exit(1) from exc

    run_panel(str(example_dir), verbose=verbose)


def _print_available(names: list[str]) -> None:
    print(f"Available examples: {', '.join(names) or 'none'}")


def cli() -> None:
    """Run the example launcher."""
    typer.run(main)


if __name__ == "__main__":
    cli()
