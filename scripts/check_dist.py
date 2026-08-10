"""Verify built distributions ship the operator panel frontend."""  # noqa: INP001

import sys
import tarfile
import zipfile
from pathlib import Path

DIST_DIR = Path("dist")

# The panel serves these from `jig/jig_panel/frontend/dist` at runtime. They are
# produced by the sdist build hook, so a packaging change can silently drop them
# and leave an installed package whose panel answers 404.
REQUIRED_MEMBERS = (
    "jig/jig_panel/frontend/dist/index.html",
    "jig/jig_panel/frontend/dist/locales/en/translation.json",
)


def _sdist_members(archive: Path) -> set[str]:
    with tarfile.open(archive) as tar:
        # Every sdist member is prefixed with `<name>-<version>/`.
        return {name.partition("/")[2] for name in tar.getnames()}


def _wheel_members(archive: Path) -> set[str]:
    with zipfile.ZipFile(archive) as wheel:
        return set(wheel.namelist())


def _missing_members(archive: Path) -> list[str]:
    members = (
        _sdist_members(archive)
        if archive.name.endswith(".tar.gz")
        else _wheel_members(archive)
    )
    return [required for required in REQUIRED_MEMBERS if required not in members]


def main() -> int:
    """Report distributions that are missing the frontend bundle."""
    archives = sorted(DIST_DIR.glob("*.tar.gz")) + sorted(DIST_DIR.glob("*.whl"))
    if not archives:
        sys.stderr.write(f"No distributions found in {DIST_DIR}/\n")
        return 1

    failures = 0
    for archive in archives:
        missing = _missing_members(archive)
        if missing:
            failures += 1
            sys.stderr.write(f"{archive.name} is missing: {', '.join(missing)}\n")
        else:
            sys.stdout.write(f"{archive.name} contains the frontend bundle\n")

    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
