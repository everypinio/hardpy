# Database

## About

We use CouchDB because it's a simple document-oriented NoSQL database.
The database has two main purposes:

- Saving test report;
- Data synchronization with the web interface.
Data synchronization uses the replication mechanism of CouchDB and PouchDB.

The CouchDB version must be equal to or greater than the 3.2 version.

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

1. Use this [instruction](https://docs.couchdb.org/en/stable/install/unix.html#installation-using-the-apache-couchdb-convenience-binary-packages) to install CouchDB
2. The installer asks you if you want to install CouchDB as a standalone
application or in a clustered configuration.
Select `Standalone` and press Enter.
3. You are prompted to enter the Erlang Node Name.
You can ask it in Terminal with the command `hostname -f`
4. Set the Erlang Magic Cookie.
This is a unique identifier, for example, `test1234`
5. Configure the network interfaces on which CouchDB will be bound.
`localhost` is fine.
6. Enter an admin password of your choice for CouchDB, press `Enter`, re-type the password
and press `Enter` again to continue the installation.
7. After launching the database, it becomes available at the following
address http://localhost:5984/_utils/.
Open it.
8. First of all, in the `User Management` section in the `Create Admins` tab,
create a user with the login `dev` and password `dev`
9. In the `Config` choose `CORS` and appoint `Enable CORS` with `All domains`

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

1. Use this [instruction](https://docs.couchdb.org/en/stable/install/windows.html#installation-on-windows) to install CouchDB
2. Be sure to install CouchDB to a path with no spaces, such as `C:\CouchDB`.
3. Create a user with the login `dev` and password `dev` during the installation steps. Validate Credentials.
4. Generate Random Cookie.
5. After launching the database, it becomes available at the following address http://localhost:5984/_utils/.
Open it.
6. In the `Config` choose `CORS` and appoint `Enable CORS` with `All domains`


## Database in pytest-hardpy

### Description of databases

The pytest plugin has 2 databases: **statestore** and **runstore**.

- The **statestore** database contains the document **current**, which is a JSON
object that stores the current state of the test run without artifacts.
The plugin updates the document as testing progresses using the **StateStore** class.
- The **runstore** database contains the document **current**, which is a JSON object
that stores the current state of the test run with artifacts - a report on the current test run.
- The plugin updates the document as testing progresses using the **RunStore** class.

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

### Statestore scheme

<h1 align="center">
    <img src="https://raw.githubusercontent.com/everypinio/hardpy/main/docs/img/database/statestore.png" alt="statestore_scheme">
</h1>

The **current** document of the **statestore** database contains the following fields:

- **_rev**: current document revision;
- **_id**: unique document identifier;
- **progress**: test progress;
- **stop_time**: end time of testing in Unix seconds;
- **start_time**: testing start time in Unix seconds;
- **status**: test execution status;
- **name**: test suite name;
- **dut**: DUT information containing the serial number and additional information;
- **test_stand**: information about the test stand in the form of a dictionary;
- **modules**: module information;
- **alert**: operator panel alert information;
- **operator_msg**: operator message.

The **test_stand** block containt the following fields:

  - **name** - test stand name;
  - **drivers**: information about drivers in the form of a dictionary;
  - **info**: a dictionary containing additional information about the test stand;
  - **timezone**: timezone as a string;
  - **location**: test stand location;
  - **hw_id**: test stand machine id (GUID) or MAC address.

The **dut** block contains the following fields:

  - **serial_number**: DUT serial number;
  - **part_number**: DUT part number;
  - **info**: a dictionary containing additional information about the DUT, such as batch, board revision, etc.

The **operator_msg** block contains the following fields:

  - **msg**: message for operator;
  - **title**: the title of operator message dialog box;
  - **visible**: should a message be displayed on the operator panel;
  - **id**: operator message id;
  - **font_size**: operator message font size;
  - **image**: information about image;
    - **address**: image address;
    - **width**: image width in percent;
    - **border**: image border in pixels;
    - **base64**: image in base64 code;
  - **html**: information about html;
    - **code_or_url**: html code or link;
    - **is_raw_html**: is html code is raw;
    - **width**: html width in percent;
    - **border**: html border in pixels.

The **modules** block contains the following fields:

  - **test_{module_name}**: an object containing information about a specific module. Contains the following fields:
    - **status**: module test execution status;
    - **name**: module name, by default the same as module_id;
    - **start_time**: module testing start time in Unix seconds;
    - **stop_time**: end time of module testing in Unix seconds;
    - **cases**: an object containing information about each test case within the module. Contains the following fields:
      - **test_{test_name}**: an object containing information about the test. Contains the following fields:
        - **status**: test execution status;
        - **name**: test name, by default the same as case_id;
        - **start_time**: test start time in Unix seconds;
        - **stop_time**: test end time in Unix second;
        - **assertion_msg**: error message if the test fails;
        - **msg**: additional message;
        - **attempt**: attempt counting to pass the case;
        - **dialog_box**: information about dialog box;
          - **title_bar**: title bar of the dialog box;
          - **dialog_text**: text displayed in the dialog box;
          - **widget**: information about the widget;
            - **info**: widget additional information;
            - **type**: type of the widget;
          - **image**: information about image;
            - **address**: image address;
            - **width**: image width in percent;
            - **border**: image border in pixels;
            - **base64**: image in base64 code;
          - **html**: information about html;
            - **code_or_url**: html code or link;
            - **is_raw_html**: is html code is raw;
            - **width**: html width in percent;
            - **border**: html border in pixels;
          - **visible**: should a dialog box be displayed on the operator panel;
          - **id**: dialog box id;
          - **font_size**: dialog box font size.

Example of a **current** document:

```json
    {
      "_rev": "44867-3888ae85c19c428cc46685845953b483",
      "_id": "current",
      "progress": 100,
      "stop_time": 1695817266,
      "start_time": 1695817263,
      "status": "failed",
      "alert": "",
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
        "location": "Belgrade_1"
      },
      "operator_msg": {
        "msg": "Operator message",
        "title": "Message",
        "visible": true,
        "id": "f45ac1e7-2ce8-4a6b-bb9d-8863e30bcc78"
      },
      "modules": {
        "test_1_a": {
          "status": "failed",
          "name": "Module 1",
          "start_time": 1695816884,
          "stop_time": 1695817265,
          "cases": {
            "test_dut_info": {
              "status": "passed",
              "name": "DUT info ",
              "start_time": 1695817263,
              "stop_time": 1695817264,
              "assertion_msg": null,
              "msg": null,
              "attempt": 1,
              "dialog_box": {
                "title_bar": "Example of text input",
                "dialog_text": "Type some text and press the Confirm button",
                "widget": {
                  "info": {
                    "text": "some text"
                  },
                  "type": "textinput"
                },
                "image": {
                  "address": "assets/test.png",
                  "width": 100,
                  "border": 0,
                },
                "html": {
                  "code_or_url": "https://everypinio.github.io/hardpy/",
                  "width": 100,
                  "border": 0,
                  "is_raw_html": false
                },
                "visible": true,
                "id": "b57ab1e7-8cf8-4a6a-bb9d-8863ea0bcc78"
              }
            },
            "test_minute_parity": {
              "status": "failed",
              "name": "Test 1",
              "start_time": 1695817264,
              "stop_time": 1695817264,
              "assertion_msg": "The test failed because minute 21 is odd! Try again!",
              "attempt": 1,
              "msg": [
                "Current minute 21"
              ]
            }
          }
        }
      }
    }
```

### Runstore scheme

<h1 align="center">
    <img src="https://raw.githubusercontent.com/everypinio/hardpy/main/docs/img/database/runstore.png" alt="runstore_scheme">
</h1>

The **runstore** database is similar to **statestore** database, but there are differences:

- **runstore** contains the **artifact** field for test run, module, and case;
- **runstore** does not contain **dialog_box** and **attempt** fields.

The **current** document of **runstore** database contains the following fields:

- **_rev**: current document revision;
- **_id**: unique document identifier;
- **stop_time**: end time of testing in Unix seconds;
- **start_time**: testing start time in Unix seconds;
- **status**: test execution status;
- **name**: test suite name;
- **dut**: DUT information containing the serial number and additional information;
- **test_stand**: information about the test stand in the form of a dictionary;
- **artifact**: an object containing information about artifacts created during the test run;
- **modules**: module information.

The **test_stand** block containt the following fields:

  - **name** - test stand name;
  - **drivers**: information about drivers in the form of a dictionary;
  - **info**: a dictionary containing additional information about the test stand;
  - **timezone**: timezone as a string;
  - **location**: test stand location;
  - **hw_id**: test stand machine id (GUID) or MAC address.

The **dut** block contains the following fields:

  - **serial_number**: DUT serial number;
  - **part_number**: DUT part number;
  - **info**: A dictionary containing additional information about the DUT, such as batch, board revision, etc.

The **modules** block contains the following fields:

  - **test_{module_name}**: an object containing information about a specific module. Contains the following fields:
    - **status**: module test execution status;
    - **name**: module name, by default the same as module_id;
    - **start_time**: module testing start time in Unix seconds;
    - **stop_time**: end time of module testing in Unix seconds;
    - **artifact**: an object containing information about artifacts created during the test module process;
    - **cases**: an object containing information about each test within the module. Contains the following fields:
      - **test_{test_name}**: an object containing information about the test. Contains the following fields:
        - **status**: test execution status;
        - **name**: test name, by default the same as case_id;
        - **start_time**: test start time in Unix seconds;
        - **stop_time**: test end time in Unix second;
        - **assertion_msg**: error message if the test fails;
        - **msg**: additional message;
        - **artifact**: an object containing information about artifacts created during the test case process.

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
        "location": "Belgrade_1"
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
