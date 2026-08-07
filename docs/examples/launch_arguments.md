# Launch arguments

**Jig** launches pytest tests.
Jig supports two methods for passing parameters to tests. 
The recommended method is the [start arguments](./../documentation/cli.md#jig-start) functionality.
The other method is writing your own [addoption](#addoption) pytest approach.

## Start arguments

The [jig_start_args](../documentation/pytest_jig.md#jig_start_args) 
fixture allows you to pass dynamic parameters to your test runs using the `--arg` 
option (CLI) or [--jig-start-arg](./../documentation/pytest_jig.md#jig-start-arg) option (pytest).
This is particularly useful for configuring tests at runtime without changing the code.

Contains examples of how to use dynamic start arguments in tests.

### how to start

1. Launch `jig init start_arguments`.
2. Launch [CouchDB instance](../documentation/database.md#couchdb-instance).
3. Modify the files described below.
4. Launch tests with dynamic arguments:

    ```bash
    jig run start_arguments

    # Using jig command
    jig start start_arguments --arg test_mode=debug --arg device_id=DUT-007 --arg retry_count=3

    # Or using pytest directly
    pytest --jig-start-arg test_mode=debug --jig-start-arg device_id=DUT-007 --jig-start-arg retry_count=3
    ```

    Alternatively, you can specify start arguments in the `pytest.ini` file.
    This is useful for setting default arguments that are always used when running tests.

    ```pytest
    [pytest]
    addopts = --jig-pt
            --jig-db-url http://dev:dev@localhost:5984/
            --jig-start-arg test_mode=debug
            --jig-start-arg device_id=DUT-007
    ```

### test_1.py

```python
import pytest
import jig

def test_with_start_args(jig_start_args):
   
    if jig_start_args.get("test_mode") == "debug":
        jig.set_message("Running in debug mode")
    
    device_id = jig_start_args.get("device_id")
    if device_id:
        jig.set_message(f"Testing device: {device_id}")
        jig.set_case_artifact({"device_id": device_id})
    else:
        jig.set_message("No device ID provided")
```

## Addoption

Alternative approach using pytest's built-in `addoption` method for adding custom options.
You can read more about it in the 
[pytest documentation](https://docs.pytest.org/en/stable/example/simple.html#how-to-change-command-line-options-defaults).

### how to start

1. Launch `jig init launch_arg`.
2. Launch [CouchDB instance](../documentation/database.md#couchdb-instance).
3. Modify the files described below.
4. Launch `jig run launch_arg`.

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
