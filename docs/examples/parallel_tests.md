# Parallel test execution  

This example demonstrates how to run multiple test processes in parallel using **HardPy**.
The implementation allows executing independent test scenarios simultaneously, which is useful for:

- Performance testing  
- Multi-stand testing environments  
- Long-running test cases that can be parallelized  

## Implementation  

The solution consists of two main components:  

### 1. Process controller (`conftest.py`)  

Manages parallel processes and collects their results:  

```python
import os
import signal
import subprocess
from datetime import datetime

import pytest
import hardpy

class ProcessController:
    """Controls parallel test processes execution"""
    
    def __init__(self) -> None:
        self.processes = {}
        self.start_times = {}
        self.end_times = {}
        self.results = {}

    def add_process(self, name: str, python_script: str):
        """Starts a new parallel process"""
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
        """Collects process output when completed"""
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
                    f"Process {name} finished (duration: {duration.total_seconds():.2f}s)"
                    f" with output: {output}"
                )
                return True
        return False

    def terminate_all(self):
        """Safely terminates all running processes"""
        for name, process in self.processes.items():
            if process.poll() is None:
                os.killpg(os.getpgid(process.pid), signal.SIGTERM)
                end_time = str(datetime.now())[:-7]
                duration = datetime.strptime(
                    end_time, "%Y-%m-%d %H:%M:%S",
                ) - datetime.strptime(self.start_times[name], "%Y-%m-%d %H:%M:%S")
                hardpy.set_message(
                    f"Process {name} terminated after {duration.total_seconds():.2f}s"
                )

@pytest.fixture(scope="session")
def process_controller():
    controller = ProcessController()
    yield controller
    controller.terminate_all()
```

### 2. Test implementation  

Example tests that launch and monitor parallel processes:  

```python
import time
from datetime import datetime
import hardpy
from conftest import ProcessController

def test_start_process_1(process_controller: ProcessController):
    """Launches first parallel process (5 sec duration)"""
    hardpy.set_message(f"Start test_start_process_1 at {str(datetime.now())[:-7]}")
    
    python_script = """
import time
import sys
time.sleep(5)
print("Result for process_1")
sys.stdout.flush()
"""
    process_controller.add_process("proc_1", python_script)
    time.sleep(1)

def test_start_process_2(process_controller: ProcessController):
    """Launches second parallel process (10 sec duration)"""
    hardpy.set_message(f"Start test_start_process_2 at {str(datetime.now())[:-7]}")
    
    python_script = """
import time
import sys
time.sleep(10)
print("Result for process_2")
sys.stdout.flush()
"""
    process_controller.add_process("proc_2", python_script)
    time.sleep(1)

def test_check_results(process_controller: ProcessController):
    """Verifies results from all parallel processes"""
    start_time = time.time()
    hardpy.set_message(f"Start results check at {str(datetime.now())[:-7]}")
    timeout = 20  # Max wait time for all processes

    while time.time() - start_time < timeout:
        # Check all processes for completion
        for name in process_controller.process_names:
            process_controller.collect_output(name)

        # Verify all results received
        if len(process_controller.results) == len(process_controller.process_names):
            expected = {
                "proc_1": "Result for process_1",
                "proc_2": "Result for process_2",
            }
            assert process_controller.results == expected
            hardpy.set_message("All processes completed successfully!")
            return

        time.sleep(0.2)

    # Timeout handling
    process_controller.terminate_all()
    raise TimeoutError(f"Timeout reached. Results: {process_controller.results}")
```
