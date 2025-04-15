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
self._log.warning("Random method")
```

Example of logging in a test function:

```python
def test_dut_info(module_log: logging.Logger):
    serial_number = str(uuid4())[:6]
    module_log.info(f"DUT serial number {serial_number}")
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

### Explanation of configuration options

- `log_cli = true`: Enables logging output during test execution
- `log_cli_level = INFO`: Sets the minimum logging level to display
- `log_cli_format`: Defines the format of log messages:
  - `%(asctime)s`: Timestamp
  - `[%(levelname)s]`: Log level (INFO, WARNING, etc.)
  - `%(message)s`: The actual log message
- `log_cli_date_format = %H:%M:%S`: Sets the timestamp format to hours:minutes:seconds

## Log Levels

Logging supports standard Python logging levels with these recommended use cases:

- **`INFO`**: General test progress information

  ```python
  self._log.info("Test started with parameters: %s", params)
  ```

- **`WARNING`**: Non-critical issues that don't fail the test

  ```python
  self._log.warning("Temperature approaching limit: %d°C", current_temp)
  ```

- **`ERROR`**: Recoverable errors that may affect test results

  ```python
  self._log.error("Sensor read failed, using cached value")
  ```

- **`CRITICAL`**: Severe issues requiring immediate attention

  ```python
  self._log.critical("Safety limit exceeded! Shutting down")
  ```
