# Multiple stands

This is an example of running multiple stands on one PC.

### projects

Create 2 separate projects. Add a simple test to the `tests` folder of each project.

```python
# conftest.py
import pytest
import hardpy

def pytest_configure(config: pytest.Config):
    config.pluginmanager.register(hardpy.HardpyPlugin())
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

We can use the **reports** database, as in the example [CouchDB Load](couchdb_load.md).
A separate database is required to store the list of reports.
By default, reports are saved to the default database on port 5984, but you can assign another port.
Configure database on port 5986 for storing reports in `conftest.py` in the test folder:

```python
loader = CouchdbLoader(CouchdbConfig(port=5986))
```

* `5986` - port of the database with reports
