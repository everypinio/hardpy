import datetime


class DriverExample:
    """Driver example."""


    @property
    def current_minute(self):
        """Example of driver method."""
        current_time = datetime.datetime.now()  # noqa: DTZ005
        return int(current_time.strftime("%M"))

    def random_method(self):
        """Example of random method."""
        pass   # noqa: PIE790
