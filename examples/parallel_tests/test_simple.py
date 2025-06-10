import time
from datetime import datetime

import hardpy
from examples.parallel_tests.conftest import ProcessController


def test_start_process_1(process_controller: ProcessController):
    hardpy.set_message(f"Start test_start_process_1 at {str(datetime.now())[:-7]}")  # noqa: DTZ005
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
    hardpy.set_message(f"Start test_start_process_2 at {str(datetime.now())[:-7]}")  # noqa: DTZ005
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
    start_time = time.time()
    hardpy.set_message(f"Start test_check_results at {str(datetime.now())[:-7]}")  # noqa: DTZ005
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
