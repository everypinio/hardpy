# Frontend data synchronization

Data synchronization uses the replication mechanism of CouchDB and PouchDB.

- The **statestore** database contains the document **current**, which is a JSON
object that stores the current state of the test run without artifacts.
The plugin updates the document as testing progresses using the **StateStore** class.
- The [runstore](./../documentation/database.md#runstore-scheme) database contains the document
**current**, which is a JSON object that stores the current state of the test run with
artifacts - a report on the current test run.

## Statestore scheme

<h1 align="center">
    <img src="https://raw.githubusercontent.com/everypinio/hardpy/main/docs/img/database/statestore.png" alt="statestore_scheme">
</h1>

The **runstore** database is similar to **statestore** database, but there are differences:

- **runstore** contains the **artifact** field for test run, module, and case;
- **runstore** does not contain **dialog_box** and **attempt** fields.

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
- **operator_data** operator panel data, like a dialog box data;
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
      "operator_data": {
        "dialog": ""
      },
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
