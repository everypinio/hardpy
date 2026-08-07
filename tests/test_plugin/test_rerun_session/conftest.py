import pytest


@pytest.fixture
def jig_opts_repeat(jig_opts: list[str]):
    # The restart should check the uncleaned database
    assert "--jig-clear-database" not in jig_opts[1:]
    return jig_opts[1:]
