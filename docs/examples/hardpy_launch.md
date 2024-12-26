# Hardpy launch

Hardpy can be launched either from the Operator Panel or from the terminal. Below we will look at all launch options.

### how to start

Initialize the HardPy project:

1. Launch `hardpy init test_project`.
2. Launch [CouchDH instance](../documentation/database.md#couchdb-instance).

#### 1. Operator panel

1. Launch `hardpy run test_project`.
   ```
   hardpy run
   ```
2. Open the Operator Panel in your browser at: [http://localhost:8000/](http://localhost:8000/).
3. Click the **Start** button.

#### 2. Console by pytest

???+ warning
    This method is only appropriate if you are not using any operator panel features such as operator messages and dialog boxes.

After starting the Operator Panel with `hardpy run`, you can run tests either by clicking the `Start` button or by using the `pytest` command.

Run the tests by executing the following command in the terminal:

```
pytest test_project
```

### 3. IDE

We will look at an example of running in vscode. 
If you use other IDEs, explore the possibility of running tests in your environment.

[IDE for testing in vscode](https://code.visualstudio.com/docs/editor/testing)

1. Open the **Testing** extension in VS Code.
2. Run the tests through the extension interface.

???+ warning
    This method is only appropriate if you are not using any operator panel features such as operator messages and dialog boxes.

After starting the Operator Panel with `hardpy run`, you can run tests either by clicking the `Start` button or by using the testing IDE.