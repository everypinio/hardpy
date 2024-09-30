# Multiple stands

This is an example of running multiple stands on one PC.

The example implements the launch of two stands and three CouchDB Instances.

Each stand will record reports on the conducted testing in the CouchDB Instance
assigned to it in the **runstore** and **statestore** databases.
The third CouchDB Instance is needed to store reports in the **report**
database on each conducted test of each stand.

You can learn more about storing reports here
[Couchdb instance](../documentation/database.md#couchdb-instance).

### projects

* Create 2 separate projects.

```bash
hardpy init tests_1
```

```bash
hardpy init tests_2 --database-port 5985 --frontend-port 8001
```

### databases

For the third database, you can use `hardpy init` and delete
all files except the database folder and the `docker-compose.yaml` file.

```bash
hardpy init third_database --database-port 5986
```

#### conftest.py

Modify `conftest.py` file in each project.
Contains settings and fixtures for all tests:

* The function of generating a report and recording it in the database `save_report_to_couchdb`;
* The list of actions that will be performed after testing is filled in function `fill_actions_after_test`;

To store reports from all booths in the third CouchDB Instance, specify the
port numbers of this CouchDB Instance in the file `conftest.py` in the folder of each stand.

```bash
import pytest

from hardpy import (
    CouchdbLoader,
    CouchdbConfig,
    get_current_report,
)

def save_report_to_couchdb():
    report = get_current_report()
    if report:
        loader = CouchdbLoader(CouchdbConfig(port=5986))
        loader.load(report)

@pytest.fixture(scope="session", autouse=True)
def fill_actions_after_test(post_run_functions: list):
    post_run_functions.append(save_report_to_couchdb)
    yield
```

* `5986` - port of the database with reports

### dialog box

If you want to use the dialog box in multiple stands on the same computer, you need
to modify a [socket port](./../documentation/cli.md#hardpy-init).
By default, hardpy uses port *6525* to pass data to the running pytest.
But if you run multiple stands, the *6525* socket port will be busy.

Example:

```bash
hardpy init tests_2 --database-port 5985 --frontend-port 8001 --socket-port 6526
```

### how to start

1. Start all databases via **docker compose**.
2. Launch both project via `hardpy run <project_name>`.
