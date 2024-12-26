# launching arguments

### how to start

1. Launch `hardpy init attempts`.
2. Launch [CouchDH instance](../documentation/database.md#couchdb-instance).
3. Modify the files described below.
4. Launch `hardpy run attempts`.

So that you can run Hardpy in separate scripts that use the arguments, you can use pytest's built-in `addoption` method. 

You can read more about it [here](https://docs.pytest.org/en/stable/example/simple.html#how-to-change-command-line-options-defaults).

### conftest.py

```python
def pytest_addoption(parser):
    parser.addoption("--my-opt", action="store", help="add my opt")

def my_opt(request):
    return request.config.getoption("--my-opt")
```

### test_1.py

```python
def test_custom_option(request):
    custom_value = request.config.getoption("--my-opt")
    print(f"Custom option value: {custom_value}")
    assert custom_value == "hello"
```

### launch test with your parameter

You can launch tests with this command:

```
pytest --my-opt hello
```

Alternatively, you can add the parameter `--my-opt hello` to the `pytest.ini` file. 
This is the only way to run the test from the IDE for testing purposes.

### summarize

You can pass any parameters in the terminal using command line arguments.

Running in the Ubuntu terminal is done in the same way. 
Don't forget to configure the environment.