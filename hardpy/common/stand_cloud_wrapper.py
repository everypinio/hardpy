# Copyright (c) 2025 Everypin
# GNU General Public License v3.0 (see LICENSE or https://www.gnu.org/licenses/gpl-3.0.txt)

from time import sleep

from hardpy.pytest_hardpy.db import DatabaseField as DF  # noqa: N817
from hardpy.pytest_hardpy.reporter import RunnerReporter


class StandCloudWrapper:
    """Stub for operator panel debug."""

    def __init__(self) -> None:
        pass

    def register(self) -> bool:
        """Register to StandCloud.

        Returns:
            bool: True if successful
        """
        reporter = RunnerReporter()
        key = reporter.generate_key(DF.STAND_CLOUD, DF.MSG)
        reporter.set_doc_value(key, "https://standcloud.io/", statestore_only=True)
        reporter.update_db_by_doc()

        return True

    def check_connection(self) -> bool:
        """Check connection to StandCloud.

        Returns:
            bool: True if successful
        """
        sleep(1)

        reporter = RunnerReporter()
        key = reporter.generate_key(DF.STAND_CLOUD, DF.MSG)
        reporter.set_doc_value(key, "Connection STUB", statestore_only=True)
        reporter.update_db_by_doc()
        return True

    def close_window(self) -> bool:
        """Close StandCLoud dialog box window.

        Returns:
            bool: True if successful
        """
        reporter = RunnerReporter()
        key = reporter.generate_key(DF.STAND_CLOUD, DF.MSG)
        reporter.set_doc_value(key, {}, statestore_only=True)
        reporter.update_db_by_doc()
        return True
