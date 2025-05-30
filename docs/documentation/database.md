# Database

## About

We use CouchDB because it's a simple document-oriented NoSQL database.
The database has two main purposes:

- Saving test report;
- [Data synchronization](./../about/fronted_sync.md) with the web interface.

The CouchDB version must be equal to or greater than the 3.2 version.

## Database in pytest-hardpy

### Description of databases

The pytest plugin has 2 databases: **statestore** and **runstore**.

- The **statestore** database uses for frontend [data synchronization](./../about/fronted_sync.md).
- The **runstore** database contains the document **current**, which is a JSON object
that stores the current state of the test run.

A separate database is required to store the list of reports.
The **report** database is used as an example of storing reports on past testing runs.
It can be launched in the same instance as the **statestore**, **runstore** database, or in a different one.
The database is accessed through the **CouchdbLoader** class, which can be called at the end of each launch.
To read the current report, use the `get_current_report()` function.

Sample code for saving a report at the end of testing:

```python
# conftest.py
def save_report_to_couchdb():
    report = get_current_report()
    if report:
        loader = CouchdbLoader(CouchdbConfig())
        loader.load(report)


@pytest.fixture(scope="session", autouse=True)
def fill_actions_after_test(post_run_functions: list):
    post_run_functions.append(save_report_to_couchdb)
    yield
```

**HardPy** users have the flexibility to choose their preferred database.
They can write custom classes to record reports at the end of testing.

### Runstore scheme

The **runstore** and **report** databases have the same schema, as **runstore**
stores the current report and **report** stores reports.

<h1 align="center">
    <img src="https://raw.githubusercontent.com/everypinio/hardpy/main/docs/img/database/runstore.png" alt="runstore_scheme">
</h1>

The **current** document of **runstore** database contains some section.

#### main

- **_rev**: a CouchDB [revision MVCC](https://docs.couchdb.org/en/stable/api/document/common.html) token;
  The variable is assigned automatically.
- **_id**: unique document identifier.
  The variable is assigned automatically.
- **stop_time**: the end time of the test in Unix seconds. The variable is assigned automatically.
- **start_time**: the start time of the test in Unix seconds. The variable is assigned automatically.
- **status**: test execution status from **pytest**: **passed**, **failed**, **skipped**, **stopped**.
  The variable is assigned automatically.
- **name**: the name of the test suite. It is displayed in the header of the operator panel.
  The user can specify the name using the `tests_name` variable in the **hardpy.toml** file.
  If this variable is not set, the name will be taken from the directory name containing the tests.
- **dut**: DUT information. See the [dut](#dut) section for more information.
- **test_stand**: test stand information. See the [test_stand](#test_stand) section for more information.
- **artifact**: an object that contains information about the artifacts created during the test run.
  The user can specify the run artifact by using [set_run_artifact](./pytest_hardpy.md#set_run_artifact) function.
  The artifact contains a dictionary where the user can store any data at the test run level.
  The artifacts are not displayed on the operator panel.
- **modules**: module (pytest files) information. See the [modules](#modules) section for more information.

#### test_stand

The **test_stand** section contains information about the test stand.
It is a computer on which **HardPy** is running and to which the DUT test equipment is connected.

- **name** - test stand name. It can only be set once per test run.
  The user can specify the stand name by using [set_stand_name](./pytest_hardpy.md#set_stand_name) function.
- **drivers**: information about drivers in the form of a dictionary, including test equipment and test equipment software.
  The user can specify the driver info by using [set_driver_info](./pytest_hardpy.md#set_driver_info) function.
- **info**: dictionary containing additional information about the test stand.
  The user can specify the additional info by using [set_stand_info](./pytest_hardpy.md#set_stand_info) function.
- **timezone**: timezone of test stand as a string. The variable is assigned automatically.
- **location**: the location of the test stand, e.g., the country, city, or laboratory number.
  It can only be set once per test run. The user can specify the location by using
  [set_stand_location](./pytest_hardpy.md#set_stand_location) function.
- **number**: test stand number. Some stands may have the same name and
  run on the same computer but have different numbers. It can only be set once per test run.
  The user can specify the stand number by using [set_stand_number](./pytest_hardpy.md#set_stand_number) function.
- **hw_id**: test stand machine id (GUID) or host name. The variable is assigned automatically by
  the [py-machineid](https://pypi.org/project/py-machineid/) package.

##### test_stand examples

**Two stands on one computer**:

```json
// test stand 1
"test_stand": {
  "hw_id": "840982098ca2459a7b22cc608eff65d4",
  "name": "Test stand A",
  "info": {},
  "timezone": "Europe/Helsinki",
  "drivers": {
    "driver_1": {
      "state": "active",
      "port": 3000
    }
  },
  "location": "Helsinki",
  "number": 1
},
```

```json
// test stand 2
"test_stand": {
  "hw_id": "840982098ca2459a7b22cc608eff65d4",
  "name": "Test stand A",
  "info": {},
  "timezone": "Europe/Helsinki",
  "drivers": {
    "driver_1": {
      "state": "active",
      "port": 3000
    }
  },
  "location": "Helsinki",
  "number": 2
},
```

**Two different stands**:

```json
// test stand 1
"test_stand": {
  "hw_id": "840982098ca2459a7b22cc608eff65d4",
  "name": "ABC",
  "info": {},
  "timezone": "Europe/Helsinki",
  "drivers": {
    "voltmeter": {
      "sw_version": "1.1.3",
      "hw_version": "2.0.1"
    }
  },
  "location": "Laboratory 1",
  "number": null
},
```

```json
// test stand 2
"test_stand": {
  "hw_id": "156731093ab759a7b11ac108eaf69d2",
  "name": "DEF",
  "info": {},
  "timezone": "Europe/Helsinki",
  "drivers": {},
  "location": "Laboratory 2",
  "number": null
},
```

#### dut

The device under test section contains information about the DUT.

- **serial_number**: DUT serial number. This identifier is unique to the testing device or board.
  It can only be set once per test run.
  The user can specify the DUT serial number by using [set_dut_serial_number](./pytest_hardpy.md#set_dut_serial_number) function.
- **part_number**: DUT part number. This identifier of a particular part design, board or device.
  It can only be set once per test run.
  The user can specify the DUT part number by using [set_dut_part_number](./pytest_hardpy.md#set_dut_part_number) function.
- **info**: dictionary containing additional information about the the DUT, such as batch, board revision, etc.
  The user can specify the additional info by using [set_dut_info](./pytest_hardpy.md#set_dut_info) function.

##### dut examples

**Testing of two devices of the same type (same part number)**:

```json
// dut 1
"dut": {
  "serial_number": "1000-10",
  "part_number": "ABC11",
  "info": {
    "board_rev": "rev_1"
  }
}
```

```json
// dut 2
"dut": {
  "serial_number": "1000-11",
  "part_number": "ABC11",
  "info": {
    "board_rev": "rev_1"
  }
}
```

#### modules

The **modules** section contains the information about tests.
Each module contains information from a single test file.
The module's name is the same as the file's name.

- **test_{module_name}**: an object containing information about a specific module.
  The `{module_name}` variable is assigned automatically.
  Contains the following fields:
  - **status**: module test execution status. The variable is assigned automatically.
  - **name**: module name, by default the same as module_id.
    The user can specify the module name by using [module_name](./pytest_hardpy.md#module_name) marker.
  - **start_time**: start time of module testing in Unix seconds. The variable is assigned automatically.
  - **stop_time**: end time of module testing in Unix seconds. The variable is assigned automatically.
  - **artifact**: an object that contains information about the artifacts created during the test module.
    The user can specify the module artifact by using [set_module_artifact](./pytest_hardpy.md#set_module_artifact) function.
    The artifact contains a dictionary where the user can store any data at the test module level.
    The artifacts are not displayed on the operator panel.
  - **cases**: an object that contains information about each test case within the module.
    - **test_{case_name}**: an object containing information about a specific case.
      The `{case_name}` variable is assigned automatically.
      Contains the following fields:
      - **status**: test case execution status. The variable is assigned automatically.
      - **name**: case name, by default the same as case_id.
        The user can specify the case name by using [case_name](./pytest_hardpy.md#case_name) marker.
      - **start_time**: start time of case testing in Unix seconds. The variable is assigned automatically.
      - **stop_time**: end time of case testing in Unix seconds. The variable is assigned automatically.
      - **assertion_msg**: assert or error message if the test case fails. The variable is assigned automatically.
        However, the user can write their own message in case of an assertion, which will be written to this variable.
        For example:
        ```python
        assert False, "This is an example"
        ```
        The **assertion_msg** is displayed in the operator panel next to the test case in which it was called.
      - **msg**: the log message is displayed in the operator panel next to the test case in which it was called.
        The user can specify and update current message by using [set_message](./pytest_hardpy.md#set_message) function.
      - **artifact**: an object that contains information about the artifacts created during the test case.
        The user can specify the case artifact by using [set_case_artifact](./pytest_hardpy.md#set_case_artifact) function.
        The artifact contains a dictionary where the user can store any data at the test case level.
        The artifacts are not displayed on the operator panel.

### Report example

Example of a **current** document:

```json
    {
      "_rev": "44867-3888ae85c19c428cc46685845953b483",
      "_id": "current",
      "stop_time": 1695817266,
      "start_time": 1695817263,
      "status": "failed",
      "name": "hardpy-stand",
      "dut": {
        "serial_number": "92c5a4bb-ecb0-42c5-89ac-e0caca0919fd",
        "part_number": "part_1",
        "info": {
          "batch": "test_batch",
          "board_rev": "rev_1"
        }
      },
      "test_stand": {
        "hw_id": "840982098ca2459a7b22cc608eff65d4",
        "name": "test_stand_1",
        "info": {
          "geo": "Belgrade"
        },
        "timezone": "Europe/Belgrade",
        "drivers": {
          "driver_1": "driver info",
          "driver_2": {
            "state": "active",
            "port": 8000
          }
        },
        "location": "Belgrade_1",
        "number": 2
      },
      "artifact": {},
      "modules": {
        "test_1_a": {
          "status": "failed",
          "name": "Module 1",
          "start_time": 1695816884,
          "stop_time": 1695817265,
          "artifact": {},
          "cases": {
            "test_dut_info": {
              "status": "passed",
              "name": "DUT info",
              "start_time": 1695817263,
              "stop_time": 1695817264,
              "assertion_msg": null,
              "msg": null,
              "artifact": {}
            },
            "test_minute_parity": {
              "status": "failed",
              "name": "Test 1",
              "start_time": 1695817264,
              "stop_time": 1695817264,
              "assertion_msg": "The test failed because minute 21 is odd! Try again!",
              "msg": [
                "Current minute 21"
              ],
              "artifact": {
                "data_str": "123DATA",
                "data_int": 12345,
                "data_dict": {
                  "test_key": "456DATA"
                }
              }
            }
          }
        }
      }
    }
```

## CouchDB instance

This section explains how to launch and manage a CouchDB instance.
After launching the database, it becomes available at the following address:

> http://localhost:5984/_utils/

The internal settings of the database are contained in the **couchDB.ini** configuration file.
It contains settings that define the behavior and operating parameters of the database.

### Running CouchDB with Docker Compose

An example configuration for running CouchDB via Docker Compose is located in
the `example/database/couchdb` folder.
A shortened version of the instructions is described below.

1. Create a `docker` directory in the project's root directory.
2. Create a `couchdb.ini` file in the `docker` directory.

```ini
[chttpd]
enable_cors=true

[cors]
origins = *
methods = GET, PUT, POST, HEAD, DELETE
credentials = true
headers = accept, authorization, content-type, origin, referer, x-csrf-token
```
3. Create a `docker-compose.yaml` file in project's root directory.

```yaml
version: "3.8"

services:
  couchserver:
    image: couchdb:3.4
    ports:
      - "5984:5984"
    environment:
      COUCHDB_USER: dev
      COUCHDB_PASSWORD: dev
    volumes:
      - ./docker/dbdata:/opt/couchdb/data
      - ./docker/couchdb.ini:/opt/couchdb/etc/local.ini
```
4. Run **docker compose** in the root directory.

```bash
docker compose up
```
5. To stop the database, run the command:

```bash
docker compose down
```

### Running CouchDB with Docker

1. Create `couchdb.ini` file.

```ini
[chttpd]
enable_cors=true

[cors]
origins = *
methods = GET, PUT, POST, HEAD, DELETE
credentials = true
headers = accept, authorization, content-type, origin, referer, x-csrf-token
```
2. The Docker version must be 24.0.0 or higher. Run the Docker container (from the folder with the couchdb.ini file):

```bash
docker run --rm --name couchdb -p 5984:5984 -e COUCHDB_USER=dev -e COUCHDB_PASSWORD=dev -v ./couchdb.ini:/opt/couchdb/etc/local.ini couchdb:3.4
```

Command for Windows:

```bash
docker run --rm --name couchdb -p 5984:5984 -e COUCHDB_USER=dev -e COUCHDB_PASSWORD=dev -v .\couchdb.ini:/opt/couchdb/etc/local.ini couchdb:3.4
```

The container will be deleted after use.

### Running CouchDB with binary packages in Linux

1. Use this [instruction](https://docs.couchdb.org/en/stable/install/unix.html#installation-using-the-apache-couchdb-convenience-binary-packages) to install CouchDB.
2. The installer asks you if you want to install CouchDB as a standalone
application or in a clustered configuration.
Select `Standalone` and press Enter.
3. You are prompted to enter the Erlang Node Name.
You can ask it in Terminal with the command `hostname -f`.
4. Set the Erlang Magic Cookie.
This is a unique identifier, for example, `test1234`.
5. Configure the network interfaces on which CouchDB will be bound
`localhost` is fine.
6. Enter an admin password of your choice for CouchDB, press `Enter`, re-type the password
and press `Enter` again to continue the installation.
7. After launching the database, it becomes available at the following
address http://localhost:5984/_utils/.
Open it.
8. First of all, in the `User Management` section in the `Create Admins` tab,
create a user with the login `dev` and password `dev`.
9. In the `Config` choose `CORS` and appoint `Enable CORS` with `All domains`.

#### To disable the CouchDB service:

Remove packages:
```bash
sudo apt remove --purge couchdb
```
Remove GPG keys and repository:
```bash
sudo rm /usr/share/keyrings/couchdb-archive-keyring.gpg
sudo rm /etc/apt/sources.list.d/couchdb.list
```
Clean APT cache:
```bash
sudo apt clean
```
Disable service:
```bash
systemctl stop couchdb.service
systemctl disable couchdb.service
systemctl daemon-reload
systemctl reset-failed
```

### Running CouchDB with binary packages in Windows

1. Use this [instruction](https://docs.couchdb.org/en/stable/install/windows.html#installation-on-windows) to install CouchDB.
2. Be sure to install CouchDB to a path with no spaces, such as `C:\CouchDB`.
3. Create a user with the login `dev` and password `dev` during the installation steps. Validate Credentials.
4. Generate Random Cookie.
5. After launching the database, it becomes available at the following address http://localhost:5984/_utils/.
Open it.
6. In the `Config` choose `CORS` and appoint `Enable CORS` with `All domains`.
