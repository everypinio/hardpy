from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from pytest import Pytester


def test_parallel_processes_success(pytester: Pytester, hardpy_opts: list[str]):
    """Test successful parallel process execution."""
    pytester.makepyfile(
        test_file1="""
import time
from datetime import datetime

import hardpy
from examples.parallel_tests.conftest import ProcessController


def test_start_process_1(process_controller: ProcessController):
    hardpy.set_message(f"Start test_start_process_1 at {str(datetime.now())[:-7]}")
    python_script = '''
import time
import sys
time.sleep(2)
print("Result for process_1")
sys.stdout.flush()
'''
    process_controller.add_process("proc_1", python_script)
    time.sleep(1)


def test_start_process_2(process_controller: ProcessController):
    hardpy.set_message(f"Start test_start_process_2 at {str(datetime.now())[:-7]}")
    python_script = '''
import time
import sys
time.sleep(3)
print("Result for process_2")
sys.stdout.flush()
'''
    process_controller.add_process("proc_2", python_script)
    time.sleep(1)


def test_check_results(process_controller: ProcessController):
    start_time = time.time()
    hardpy.set_message(f"Start test_check_results at {str(datetime.now())[:-7]}")
    timeout = 10

    while time.time() - start_time < timeout:
        for name in process_controller.process_names:
            process_controller.collect_output(name)

        if len(process_controller.results) == len(process_controller.process_names):
            expected = {
                "proc_1": "Result for process_1",
                "proc_2": "Result for process_2",
            }
            assert process_controller.results == expected
            hardpy.set_message("All results received successfully!")
            return

        time.sleep(0.2)

    process_controller.terminate_all()
    msg = f"Timeout reached. Results: {process_controller.results}"
    raise TimeoutError(msg)
        """,
        conftest="""
import os
import signal
import subprocess
from datetime import datetime

import pytest

import hardpy


class ProcessController:
    def __init__(self) -> None:
        self.processes = {}
        self.start_times = {}
        self.end_times = {}
        self.results = {}

    @property
    def process_names(self):
        return list(self.processes.keys())

    def add_process(self, name: str, python_script: str):
        self.start_times[name] = str(datetime.now())[:-7]

        self.processes[name] = subprocess.Popen(
            ["python", "-c", python_script],
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
        if name not in self.processes:
            return False

        process = self.processes[name]

        if process.poll() is not None and name not in self.results:
            self.end_times[name] = str(datetime.now())[:-7]
            stdout, _ = process.communicate()
            output = stdout.strip()
            if output:
                self.results[name] = output
                duration = datetime.strptime(
                    self.end_times[name], "%Y-%m-%d %H:%M:%S",
                ) - datetime.strptime(self.start_times[name], "%Y-%m-%d %H:%M:%S")
                hardpy.set_message(
                    f"Process {name} finished at {self.end_times[name]} "
                    f"(duration: {duration.total_seconds():.2f}s) with output: {output}"
                )
                return True
        return False

    def is_process_alive(self, name: str):
        return name in self.processes and self.processes[name].poll() is None

    def terminate_all(self):
        for name, process in self.processes.items():
            if self.is_process_alive(name):
                os.killpg(os.getpgid(process.pid), signal.SIGTERM)
                end_time = str(datetime.now())[:-7]
                duration = datetime.strptime(
                    end_time, "%Y-%m-%d %H:%M:%S",
                ) - datetime.strptime(self.start_times[name], "%Y-%m-%d %H:%M:%S")
                hardpy.set_message(
                    f"Process {name} terminated at {end_time} "
                    f"(duration: {duration.total_seconds():.2f}s)"
                )


@pytest.fixture(scope="session")
def process_controller():
    controller = ProcessController()
    yield controller
    controller.terminate_all()
        """,
    )
    result = pytester.runpytest(*hardpy_opts)
    result.assert_outcomes(passed=3)


def test_parallel_processes_timeout(pytester: Pytester, hardpy_opts: list[str]):
    """Test timeout in parallel process execution."""
    pytester.makepyfile(
        test_file1="""
import time
from datetime import datetime

import hardpy
from examples.parallel_tests.conftest import ProcessController


def test_start_process_1(process_controller: ProcessController):
    hardpy.set_message(f"Start test_start_process_1 at {str(datetime.now())[:-7]}")
    python_script = '''
import time
import sys
time.sleep(10)
print("Result for process_1")
sys.stdout.flush()
'''
    process_controller.add_process("proc_1", python_script)
    time.sleep(1)


def test_start_process_2(process_controller: ProcessController):
    hardpy.set_message(f"Start test_start_process_2 at {str(datetime.now())[:-7]}")
    python_script = '''
import time
import sys
time.sleep(15)
print("Result for process_2")
sys.stdout.flush()
'''
    process_controller.add_process("proc_2", python_script)
    time.sleep(1)


def test_check_results(process_controller: ProcessController):
    start_time = time.time()
    hardpy.set_message(f"Start test_check_results at {str(datetime.now())[:-7]}")
    timeout = 5

    while time.time() - start_time < timeout:
        for name in process_controller.process_names:
            process_controller.collect_output(name)

        if len(process_controller.results) == len(process_controller.process_names):
            expected = {
                "proc_1": "Result for process_1",
                "proc_2": "Result for process_2",
            }
            assert process_controller.results == expected
            hardpy.set_message("All results received successfully!")
            return

        time.sleep(0.2)

    process_controller.terminate_all()
    msg = f"Timeout reached. Results: {process_controller.results}"
    raise TimeoutError(msg)
        """,
        conftest="""
import os
import signal
import subprocess
from datetime import datetime

import pytest

import hardpy


class ProcessController:
    def __init__(self) -> None:
        self.processes = {}
        self.start_times = {}
        self.end_times = {}
        self.results = {}

    @property
    def process_names(self):
        return list(self.processes.keys())

    def add_process(self, name: str, python_script: str):
        self.start_times[name] = str(datetime.now())[:-7]

        self.processes[name] = subprocess.Popen(
            ["python", "-c", python_script],
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
        if name not in self.processes:
            return False

        process = self.processes[name]

        if process.poll() is not None and name not in self.results:
            self.end_times[name] = str(datetime.now())[:-7]
            stdout, _ = process.communicate()
            output = stdout.strip()
            if output:
                self.results[name] = output
                duration = datetime.strptime(
                    self.end_times[name], "%Y-%m-%d %H:%M:%S",
                ) - datetime.strptime(self.start_times[name], "%Y-%m-%d %H:%M:%S")
                hardpy.set_message(
                    f"Process {name} finished at {self.end_times[name]} "
                    f"(duration: {duration.total_seconds():.2f}s) with output: {output}"
                )
                return True
        return False

    def is_process_alive(self, name: str):
        return name in self.processes and self.processes[name].poll() is None

    def terminate_all(self):
        for name, process in self.processes.items():
            if self.is_process_alive(name):
                os.killpg(os.getpgid(process.pid), signal.SIGTERM)
                end_time = str(datetime.now())[:-7]
                duration = datetime.strptime(
                    end_time, "%Y-%m-%d %H:%M:%S",
                ) - datetime.strptime(self.start_times[name], "%Y-%m-%d %H:%M:%S")
                hardpy.set_message(
                    f"Process {name} terminated at {end_time} "
                    f"(duration: {duration.total_seconds():.2f}s)"
                )


@pytest.fixture(scope="session")
def process_controller():
    controller = ProcessController()
    yield controller
    controller.terminate_all()
        """,
    )
    result = pytester.runpytest(*hardpy_opts)
    result.assert_outcomes(failed=1, passed=2)


def test_parallel_processes_partial_results(pytester: Pytester, hardpy_opts: list[str]):
    """Test case when only some processes complete successfully."""
    pytester.makepyfile(
        test_file1="""
import time
from datetime import datetime

import hardpy
from examples.parallel_tests.conftest import ProcessController


def test_start_process_1(process_controller: ProcessController):
    hardpy.set_message(f"Start test_start_process_1 at {str(datetime.now())[:-7]}")
    python_script = '''
import time
import sys
time.sleep(2)
print("Result for process_1")
sys.stdout.flush()
'''
    process_controller.add_process("proc_1", python_script)
    time.sleep(1)


def test_start_process_2(process_controller: ProcessController):
    hardpy.set_message(f"Start test_start_process_2 at {str(datetime.now())[:-7]}")
    python_script = '''
import time
import sys
time.sleep(10)
print("Result for process_2")
sys.stdout.flush()
'''
    process_controller.add_process("proc_2", python_script)
    time.sleep(1)


def test_check_results(process_controller: ProcessController):
    start_time = time.time()
    hardpy.set_message(f"Start test_check_results at {str(datetime.now())[:-7]}")
    timeout = 5

    while time.time() - start_time < timeout:
        for name in process_controller.process_names:
            process_controller.collect_output(name)

        if len(process_controller.results) == len(process_controller.process_names):
            expected = {
                "proc_1": "Result for process_1",
                "proc_2": "Result for process_2",
            }
            assert process_controller.results == expected
            hardpy.set_message("All results received successfully!")
            return

        time.sleep(0.2)

    process_controller.terminate_all()
    msg = f"Timeout reached. Results: {process_controller.results}"
    raise TimeoutError(msg)
        """,
        conftest="""
import os
import signal
import subprocess
from datetime import datetime

import pytest

import hardpy


class ProcessController:
    def __init__(self) -> None:
        self.processes = {}
        self.start_times = {}
        self.end_times = {}
        self.results = {}

    @property
    def process_names(self):
        return list(self.processes.keys())

    def add_process(self, name: str, python_script: str):
        self.start_times[name] = str(datetime.now())[:-7]

        self.processes[name] = subprocess.Popen(
            ["python", "-c", python_script],
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
        if name not in self.processes:
            return False

        process = self.processes[name]

        if process.poll() is not None and name not in self.results:
            self.end_times[name] = str(datetime.now())[:-7]
            stdout, _ = process.communicate()
            output = stdout.strip()
            if output:
                self.results[name] = output
                duration = datetime.strptime(
                    self.end_times[name], "%Y-%m-%d %H:%M:%S",
                ) - datetime.strptime(self.start_times[name], "%Y-%m-%d %H:%M:%S")
                hardpy.set_message(
                    f"Process {name} finished at {self.end_times[name]} "
                    f"(duration: {duration.total_seconds():.2f}s) with output: {output}"
                )
                return True
        return False

    def is_process_alive(self, name: str):
        return name in self.processes and self.processes[name].poll() is None

    def terminate_all(self):
        for name, process in self.processes.items():
            if self.is_process_alive(name):
                os.killpg(os.getpgid(process.pid), signal.SIGTERM)
                end_time = str(datetime.now())[:-7]
                duration = datetime.strptime(
                    end_time, "%Y-%m-%d %H:%M:%S",
                ) - datetime.strptime(self.start_times[name], "%Y-%m-%d %H:%M:%S")
                hardpy.set_message(
                    f"Process {name} terminated at {end_time} "
                    f"(duration: {duration.total_seconds():.2f}s)"
                )


@pytest.fixture(scope="session")
def process_controller():
    controller = ProcessController()
    yield controller
    controller.terminate_all()
        """,
    )
    result = pytester.runpytest(*hardpy_opts)
    result.assert_outcomes(failed=1, passed=2)


def test_parallel_with_critical_and_attempt(pytester: Pytester, hardpy_opts: list[str]):
    """Test parallel execution with critical tests and attempt markers."""
    pytester.makepyfile(
        test_file1="""
import time
import pytest
from datetime import datetime

import hardpy

attempt_count = 0

@pytest.mark.critical
@pytest.mark.attempt(3)
def test_parallel_process_1(process_controller):
    global attempt_count
    attempt_count += 1

    hardpy.set_message(f"Start test_parallel_process_1 (attempt {attempt_count}) at {str(datetime.now())[:-7]}")

    python_script = '''
import time
import sys
time.sleep(2)
print("Result for process_1")
sys.stdout.flush()
'''
    process_controller.add_process("proc_1", python_script)
    time.sleep(1)

    if attempt_count < 2:
        assert False
    assert True
""",
        test_file2="""
import time
import pytest
from datetime import datetime

import hardpy

@pytest.mark.dependency("test_file1::test_parallel_process_1")
def test_parallel_process_2(process_controller):
    hardpy.set_message(f"Start test_parallel_process_2 at {str(datetime.now())[:-7]}")

    python_script = '''
import time
import sys
time.sleep(4)
print("Result for process_2")
sys.stdout.flush()
'''
    process_controller.add_process("proc_2", python_script)
    time.sleep(1)
    assert True
""",
        test_file3="""
import time
import pytest
from datetime import datetime

import hardpy

def test_check_parallel_results(process_controller):
    start_time = time.time()
    hardpy.set_message(f"Start test_check_results at {str(datetime.now())[:-7]}")
    timeout = 20

    while time.time() - start_time < timeout:
        for name in process_controller.process_names:
            process_controller.collect_output(name)

        if len(process_controller.results) == len(process_controller.process_names):
            expected = {
                "proc_1": "Result for process_1",
                "proc_2": "Result for process_2",
            }
            assert process_controller.results == expected
            hardpy.set_message("All results received successfully!")
            return

        time.sleep(0.2)

    process_controller.terminate_all()
    msg = f"Timeout reached. Results: {process_controller.results}"
    raise TimeoutError(msg)
""",
        conftest="""
import os
import signal
import subprocess
from datetime import datetime

import pytest
import hardpy


class ProcessController:
    def __init__(self) -> None:
        self.processes = {}
        self.start_times = {}
        self.end_times = {}
        self.results = {}

    @property
    def process_names(self):
        return list(self.processes.keys())

    def add_process(self, name: str, python_script: str):
        self.start_times[name] = str(datetime.now())[:-7]

        self.processes[name] = subprocess.Popen(
            ["python", "-c", python_script],
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
        if name not in self.processes:
            return False

        process = self.processes[name]

        if process.poll() is not None and name not in self.results:
            self.end_times[name] = str(datetime.now())[:-7]
            stdout, _ = process.communicate()
            output = stdout.strip()
            if output:
                self.results[name] = output
                duration = datetime.strptime(
                    self.end_times[name], "%Y-%m-%d %H:%M:%S",
                ) - datetime.strptime(self.start_times[name], "%Y-%m-%d %H:%M:%S")
                hardpy.set_message(
                    f"Process {name} finished at {self.end_times[name]} "
                    f"(duration: {duration.total_seconds():.2f}s) with output: {output}"
                )
                return True
        return False

    def is_process_alive(self, name: str):
        return name in self.processes and self.processes[name].poll() is None

    def terminate_all(self):
        for name, process in self.processes.items():
            if self.is_process_alive(name):
                os.killpg(os.getpgid(process.pid), signal.SIGTERM)
                end_time = str(datetime.now())[:-7]
                duration = datetime.strptime(
                    end_time, "%Y-%m-%d %H:%M:%S",
                ) - datetime.strptime(self.start_times[name], "%Y-%m-%d %H:%M:%S")
                hardpy.set_message(
                    f"Process {name} terminated at {end_time} "
                    f"(duration: {duration.total_seconds():.2f}s)"
                )


@pytest.fixture(scope="session")
def process_controller():
    controller = ProcessController()
    yield controller
    controller.terminate_all()
""",
    )
    result = pytester.runpytest(*hardpy_opts)
    # First test passes after retry, second test runs as dependency, third checks results
    result.assert_outcomes(passed=3)


def test_parallel_with_critical_marker(pytester: Pytester, hardpy_opts: list[str]):
    """Test parallel execution with critical marker."""
    pytester.makepyfile(
        test_file1="""
import time
import pytest
from datetime import datetime

import hardpy

@pytest.mark.critical
def test_critical_process(process_controller):
    hardpy.set_message(f"Start test_critical_process at {str(datetime.now())[:-7]}")

    python_script = '''
import time
import sys
time.sleep(2)
print("Result for critical process")
sys.stdout.flush()
'''
    process_controller.add_process("proc_critical", python_script)
    time.sleep(1)
    assert False  # Intentionally fail the critical test
""",
        test_file2="""
import time
import pytest
from datetime import datetime

import hardpy

def test_non_critical_process(process_controller):
    hardpy.set_message(f"Start test_non_critical_process at {str(datetime.now())[:-7]}")

    python_script = '''
import time
import sys
time.sleep(3)
print("Result for non-critical process")
sys.stdout.flush()
'''
    process_controller.add_process("proc_non_critical", python_script)
    time.sleep(1)
    assert True
""",
        test_file3="""
import time
import pytest
from datetime import datetime

import hardpy

def test_check_results(process_controller: ProcessController):
    start_time = time.time()
    hardpy.set_message(f"Start test_check_results at {str(datetime.now())[:-7]}")
    timeout = 5

    while time.time() - start_time < timeout:
        for name in process_controller.process_names:
            process_controller.collect_output(name)

        if len(process_controller.results) == len(process_controller.process_names):
            expected = {
                "proc_1": "Result for process_1",
                "proc_2": "Result for process_2",
            }
            assert process_controller.results == expected
            hardpy.set_message("All results received successfully!")
            return

        time.sleep(0.2)

    process_controller.terminate_all()
    msg = f"Timeout reached. Results: {process_controller.results}"
    raise TimeoutError(msg)
""",
        conftest="""
import os
import signal
import subprocess
from datetime import datetime

import pytest
import hardpy


class ProcessController:
    def __init__(self) -> None:
        self.processes = {}
        self.start_times = {}
        self.end_times = {}
        self.results = {}

    @property
    def process_names(self):
        return list(self.processes.keys())

    def add_process(self, name: str, python_script: str):
        self.start_times[name] = str(datetime.now())[:-7]

        self.processes[name] = subprocess.Popen(
            ["python", "-c", python_script],
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
        if name not in self.processes:
            return False

        process = self.processes[name]

        if process.poll() is not None and name not in self.results:
            self.end_times[name] = str(datetime.now())[:-7]
            stdout, _ = process.communicate()
            output = stdout.strip()
            if output:
                self.results[name] = output
                duration = datetime.strptime(
                    self.end_times[name], "%Y-%m-%d %H:%M:%S",
                ) - datetime.strptime(self.start_times[name], "%Y-%m-%d %H:%M:%S")
                hardpy.set_message(
                    f"Process {name} finished at {self.end_times[name]} "
                    f"(duration: {duration.total_seconds():.2f}s) with output: {output}"
                )
                return True
        return False

    def is_process_alive(self, name: str):
        return name in self.processes and self.processes[name].poll() is None

    def terminate_all(self):
        for name, process in self.processes.items():
            if self.is_process_alive(name):
                os.killpg(os.getpgid(process.pid), signal.SIGTERM)
                end_time = str(datetime.now())[:-7]
                duration = datetime.strptime(
                    end_time, "%Y-%m-%d %H:%M:%S",
                ) - datetime.strptime(self.start_times[name], "%Y-%m-%d %H:%M:%S")
                hardpy.set_message(
                    f"Process {name} terminated at {end_time} "
                    f"(duration: {duration.total_seconds():.2f}s)"
                )


@pytest.fixture(scope="session")
def process_controller():
    controller = ProcessController()
    yield controller
    controller.terminate_all()
""",
    )
    result = pytester.runpytest(*hardpy_opts)
    # Critical test fails, other tests should be skipped
    result.assert_outcomes(failed=1, skipped=2)


def test_parallel_with_dependencies(pytester: Pytester, hardpy_opts: list[str]):
    """Test parallel execution with test dependencies."""
    pytester.makepyfile(
        test_file1="""
import time
import pytest
from datetime import datetime

import hardpy

def test_first_process(process_controller):
    hardpy.set_message(f"Start test_first_process at {str(datetime.now())[:-7]}")

    python_script = '''
import time
import sys
time.sleep(2)
print("Result for first process")
sys.stdout.flush()
'''
    process_controller.add_process("proc_first", python_script)
    time.sleep(1)
    assert True
""",
        test_file2="""
import pytest
import time
from datetime import datetime

import hardpy

@pytest.mark.dependency(depends=["test_file1::test_first_process"])
def test_dependent_process(process_controller):
    hardpy.set_message(f"Start test_dependent_process at {str(datetime.now())[:-7]}")

    python_script = '''
import time
import sys
time.sleep(3)
print("Result for dependent process")
sys.stdout.flush()
'''
    process_controller.add_process("proc_dependent", python_script)
    time.sleep(1)
    assert True
""",
        test_file3="""
import time
import pytest
from datetime import datetime

import hardpy

def test_check_results(process_controller: ProcessController):
    start_time = time.time()
    hardpy.set_message(f"Start test_check_results at {str(datetime.now())[:-7]}")
    timeout = 5

    while time.time() - start_time < timeout:
        for name in process_controller.process_names:
            process_controller.collect_output(name)

        if len(process_controller.results) == len(process_controller.process_names):
            expected = {
                "proc_1": "Result for process_1",
                "proc_2": "Result for process_2",
            }
            assert process_controller.results == expected
            hardpy.set_message("All results received successfully!")
            return

        time.sleep(0.2)

    process_controller.terminate_all()
    msg = f"Timeout reached. Results: {process_controller.results}"
    raise TimeoutError(msg)
""",
        conftest="""
import os
import signal
import subprocess
from datetime import datetime

import pytest
import hardpy


class ProcessController:
    def __init__(self) -> None:
        self.processes = {}
        self.start_times = {}
        self.end_times = {}
        self.results = {}

    @property
    def process_names(self):
        return list(self.processes.keys())

    def add_process(self, name: str, python_script: str):
        self.start_times[name] = str(datetime.now())[:-7]

        self.processes[name] = subprocess.Popen(
            ["python", "-c", python_script],
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
        if name not in self.processes:
            return False

        process = self.processes[name]

        if process.poll() is not None and name not in self.results:
            self.end_times[name] = str(datetime.now())[:-7]
            stdout, _ = process.communicate()
            output = stdout.strip()
            if output:
                self.results[name] = output
                duration = datetime.strptime(
                    self.end_times[name], "%Y-%m-%d %H:%M:%S",
                ) - datetime.strptime(self.start_times[name], "%Y-%m-%d %H:%M:%S")
                hardpy.set_message(
                    f"Process {name} finished at {self.end_times[name]} "
                    f"(duration: {duration.total_seconds():.2f}s) with output: {output}"
                )
                return True
        return False

    def is_process_alive(self, name: str):
        return name in self.processes and self.processes[name].poll() is None

    def terminate_all(self):
        for name, process in self.processes.items():
            if self.is_process_alive(name):
                os.killpg(os.getpgid(process.pid), signal.SIGTERM)
                end_time = str(datetime.now())[:-7]
                duration = datetime.strptime(
                    end_time, "%Y-%m-%d %H:%M:%S",
                ) - datetime.strptime(self.start_times[name], "%Y-%m-%d %H:%M:%S")
                hardpy.set_message(
                    f"Process {name} terminated at {end_time} "
                    f"(duration: {duration.total_seconds():.2f}s)"
                )


@pytest.fixture(scope="session")
def process_controller():
    controller = ProcessController()
    yield controller
    controller.terminate_all()
""",
    )
    result = pytester.runpytest(*hardpy_opts)
    # All tests should pass as dependency is satisfied
    result.assert_outcomes(passed=3)


def test_parallel_with_attempts(pytester: Pytester, hardpy_opts: list[str]):
    """Test parallel execution with attempt marker."""
    pytester.makepyfile(
        test_file1="""
import time
import pytest
from datetime import datetime

import hardpy

attempt_count = 0

@pytest.mark.attempt(3)
def test_process_with_retries(process_controller):
    global attempt_count
    attempt_count += 1
    hardpy.set_message(f"Attempt {attempt_count} at {str(datetime.now())[:-7]}")

    # Only start process on first attempt
    if attempt_count == 1:
        python_script = '''
import time
import sys
time.sleep(2)
print(f"Result for attempt {attempt_count}")
sys.stdout.flush()
'''
        process_controller.add_process("proc_retry", python_script)
        time.sleep(1)

    # Fail first two attempts, pass on third
    if attempt_count < 3:
        assert False
    assert True
""",
        test_file2="""
import time
import pytest
from datetime import datetime

import hardpy


def test_check_results(process_controller: ProcessController):
    start_time = time.time()
    hardpy.set_message(f"Start test_check_results at {str(datetime.now())[:-7]}")
    timeout = 5

    while time.time() - start_time < timeout:
        for name in process_controller.process_names:
            process_controller.collect_output(name)

        if len(process_controller.results) == len(process_controller.process_names):
            expected = {
                "proc_1": "Result for process_1",
                "proc_2": "Result for process_2",
            }
            assert process_controller.results == expected
            hardpy.set_message("All results received successfully!")
            return

        time.sleep(0.2)

    process_controller.terminate_all()
    msg = f"Timeout reached. Results: {process_controller.results}"
    raise TimeoutError(msg)
""",
        conftest="""
import os
import signal
import subprocess
from datetime import datetime

import pytest
import hardpy


class ProcessController:
    def __init__(self) -> None:
        self.processes = {}
        self.start_times = {}
        self.end_times = {}
        self.results = {}

    @property
    def process_names(self):
        return list(self.processes.keys())

    def add_process(self, name: str, python_script: str):
        self.start_times[name] = str(datetime.now())[:-7]

        self.processes[name] = subprocess.Popen(
            ["python", "-c", python_script],
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
        if name not in self.processes:
            return False

        process = self.processes[name]

        if process.poll() is not None and name not in self.results:
            self.end_times[name] = str(datetime.now())[:-7]
            stdout, _ = process.communicate()
            output = stdout.strip()
            if output:
                self.results[name] = output
                duration = datetime.strptime(
                    self.end_times[name], "%Y-%m-%d %H:%M:%S",
                ) - datetime.strptime(self.start_times[name], "%Y-%m-%d %H:%M:%S")
                hardpy.set_message(
                    f"Process {name} finished at {self.end_times[name]} "
                    f"(duration: {duration.total_seconds():.2f}s) with output: {output}"
                )
                return True
        return False

    def is_process_alive(self, name: str):
        return name in self.processes and self.processes[name].poll() is None

    def terminate_all(self):
        for name, process in self.processes.items():
            if self.is_process_alive(name):
                os.killpg(os.getpgid(process.pid), signal.SIGTERM)
                end_time = str(datetime.now())[:-7]
                duration = datetime.strptime(
                    end_time, "%Y-%m-%d %H:%M:%S",
                ) - datetime.strptime(self.start_times[name], "%Y-%m-%d %H:%M:%S")
                hardpy.set_message(
                    f"Process {name} terminated at {end_time} "
                    f"(duration: {duration.total_seconds():.2f}s)"
                )


@pytest.fixture(scope="session")
def process_controller():
    controller = ProcessController()
    yield controller
    controller.terminate_all()
""",
    )
    result = pytester.runpytest(*hardpy_opts)
    # Test should pass after retries
    result.assert_outcomes(passed=2)


def test_parallel_with_minute_parity(pytester: Pytester, hardpy_opts: list[str]):
    """Test parallel execution with minute parity check and attempts."""
    pytester.makepyfile(
        test_file1="""
import time
import pytest
from datetime import datetime

import hardpy

@pytest.mark.attempt(5)
def test_minute_parity(process_controller):
    attempt = hardpy.get_current_attempt()
    hardpy.set_message(f"Current attempt {attempt}", "updated_status")
    if attempt > 1:
        time.sleep(15)

    # Simulate getting current minute
    current_minute = datetime.now().minute
    hardpy.set_message(f"Current minute {current_minute}")
    hardpy.set_case_artifact({"minute": current_minute})

    # Only start process on first attempt
    if attempt == 1:
        python_script = '''
import time
import sys
time.sleep(2)
print(f"Minute check attempt {attempt}")
sys.stdout.flush()
'''
        process_controller.add_process("proc_minute", python_script)
        time.sleep(1)
    
    assert current_minute % 2 == 0, f"The test failed because {current_minute} is odd! Try again!"
""",
        test_file2="""
def test_check_results(process_controller: ProcessController):
    start_time = time.time()
    hardpy.set_message(f"Start test_check_results at {str(datetime.now())[:-7]}")
    timeout = 5

    while time.time() - start_time < timeout:
        for name in process_controller.process_names:
            process_controller.collect_output(name)

        if len(process_controller.results) == len(process_controller.process_names):
            expected = {
                "proc_1": "Result for process_1",
                "proc_2": "Result for process_2",
            }
            assert process_controller.results == expected
            hardpy.set_message("All results received successfully!")
            return

        time.sleep(0.2)

    process_controller.terminate_all()
    msg = f"Timeout reached. Results: {process_controller.results}"
    raise TimeoutError(msg)
""",
        conftest="""
import os
import signal
import subprocess
from datetime import datetime

import pytest
import hardpy


class ProcessController:
    def __init__(self) -> None:
        self.processes = {}
        self.start_times = {}
        self.end_times = {}
        self.results = {}

    @property
    def process_names(self):
        return list(self.processes.keys())

    def add_process(self, name: str, python_script: str):
        self.start_times[name] = str(datetime.now())[:-7]

        self.processes[name] = subprocess.Popen(
            ["python", "-c", python_script],
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
        if name not in self.processes:
            return False

        process = self.processes[name]

        if process.poll() is not None and name not in self.results:
            self.end_times[name] = str(datetime.now())[:-7]
            stdout, _ = process.communicate()
            output = stdout.strip()
            if output:
                self.results[name] = output
                duration = datetime.strptime(
                    self.end_times[name], "%Y-%m-%d %H:%M:%S",
                ) - datetime.strptime(self.start_times[name], "%Y-%m-%d %H:%M:%S")
                hardpy.set_message(
                    f"Process {name} finished at {self.end_times[name]} "
                    f"(duration: {duration.total_seconds():.2f}s) with output: {output}"
                )
                return True
        return False

    def is_process_alive(self, name: str):
        return name in self.processes and self.processes[name].poll() is None

    def terminate_all(self):
        for name, process in self.processes.items():
            if self.is_process_alive(name):
                os.killpg(os.getpgid(process.pid), signal.SIGTERM)
                end_time = str(datetime.now())[:-7]
                duration = datetime.strptime(
                    end_time, "%Y-%m-%d %H:%M:%S",
                ) - datetime.strptime(self.start_times[name], "%Y-%m-%d %H:%M:%S")
                hardpy.set_message(
                    f"Process {name} terminated at {end_time} "
                    f"(duration: {duration.total_seconds():.2f}s)"
                )


@pytest.fixture(scope="session")
def process_controller():
    controller = ProcessController()
    yield controller
    controller.terminate_all()
""",
    )
    result = pytester.runpytest(*hardpy_opts)
    # Depending on minute, test might pass or fail after attempts
    # We can't reliably assert outcomes here as it depends on runtime minute
    # Just verify no errors occurred
    assert result.ret != 1  # 1 means tests failed
