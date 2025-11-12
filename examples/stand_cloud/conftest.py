import pytest
from driver_example import DriverExample  # type: ignore


@pytest.fixture(scope="session")
def driver_example():
    example = DriverExample()
    yield example

