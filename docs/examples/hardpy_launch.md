# HardPy launch

**HardPy** can be started from either the operator panel or the terminal. 
Below we will look at all the launch options.

### how to start

Initialize the **HardPy** project:

1. Launch `hardpy init test_project`.
2. Launch [CouchDH instance](../documentation/database.md#couchdb-instance).

### launch options

#### 1. Operator panel

1. Launch operator panel:
   ```
   hardpy run test_project
   ```
2. Open the operator panel in your browser at: [http://localhost:8000/](http://localhost:8000/).
3. Click the **Start** button.

#### 2. Pytest in console

Run the tests by executing the following command in the terminal:

```
pytest test_project
```

##### 2.1. Pytest in console with launching operator panel

If the operator panel is running, the tests will start after the command in the terminal in the same way as by clicking on the `Start` button.

##### 2.2. Pytest in console without launching operator panel

If the operator panel has not been started, the tests will also run, but without visualization.

???+ warning
    This method is only appropriate if you are not using any operator panel features such as operator messages and dialog boxes.

#### 3. IDE

An example of starting in vscode is as follows.
If you use other IDEs, explore the possibility of running tests in your environment.

1. Open the [Testing](https://code.visualstudio.com/docs/editor/testing) extension in VS Code.
2. Run the tests through the extension interface.

##### 3.1. Pytest in Testing with launching operator panel

If the operator panel is running, the tests will start after launching in Testing in the same way as by clicking on the `Start` button.

##### 3.2. Pytest in Testing without launching operator panel

If the operator panel has not been started, the tests will also run, but without visualization.

???+ warning
    This method is only appropriate if you are not using any operator panel features such as operator messages and dialog boxes.
