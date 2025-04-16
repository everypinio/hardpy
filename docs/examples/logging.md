# Logging in Tests

How to add logging to your tests using Python's built-in `logging` package.

## How to implement logging

### Basic setup

1. Import the logging module where needed:

    ```python
    import logging
    ```

2. Add a fixture to `conftest.py`:

    ```python
    @pytest.fixture(scope="module")
    def module_log(request: pytest.FixtureRequest):
        log_name = request.module.__name__
        yield logging.getLogger(log_name)
    ```

3. Initialize the logger in your test class:

    ```python
    def __init__(self) -> None:
        self._log = getLogger(__name__)
    ```

### Using the logger

You can call logging commands anywhere in your tests:

```python
self._log.warning("Saving user credentials for registration test case")
```

Example of logging in a test function:

```python
def test_log(module_log: logging.Logger):
    module_log.info("DUT serial number logged")
    assert True

```

## Configuration

To configure logging parameters, add these settings to your `pytest.ini` file:

```ini
[pytest]
log_cli = true
log_cli_level = INFO
log_cli_format = %(asctime)s [%(levelname)s] %(message)s
log_cli_date_format = %H:%M:%S
```

You can find the description in [Pytest Live Logs Documentation](https://docs.pytest.org/en/7.1.x/how-to/logging.html#live-logs)

### Explanation of configuration options

- `log_cli = true`: Enables logging output during test execution
- `log_cli_level = INFO`: Sets the minimum logging level to display
- `log_cli_format`: Defines the format of log messages:
  - `%(asctime)s`: Timestamp
  - `[%(levelname)s]`: Log level (INFO, WARNING, etc.)
  - `%(message)s`: The actual log message
- `log_cli_date_format = %H:%M:%S`: Sets the timestamp format to hours:minutes:seconds
