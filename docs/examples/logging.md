# Logging in Tests

How to add logging to your tests using Python's built-in `logging` package.

Python's built-in `logging` package provides a flexible way to add logging to your tests, which can help with debugging and monitoring test execution.

Logging in tests is valuable because it:

- Provides visibility into test execution flow
- Helps diagnose failures by capturing context
- Creates an audit trail of test operations
- Enables performance monitoring
- Facilitates troubleshooting in CI/CD pipelines

The logs will be written to:

- Console output
- CI/CD system logs if running in a pipeline

While Python's `logging` package is versatile, **HardPy** offers additional specialized logging methods:

- [Database Logging with set_message](./../features/features.md/#database-logging-with-set_message)
- [Interactive Dialogs with run_dialog_box](./../features/features.md/#interactive-dialogs-with-run_dialog_box) 
- [Operator Messages with set_operator_message](./../features/features.md/#operator-messages-with-set_operator_message)

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

You can find the description in [How to manage logging](https://docs.pytest.org/en/latest/how-to/logging.html)

### Explanation of configuration options

- `log_cli = true`: Enables logging output during test execution
- `log_cli_level = INFO`: Sets the minimum logging level to display
- `log_cli_format`: Defines the format of log messages:
  - `%(asctime)s`: Timestamp
  - `[%(levelname)s]`: Log level (INFO, WARNING, etc.)
  - `%(message)s`: The actual log message
- `log_cli_date_format = %H:%M:%S`: Sets the timestamp format to hours:minutes:seconds
