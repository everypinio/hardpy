# Multiple stands

This is an example of running multiple stands on one PC.

Each stand will record reports on the testing it conducts in the **CouchDB** 
document assigned to it in the **runstore** and **statestore** databases.

### how to start

1. Create three separate projects, each with a different frontend port.
   Launch: 
    ```bash
    hardpy init tests_1 
    ```

    ```bash
    hardpy init tests_2 --frontend-port 8001
    ```

    ```bash
    hardpy init tests_3 --frontend-port 8002
    ```
2. Launch any database [CouchDB instance](../documentation/database.md#couchdb-instance) from any project.
3. Modify the files described below.
4. Launch all projects:
   
   ```bash
   hardpy run tests_1
   ```

   ```bash
   hardpy run tests_2
   ```

   ```bash
   hardpy run tests_3
   ```

### result

Three instances of **HardPy** will launch at the following addresses: 
localhost:8000, localhost:8001, and localhost:8002. 
Documents named *localhost_8000*, *localhost_8001*, and *localhost_8002* will 
appear immediately in the statestore database. 
Documents named *localhost_8000*, *localhost_8001*, and *localhost_8002* will 
appear after the test is launched in the runstore database. 
Each document is synchronized with its corresponding HardPy server address.
If the host addresses in the hardpy.toml file change, the document addresses will change as well.
