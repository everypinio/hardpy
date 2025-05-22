import os
import signal
import subprocess
from datetime import datetime

import pytest

import hardpy


class ProcessController:
    """A class used to control and manage processes."""

    def __init__(self) -> None:
        self.processes = {}
        self.start_times = {}
        self.end_times = {}
        self.results = {}

    @property
    def process_names(self):
        """Returns the names of the processes."""
        return list(self.processes.keys())

    def add_process(self, name: str, python_script: str):
        """Starts a new process."""
        self.start_times[name] = str(datetime.now())[:-7]  # noqa: DTZ005

        self.processes[name] = subprocess.Popen(  # noqa: S603
            ["python", "-c", python_script],  # noqa: S607
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            bufsize=1,
            universal_newlines=True,
            shell=False,
            start_new_session=True,
        )
        hardpy.set_message(f"Process {name} started at {self.start_times[name]}")

    def collect_output(self, name: str):
        """Collects the output of a process."""
        if name not in self.processes:
            return False

        process = self.processes[name]

        if process.poll() is not None and name not in self.results:
            self.end_times[name] = str(datetime.now())[:-7]  # noqa: DTZ005
            stdout, _ = process.communicate()
            output = stdout.strip()
            if output:
                self.results[name] = output
                duration = datetime.strptime(  # noqa: DTZ007
                    self.end_times[name], "%Y-%m-%d %H:%M:%S",
                ) - datetime.strptime(self.start_times[name], "%Y-%m-%d %H:%M:%S")  # noqa: DTZ007
                hardpy.set_message(
                    f"Process {name} finished at {self.end_times[name]} "
                    f"(duration: {duration.total_seconds():.2f}s) with output: {output}"
                )
                return True
        return False

    def is_process_alive(self, name: str):
        """Checks if a process is alive."""
        return name in self.processes and self.processes[name].poll() is None

    def terminate_all(self):
        """Terminates all processes."""
        for name, process in self.processes.items():
            if self.is_process_alive(name):
                os.killpg(os.getpgid(process.pid), signal.SIGTERM)
                end_time = str(datetime.now())[:-7]  # noqa: DTZ005
                duration = datetime.strptime(  # noqa: DTZ007
                    end_time, "%Y-%m-%d %H:%M:%S",
                ) - datetime.strptime(self.start_times[name], "%Y-%m-%d %H:%M:%S")  # noqa: DTZ007
                hardpy.set_message(
                    f"Process {name} terminated at {end_time} "
                    f"(duration: {duration.total_seconds():.2f}s)"
                )


@pytest.fixture(scope="session")
def process_controller():
    controller = ProcessController()
    yield controller
    controller.terminate_all()
