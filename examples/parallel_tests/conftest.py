import os
import signal
import subprocess
from datetime import datetime

import pytest

import hardpy


class ProcessController:
    def __init__(self):
        self.processes = {}
        self.start_times = {}
        self.output_files = {}

    def add_process(self, name, command, output_file=None):
        if output_file is None:
            output_file = f"/tmp/{name}_output.txt"

        self.output_files[name] = output_file
        self.start_times[name] = datetime.now()

        with open(output_file, "w") as f:
            self.processes[name] = subprocess.Popen(
                command,
                stdout=f,
                stderr=subprocess.STDOUT,
                shell=True,
                preexec_fn=os.setsid,
            )

        hardpy.set_message(f"Process {name} started at {self.start_times[name]}")

    def get_result(self, name):
        if name in self.processes and self.processes[name].poll() is not None:
            end_time = datetime.now()
            duration = (end_time - self.start_times[name]).total_seconds()

            with open(self.output_files[name], "r") as f:
                result = f.read().strip()

            hardpy.set_message(
                f"Process {name} finished at {end_time}, duration: {duration:.2f}s"
            )
            hardpy.set_message(f"Process {name} output: {result}")
            return result

        return None

    def is_process_alive(self, name):
        return name in self.processes and self.processes[name].poll() is None

    def terminate_all(self):
        for name, process in self.processes.items():
            if self.is_process_alive(name):
                os.killpg(os.getpgid(process.pid), signal.SIGTERM)
                hardpy.set_message(f"Process {name} terminated")


@pytest.fixture(scope="session")
def process_controller():
    controller = ProcessController()
    yield controller
    controller.terminate_all()
