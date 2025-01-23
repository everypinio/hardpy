# Launch arguments

**HardPy** launches pytest tests.
User can add own arguments and options for test execution.
For example, user can write own script for **HardPy** to run with special arguments, such as device serial number, and use it in tests.

### how to start

1. Launch `hardpy init launch_arg`.
2. Launch [CouchDH instance](../documentation/database.md#couchdb-instance).
3. Modify the files described below.
4. Launch `hardpy run launch_arg`.

So that you can run **HardPy** in separate scripts that use the arguments, you can use pytest's built-in `addoption` method.
You can read more about it [here](https://docs.pytest.org/en/stable/example/simple.html#how-to-change-command-line-options-defaults).

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
