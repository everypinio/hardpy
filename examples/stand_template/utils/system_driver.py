import datetime
import psutil


class SystemDriver:
    """System driver."""

    def __init__(self):
        pass

    def connect(self) -> bool:
        return True

    def disconnect(self) -> bool:
        return True

    @property
    def current_minute(self) -> int:
        """Example of driver method."""
        current_time = datetime.datetime.now()
        return int(current_time.strftime("%M"))

    @property
    def cpu_freq(self) -> float:
        return psutil.cpu_freq()
