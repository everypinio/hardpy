# Multiple stands

This is an example of running multiple stands on one PC.

The example implements the launch of two stands and three CouchDB Instances. 

Each stand will record reports on the conducted testing in the CouchDB Instance assigned to it in the **runstore** and **statestore** databases.
The third CouchDB Instance is needed to store reports in the **report** database on each conducted test of each stand.

You can learn more about storing reports here [Couchdb instance](../documentation/database.md#couchdb-instance).

### projects

* Create 2 separate projects. Add a simple test to the `tests` folder of each project.

```ini
# pytest.ini
[pytest]
addopts = --hardpy-pt
```

```python
# test_1.py
import pytest

def test_one():
    assert True
```
* Create another project for the CouchDB instance to store the report history.

### databases

Create a separate CouchDB Instance for each project, and use a different port for each.

To create a CouchDB Instance use [CouchDH instance](../documentation/database.md#couchdb-instance) instruction.

* Create a `couchdb.ini` file in each project.
* Launch the next script from the folder with the `couchdb.ini` file:

```bash
docker run 6--name tests_hardpy -p 5984:5984 -e COUCHDB_USER=dev -e COUCHDB_PASSWORD=dev -v ./couchdb.ini:/opt/couchdb/etc/local.ini  couchdb:3.3
```
Where:

* `--name tests_hardpy` - container name
* `-p 5984:5984` - database port (use a different port for each)
* `-e COUCHDB_USER=dev` - user name
* `-e COUCHDB_PASSWORD=dev` - password

For example, run a second database on port 5985:

```bash
docker run --name tests_hardpy_2 -p 5985:5984 -e COUCHDB_USER=dev -e COUCHDB_PASSWORD=dev -v ./couchdb.ini:/opt/couchdb/etc/local.ini  couchdb:3.3
```

For example, run a third database on port 5986:

```bash
docker run --name tests_hardpy_3 -p 5986:5984 -e COUCHDB_USER=dev -e COUCHDB_PASSWORD=dev -v ./couchdb.ini:/opt/couchdb/etc/local.ini  couchdb:3.3
```

#### conftest.py

Create in the folder of each stand `conftest.py` file.
Contains settings and fixtures for all tests:

* The function of generating a report and recording it in the database `save_report_to_couchdb`;
* The list of actions that will be performed after testing is filled in function `fill_actions_after_test`;

To store reports from all booths in the third CouchDB Instance, specify the port numbers of this CouchDB Instance in the file `conftest.py` in the folder of each stand.

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


### operator panels

In projects with tests, configure a connection to its own database for storing state and to its own operator panel.
To launch project with connection to database use script:

```bash
hardpy-panel -dbp 5984 -wp 8000 <dir_name>/tests
```

* `5984` - port of database
* `8000` - operator-panel port (frontend)
* `<dir_name>/tests` - the path to the folder with the tests

For another project, use different ports:

```bash
hardpy-panel -dbp 5985 -wp 8001 tests
```