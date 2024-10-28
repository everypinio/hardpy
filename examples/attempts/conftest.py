import datetime

import pytest


class CurrentMinute:
    """Class example."""

    def get_minute(self):
        """Get current minute."""
        current_time = datetime.datetime.now()  # noqa: DTZ005
        return int(current_time.strftime("%M"))


@pytest.fixture
def current_minute():
    current_time = CurrentMinute()
    yield current_time
