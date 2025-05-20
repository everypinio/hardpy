import time
from datetime import datetime

import hardpy


def test_start_process_1(process_controller):
    test_start = datetime.now()
    time.sleep(8)
    hardpy.set_message(f"Test test_start_process_1 started at {test_start}")

    process_controller.add_process("proc_1", 'sleep 5; echo "Result for process_1"')

    test_end = datetime.now()
    hardpy.set_message(
        f"Test test_start_process_1 finished at {test_end}, duration: {(test_end-test_start).total_seconds():.2f}s"
    )


def test_start_process_2(process_controller):
    test_start = datetime.now()
    time.sleep(6)
    hardpy.set_message(f"Test test_start_process_2 started at {test_start}")

    process_controller.add_process("proc_2", 'sleep 7; echo "Result for process_2"')

    test_end = datetime.now()
    hardpy.set_message(
        f"Test test_start_process_2 finished at {test_end}, duration: {(test_end-test_start).total_seconds():.2f}s"
    )


def test_check_results(process_controller):
    test_start = datetime.now()
    hardpy.set_message(f"Test test_check_results started at {test_start}")

    timeout = 20
    start_time = time.time()

    while True:
        results = []
        for name in ["proc_1", "proc_2"]:
            if not process_controller.is_process_alive(name):
                result = process_controller.get_result(name)
                if result and "Result for" in result:
                    results.append(
                        result.splitlines()[-1]
                    )

        if len(results) == 2:
            assert sorted(results) == sorted(
                ["Result for process_1", "Result for process_2"]
            )
            break

        if time.time() - start_time > timeout:
            process_controller.terminate_all()
            msg = f"Processes didn't finish in time. Current results: {results}"
            raise TimeoutError(msg)

        time.sleep(0.5)

    test_end = datetime.now()
    hardpy.set_message(
        f"Test test_check_results finished at {test_end}, duration: {(test_end-test_start).total_seconds():.2f}s"
    )
