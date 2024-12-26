# Instructions for running HardPy and tests with Pytest

## Step 1: Initialize the project

1. **Initialize the HardPy project:**

   ```
   hardpy init hello_hardpy
   ```

2. **Launch the CouchDB instance:**

   Launch [CouchDH instance](../documentation/database.md#couchdb-instance).

3. **(Optional) Launch HardPy:**

   ```
   hardpy run hello_hardpy
   ```

## Step 2: Options for running the tests

### Option 1: Run from the operator panel

1. Open the Operator Panel in your browser at: [http://localhost:8000/](http://localhost:8000/).
2. Click the **Start** button.

   ```
   hardpy run
   ```

### Option 2: Run through the console using Pytest

> **Note:** This method is only appropriate if you are not using any operator panel features such as operator messages and dialog boxes.

> **Note 2:** If the tests have operator messages, the tests themselves will work. 
If the tests have dialog boxes, the tests will not work correctly.

Run the tests by executing the following command in the terminal:

```
pytest <address of the folder with the tests>
```

Example:

```
pytest examples/couchdb_load
```

### Option 3: Run through the Testing extension in VS Code

1. Open the **Testing** extension in VS Code.
2. Run the tests through the extension interface.

> **Note:** This method is only appropriate if you are not using any operator panel features such as operator messages and dialog boxes.

> **Note 2:** If the tests have messages to the operator, the tests themselves will run. 
If the tests have dialog boxes, the tests will not work correctly.

### Option 4: Running with additional arguments

If you need to pass your own variables to the tests, you can use pytest's built-in `addoption` method. 
You can read more about it [here](https://docs.pytest.org/en/stable/example/simple.html#how-to-change-command-line-options-defaults).

#### Example of use:

1. In the `conftest.py` file, add the following code:

    ```python
    def pytest_addoption(parser):
        parser.addoption("--my-opt", action="store", help="add my opt")

    def my_opt(request):
        return request.config.getoption("--my-opt")
    ```

2. The test:

    ```python
    def test_custom_option(request):
        custom_value = request.config.getoption("--my-opt")
        print(f"Custom option value: {custom_value}")
        assert custom_value == "hello"
    ```

3. Run the test with the passed parameter:

    ```
    pytest --my-opt hello
    ```

    Alternatively, you can add the parameter `--my-opt hello` to the `pytest.ini` file. 
    This is the only way to run the test from the IDE for testing purposes.

## To summarise

You can pass any parameters in the terminal using command line arguments.

Running in the Ubuntu terminal is done in the same way. 
Don't forget to configure the environment.
