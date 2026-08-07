from pathlib import Path

import pytest

from jig.common.config import ConfigManager

pytest_plugins = "pytester"


@pytest.fixture(params=["couchdb", "json"], autouse=True)
def jig_opts(request):  # noqa: ANN001
    config_manager = ConfigManager()
    if request.param == "couchdb":
        config_data = config_manager.read_config(
            Path(__file__).parent.resolve(),
        )
        if not config_data:
            msg = "Config not found"
            raise RuntimeError(msg)

        return [
            "--jig-clear-database",
            "--jig-db-url",
            config_data.database.url,
            "--jig-pt",
        ]
    if request.param == "json":
        config_data = config_manager.read_config(
            Path(__file__).parent / "json_toml",
        )
        return ["--jig-clear-database", "--jig-pt"]
    return None
