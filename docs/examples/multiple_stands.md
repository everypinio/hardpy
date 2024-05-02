# Multiple stands

This is an example of running multiple stands on one PC.

### projects

Create 2 separate projects. Add a simple test to the `tests` folder of each project.

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

### databases

Create a separate database for each project, and use a different port for each.
To create a database use [CouchDH instance](../documentation/database.md#couchdb-instance) instruction.

* Create a `couchdb.ini` file:
* Launch the next script from the folder with the `couchdb.ini` file:

```bash
docker run --name tests_hardpy  -p 5984:5984  -e COUCHDB_USER=dev  -e COUCHDB_PASSWORD=dev  -v ./couchdb.ini:/opt/couchdb/etc/local.ini  couchdb:3.3
```
Where:

* `--name tests_hardpy` - container name
* `-p 5984:5984` - database port (use a different port for each)
* `-e COUCHDB_USER=dev` - user name
* `-e COUCHDB_PASSWORD=dev` - password

For example, run a second database on port 5985:
```bash
docker run --name tests_hardpy_2  -p 5985:5984  -e COUCHDB_USER=dev  -e COUCHDB_PASSWORD=dev  -v ./couchdb.ini:/opt/couchdb/etc/local.ini  couchdb:3.3
```

### operator panels

Configure in each project a connection to its own database for storing state and to its own operator panel.
To launch project with connection to database use script:

```bash
hardpy-panel -dbp 5984 -wp 8000 tests
```

* `5984` - port of database
* `8000` - operator-panel port (frontend)
* `tests` - folder with tests

For another project, use different ports:

```bash
hardpy-panel -dbp 5985 -wp 8001 tests
```

### storing reports

We can use the database to store a list of reports. This will require a separate database.

We can use the **reports** database, as in the example [CouchDB Load](couchdb_load.md).


#### pytest.ini

Create in the folder of each stand `pytest.ini` file.

It is a file of built-in configuration options that determine how live logging works and enable pytest-hardpy plugin for launching via pytest.

```bash
[pytest]
log_cli = true
log_cli_level = INFO
log_cli_format = %(asctime)s [%(levelname)s] %(message)s
log_cli_date_format = %H:%M:%S
addopts = --hardpy-pt
```

#### conftest.py

Create in the folder of each stand `conftest.py` file.

Contains settings and fixtures for all tests:

* The function of generating a report and recording it in the database save_report_to_couchdb;
* The list of actions that will be performed after testing is filled in function fill_actions_after_test;

To store reports from all booths in one database, set the port number 
of this database to a file `conftest.py ` in the folder of each stand.

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


#### Running CouchDB with Docker

1. Create couchdb.ini file.

```bash
[chttpd]
enable_cors=true

[cors]
origins = *
methods = GET, PUT, POST, HEAD, DELETE
credentials = true
headers = accept, authorization, content-type, origin, referer, x-csrf-token
```

2. The Docker version must be 24.0.0 or higher. Run the Docker container (from the folder with the couchdb.ini file).

    Command for Linux:

    ```bash
    docker run --rm --name couchdb -p 5984:5984 -e COUCHDB_USER=dev -e COUCHDB_PASSWORD=dev -v ./couchdb.ini:/opt/couchdb/etc/local.ini couchdb:3.3
    ```

    Command for Windows:

    ```bash
    docker run --rm --name couchdb -p 5984:5984 -e COUCHDB_USER=dev -e COUCHDB_PASSWORD=dev -v .\couchdb.ini:/opt/couchdb/etc/local.ini couchdb:3.3.2
    ```

    The container will be deleted after use.


