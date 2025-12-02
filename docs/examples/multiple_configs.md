# Multiple Configs

This example demonstrates how to manage multiple test configurations within a single **HardPy** project. 
This is useful when you need to run different sets of tests, 
or the same tests with different parameters, without modifying the main `hardpy.toml` or `pytest.ini` files for each run.
The code for this example can be seen inside the hardpy package
[Multiple Configs](https://github.com/everypinio/hardpy/tree/main/examples/multiple_configs).

### how to start

1. Launch [CouchDB instance](../documentation/database.md#couchdb-instance).
2. Launch `hardpy run examples/multiple_configs`.

### Project Structure

The `examples/multiple_configs` directory contains:

- `hardpy.toml`: The main HardPy configuration file, which defines the available test configurations.
- `config1_pytest.ini`, `config2_pytest.ini`, `config3_pytest.ini`: Individual pytest configuration files, 
  each specifying a unique set of tests or pytest arguments.
- `test_1.py`, `test_2.py`, `test_3.py`: Example test files that are executed based on the selected configuration.

### `hardpy.toml` Configuration

The `hardpy.toml` file defines the different test configurations using the `[[test_configs]]` table array. Each entry has:

- `name`: A user-friendly name for the configuration.
- `file`: The path to the `pytest.ini` file that defines the specific pytest arguments and test selection for this configuration.
- `description`: An optional field to provide a more detailed explanation of the configuration.

```toml
# examples/multiple_configs/hardpy.toml
[[test_configs]]
name = "Config 1"
file = "config1_pytest.ini"

[[test_configs]]
name = "Config 2"
file = "config2_pytest.ini"

[[test_configs]]
name = "Config 3"
description = "Example description"
file = "config3_pytest.ini"
```

### `pytest.ini` Files

Each `pytest.ini` file specifies the `python_files` that pytest should collect and run for that specific configuration.

For example, `config1_pytest.ini` will run `test_1.py`:

```ini
# examples/multiple_configs/config1_pytest.ini
[pytest]
addopts = --hardpy-pt
          --hardpy-db-url http://dev:dev@localhost:5984/

; This prevents pytest from trying to collect tests from this directory
testpaths = 

; Instead we specify the test files directly
python_files = test_1.py
```

### Running Multiple Configurations

When launching HardPy, you can select which configuration to use. 
This allows you to easily switch between different testing scenarios.
