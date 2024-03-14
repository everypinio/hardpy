import datetime
from logging import getLogger


class DriverExample(object):
    """Driver example."""

    def __init__(self):
        self._log = getLogger(__name__)

    @property
    def current_minute(self):
        """Example of driver method."""
        current_time = datetime.datetime.now()
        return int(current_time.strftime("%M"))

    def random_method(self):
        """Example of random method."""
        self._log.warning("Random method")
