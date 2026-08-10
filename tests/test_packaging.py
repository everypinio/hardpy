# Copyright (c) 2026 Everypin
# GNU General Public License v3.0 (see LICENSE or https://www.gnu.org/licenses/gpl-3.0.txt)

from pathlib import Path
from typing import Any

import tomli

from jig import DISTRIBUTION_NAME, __version__

PYPROJECT_PATH = Path(__file__).resolve().parent.parent / "pyproject.toml"


def _project_metadata() -> dict[str, Any]:
    with PYPROJECT_PATH.open("rb") as pyproject_file:
        return tomli.load(pyproject_file)["project"]


def test_distribution_name_matches_pyproject():
    """Keep the packaged name and the name the package looks up in sync.

    `jig.__version__` resolves installed metadata by distribution name, so
    renaming the distribution in pyproject.toml must be mirrored in `jig`.
    """
    assert _project_metadata()["name"] == DISTRIBUTION_NAME


def test_version_resolves_from_installed_metadata():
    """Fail loudly when the reported version drifts from the packaged one.

    An unresolvable distribution name degrades `__version__` to "unknown"
    silently, shipping a package and a CLI that report no version.
    """
    assert __version__ == _project_metadata()["version"], (
        f"Installed {DISTRIBUTION_NAME} metadata does not match pyproject.toml. "
        f"Reinstall the package (`pip install -e .`) after a version bump."
    )
