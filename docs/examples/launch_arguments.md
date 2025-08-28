# Launch arguments

**HardPy** launches pytest tests.
**HardPy** supports two methods for passing parameters to tests: the built-in start arguments functionality (recommended) and the classic pytest launch arguments approach.

## Start arguments (recommended method)

The [Start arguments](../documentation/pytest_hardpy.md#get_start_args) functionality allows you to pass dynamic parameters to your test runs using the `--arg` option (CLI) or `--hardpy-start-arg` option (pytest).
This is particularly useful for configuring tests at runtime without changing the code.

Contains examples of how to use dynamic start arguments in tests.

### how to start

1. Launch `hardpy init start_arguments`.
2. Launch [CouchDB instance](../documentation/database.md#couchdb-instance).
3. Modify the files described below.
4. Launch tests with dynamic arguments:

    ```bash
    hardpy run start_arguments

    # Using hardpy command
    hardpy start start_arguments --arg test_mode=debug --arg device_id=DUT-007 --arg retry_count=3

    # Or using pytest directly
    pytest --hardpy-start-arg test_mode=debug --hardpy-start-arg device_id=DUT-007 --hardpy-start-arg retry_count=3
    ```

    Alternatively, you can specify start arguments in the `pytest.ini` file.
    This is useful for setting default arguments that are always used when running tests.

    ```pytest
    [pytest]
    addopts = --hardpy-pt
            --hardpy-db-url http://dev:dev@localhost:5984/
            --hardpy-start-arg test_mode=debug
            --hardpy-start-arg device_id=DUT-007
            --hardpy-start-arg retry_count=3
    ```

### test_1.py

```python
import pytest
import hardpy

def test_with_start_args():
    start_args = hardpy.get_start_args()
    
    if start_args.get("test_mode") == "debug":
        hardpy.set_message("Running in debug mode")
    
    device_id = start_args.get("device_id")
    if device_id:
        hardpy.set_message(f"Testing device: {device_id}")
        hardpy.set_case_artifact({"device_id": device_id})
    else:
        hardpy.set_message("No device ID provided")
    
    retry_count = start_args.get("retry_count")
    if retry_count:
        hardpy.set_message(f"Retry count: {retry_count}")
    else:
        hardpy.set_message("Retry count not set")

def test_conditional_behavior():
    args = hardpy.get_start_args()
    
    if args.get("test_mode") != "debug":
        pytest.skip("This test runs only in debug mode")
    
    hardpy.set_message("Running debug-specific test")
    assert True, "Debug test passed"

def test_parameterized_assertions():
    args = hardpy.get_start_args()
    expected_value = args.get("expected_value", "default")
    
    actual_value = "default"
    assert actual_value == expected_value, f"Expected {expected_value}, got {actual_value}"
    
    hardpy.set_message(f"Verified value: {actual_value}")
```

## Addoption

Alternative approach using pytest's built-in `addoption` method for adding custom options.
You can read more about it [here](https://docs.pytest.org/en/stable/example/simple.html#how-to-change-command-line-options-defaults).

### how to start

1. Launch `hardpy init launch_arg`.
2. Launch [CouchDB instance](../documentation/database.md#couchdb-instance).
3. Modify the files described below.
4. Launch `hardpy run launch_arg`.

### conftest.py

```python
def pytest_addoption(parser):
    parser.addoption("--my-opt", action="store", help="add my opt")

@pytest.fixture(scope="session")
def my_opt(request):
    return request.config.getoption("--my-opt")
```

### test_1.py

```python
def test_custom_option_1(request):
    custom_value = request.config.getoption("--my-opt")
    print(f"Custom option value: {custom_value}")
    assert custom_value == "hello"

def test_custom_option_2(my_opt):
    print(f"Custom option value: {my_opt}")
    assert my_opt == "hello"
```

### launch test with your parameter

You can launch tests with this command:

```
pytest --my-opt hello
```

Alternatively, you can add the parameter `--my-opt hello` to the `pytest.ini` file.
