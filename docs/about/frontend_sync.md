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

- **runstore** contains the **artifact** field for test run, module, and case.
- **runstore** does not contain some fields: **progress**, **dialog_box**, **attempt**,
  **alert**, **operator_data**, **operator_msg**.

The **current** document of the **statestore** database contains some section.

#### main

- **_rev**: a CouchDB [revision MVCC](https://docs.couchdb.org/en/stable/api/document/common.html) token;
  The variable is assigned automatically.
- **_id**: unique document identifier.
  The variable is assigned automatically.
- **progress**: test run progress.
  The variable is assigned automatically.
- **stop_time**: the end time of the test in Unix seconds. The variable is assigned automatically.
- **start_time**: the start time of the test in Unix seconds. The variable is assigned automatically.
- **status**: test execution status from **pytest**: **passed**, **failed**, **skipped**, **stopped**.
  The variable is assigned automatically.
- **name**: the name of the test suite. It is displayed in the header of the operator panel.
  The user can specify the name using the `tests_name` variable in the **hardpy.toml** file.
  If this variable is not set, the name will be taken from the directory name containing the tests.
- **dut**: DUT information. See the [dut](#dut) section for more information.
- **process** information about the testing process. See the [process](#process) section for more information.
- **modules**: module (pytest files) information. See the [modules](#modules) section for more information.
- **user**: **HardPy** operator panel user name.
  The variable is assigned by [set_user_name](./../documentation/pytest_hardpy.md#set_user_name) function.
  It can only be set once per test run.
- **batch_serial_number**: the serial number of the device batch.
  The variable is assigned by [set_batch_serial_number](./../documentation/pytest_hardpy.md#set_batch_serial_number) function.
  It can only be set once per test run.
- **caused_dut_failure_id**: the ID of the first failed test that caused the test failure.
  Format id: `module_name::case_name`. The variable is assigned automatically.
- **error_code** the error code (non-negative integer) of the caused DUT failure test.
  The variable is assigned by [ErrorCode](./../documentation/pytest_hardpy.md#errorcode) class.
- **test_stand**: test stand information. See the [test_stand](#test_stand) section for more information.
- **modules**: module (pytest files) information. See the [modules](#modules) section for more information.
- **alert**: operator panel alert information.
  Alert information is displayed at the top of the operator panel.
  The variable is assigned automatically.
- **operator_data** operator panel data for operator message.
  This is filled in when the [set_operator_message](./../documentation/pytest_hardpy.md#set_operator_message) function is called.
- **operator_msg**: text of an operator message.
  This is filled in when the [set_operator_message](./../documentation/pytest_hardpy.md#set_operator_message) or
  [clear_operator_message](./../documentation/pytest_hardpy.md#clear_operator_message) functions is called.

#### test_stand

The **test_stand** section contains information about the test stand.
It is a computer on which **HardPy** is running and to which the DUT test equipment is connected.

- **name**: test stand name. It can only be set once per test run.
  The user can specify the stand name by using [set_stand_name](./../documentation/pytest_hardpy.md#set_stand_name) function.
- **revision** test stand revision. It can only be set once per test run.
  The user can specify the stand revision by using [set_stand_revision](./../documentation/pytest_hardpy.md#set_stand_revision) function.
- **drivers**: **DEPRECATED, DO NOT USE IT**.
  Information about drivers in the form of a dictionary, including test equipment and test equipment software.
- **instruments**: list of information about the instruments (i.e. equipment) that form part of the test bench.
  See the [instrument](#instrument) section for more information.
- **drivers**: information about drivers in the form of a dictionary, including test equipment and test equipment software.
  The user can specify the driver info by using [set_driver_info](./../documentation/pytest_hardpy.md#set_driver_info) function.
- **info**: dictionary containing additional information about the test stand.
  The user can specify the additional info by using [set_stand_info](./../documentation/pytest_hardpy.md#set_stand_info) function.
- **timezone**: timezone of test stand as a string. The variable is assigned automatically.
- **location**: the location of the test stand, e.g., the country, city, or laboratory number.
  It can only be set once per test run. The user can specify the location by using
  [set_stand_location](./../documentation/pytest_hardpy.md#set_stand_location) function.
- **number**: test stand number. Some stands may have the same name and
  run on the same computer but have different numbers. It can only be set once per test run.
  The user can specify the stand number by using [set_stand_number](./../documentation/pytest_hardpy.md#set_stand_number) function.
- **hw_id**: test stand machine id (GUID) or host name. The variable is assigned automatically by
  the [py-machineid](https://pypi.org/project/py-machineid/) package

##### instrument

Information about the instrument (i.e equipment) that form part of the test bench.
Information about equipment such as power supplies and voltmeters, which may be used in the test stand, should be stored.
The user can specify the instrument information by using [set_instrument](./../documentation/pytest_hardpy.md#set_instrument) function.

- **name**: instrument name.
- **revision** instrument revision.
- **number**: instrument number.
- **comment**: comment on the instrument.
- **info**: dictionary containing additional information about the instrument.

#### process

Information about the testing process. For example, the device undergoes several stages of testing
during the manufacturing process, including acceptance testing, firmware testing and functional
testing of the board both with and without the case.
Each stage may have its own name, number and other attributes.

- **name**: process name. It can only be set once per test run.
  The user can specify the process name by using [set_process_name](./../documentation/pytest_hardpy.md#set_process_name) function.
- **number**: process number. It can only be set once per test run.
  The user can specify the process number by using [set_process_number](./../documentation/pytest_hardpy.md#set_process_number) function.
- **info**: dictionary containing additional information about the process.
  The user can specify the additional info by using [set_process_info](./../documentation/pytest_hardpy.md#set_process_info) function.

#### dut

The device under test section contains information about the DUT.

- **name**: human-readable name of the DUT.
  The user can specify the DUT name by using [set_dut_name](./../documentation/pytest_hardpy.md#set_dut_name) function.
  It can only be set once per test run.
- **type**: type of DUT, f.e "PCBA", "Casing", etc.
  The user can specify the DUT type by using [set_dut_type](./../documentation/pytest_hardpy.md#set_dut_type) function.
  It can only be set once per test run.
- **serial_number**: DUT serial number. This identifier is unique to the testing device or board.
  It can only be set once per test run.
  The user can specify the DUT serial number by using [set_dut_serial_number](./../documentation/pytest_hardpy.md#set_dut_serial_number) function.
- **part_number**: DUT part number. This identifier of a particular part design, board or device.
  It can only be set once per test run.
  The user can specify the DUT part number by using [set_dut_part_number](./../documentation/pytest_hardpy.md#set_dut_part_number) function.
- **revision**: DUT revision. The user can specify the DUT revision by using
  [set_dut_revision](./../documentation/pytest_hardpy.md#set_dut_revision) function.
  It can only be set once per test run.
- **sub_units**: list of sub units of main DUT. Each sub-unit has a similar structure to the DUT itself, but does not contain any other sub units.
  The user can add the sub unit by using [set_dut_sub_unit](./../documentation/pytest_hardpy.md#set_dut_sub_unit) function.
- **info**: dictionary containing additional information about the the DUT, such as batch, board revision, etc.
  The user can specify the additional info by using [set_dut_info](./../documentation/pytest_hardpy.md#set_dut_info) function.

#### operator_msg

The **operator_msg** section contains operator message data.
The user can open a operator message box by using the [set_operator_message](./../documentation/pytest_hardpy.md#set_operator_message) function.
The user can close a operator message box by using the [clear_operator_message](./../documentation/pytest_hardpy.md#clear_operator_message) function.

- **msg**: message for operator.
- **title**: the title of operator message dialog box.
- **visible**: should a message be displayed on the operator panel.
- **id**: operator message id.
- **font_size**: operator message font size.
- **image**: information about image.
  - **address**: image address.
  - **width**: image width in percent.
  - **border**: image border in pixels.
  - **base64**: image in base64 code.
- **html**: information about html.
  - **code_or_url**: html code or link.
  - **is_raw_html**: is html code is raw.
  - **width**: html width in percent.
  - **border**: html border in pixels.

#### modules

The **modules** section contains the information about tests.
Each module contains information from a single test file.
The module's name is the same as the file's name.

- **test_{module_name}**: an object containing information about a specific module.
  The `{module_name}` variable is assigned automatically.
  Contains the following fields:
  - **status**: module test execution status. The variable is assigned automatically.
  - **name**: module name, by default the same as module_id.
    The user can specify the module name by using [module_name](./../documentation/pytest_hardpy.md#module_name) marker.
  - **start_time**: start time of module testing in Unix seconds. The variable is assigned automatically.
  - **stop_time**: end time of module testing in Unix seconds. The variable is assigned automatically.
  - **group**: the group of module: *Setup*, *Main* or *Teardown* (*Main* by default).
    The user can specify the module group by using [module_group](./../documentation/pytest_hardpy.md#module_group) marker.
  - **cases**: an object that contains information about each test case within the module.
    - **test_{case_name}**: an object containing information about a specific case.
      The `{case_name}` variable is assigned automatically.
      Contains the following fields:
      - **status**: test case execution status. The variable is assigned automatically.
      - **name**: case name, by default the same as case_id.
        The user can specify the case name by using [case_name](./../documentation/pytest_hardpy.md#case_name) marker.
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
        The user can specify and update current message by using [set_message](./../documentation/pytest_hardpy.md#set_message) function.
      - **group**: the group of case: *Setup*, *Main* or *Teardown* (*Main* by default).
        The user can specify the case group by using [case_group](./../documentation/pytest_hardpy.md#case_group) marker.
      - **measurements**: list of measurements.
        See the [measurements](#measurements) section for more information.
      - **attempt**: number of attempts per successful test case.
        The user can specify the case name by using [attempt](./../documentation/pytest_hardpy.md#attempt) marker.
      - **dialog_box**: information about dialog box.
        The user can open a dialog box within a test case by using the [run_dialog_box](./../documentation/pytest_hardpy.md#run_dialog_box) function.
        Data from the dialog box is passed through the [DialogBox](./../documentation/pytest_hardpy.md#DialogBox) class.
        - **title_bar**: title bar of the dialog box.
        - **dialog_text**: text displayed in the dialog box.
        - **widget**: information about the widget.
          - **info**: widget additional information.
          - **type**: type of the widget.
        - **image**: information about image.
          - **address**: image address.
          - **width**: image width in percent.
          - **border**: image border in pixels.
          - **base64**: image in base64 code.
        - **html**: information about html.
          - **code_or_url**: html code or link.
          - **is_raw_html**: is html code is raw.
          - **width**: html width in percent.
          - **border**: html border in pixels.
        - **visible**: should a dialog box be displayed on the operator panel.
        - **id**: dialog box id.
        - **font_size**: dialog box font size.

##### Measurements

The **measurements** section contains the information about measurements.
The user fills in the list of measurements for each case by 
[set_case_measurement](./../documentation/pytest_hardpy.md#set_case_measurement) function.

###### Numeric measurement

A **NumericMeasurement** is a structured container for storing numerical measurements.
For example, the measured voltage must fall within a specific range.

- **type**: `numeric` by default.
- **value**: numeric measure value.
- **name**: numeric measure name.
- **unit**: unit of numeric measure.
- **operation**: comparison operators of numeric measure.
- **comparison_value** value to compare against.
- **lower_limit**: lower limit for range operations.
- **upper_limit** upper limit for range operations.
- **result** the result of the measurement if the operation exists; otherwise, it is empty.
  Filled in without user involvement.

```json
// voltage measure
{
  "type": "numeric",
  "value": "3.57",
  "name": "Main voltage",
  "lower_limit": "3.45",
  "upper_limit": "3.65",
  "unit": "V",
  "operation": "GTLT",
  "result": true
}
```

```json
// temperature measure
{
  "type": "numeric",
  "value": "14",
}
```

###### String measurement

A **StringMeasurement** is a structured container for storing string measurements.
For example, the firmware version comparison.

- **type**: `string` by default.
- **value**: string measure value.
- **name**: string measure name.
- **operation**: comparison operators of string measure.
- **comparison_value** value to compare against.
- **casesensitive**: case sensitivity, default is `True`.
- **result** the result of the measurement if the operation exists; otherwise, it is empty.
  Filled in without user involvement.

```json
{
  "type": "string",
  "value": "3.1.2",
  "operation": "EQ",
  "casesensitive": true,
  "result": true
}
```

### Statestore current document example

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
      "user": null,
      "batch_serial_number": "0613",
      "caused_dut_failure": "test_1_a::test_minute_parity",
      "error_code": null,
      "dut": {
        "name": "analogue",
        "type": "PCBA",
        "serial_number": "92c5a4bb-ecb0-42c5-89ac-e0caca0919fd",
        "part_number": "0507",
        "revision": "rev_1",
        "sub_units": [],
        "info": {
          "sw_version": "3.2.0"
        }
      },
      "test_stand": {
        "hw_id": "840982098ca2459a7b22cc608eff65d4",
        "name": "test_stand_1",
        "revision": "1.0",
        "timezone": "Europe/Belgrade",
        "drivers": {},
        "location": "Belgrade_1",
        "number": 2,
        "instruments": [
          {
            "name": "Everypin Power Supply",
            "revision": "2.0",
            "number": 1,
            "comment": "",
            "info": {}
          }
        ],
        "info": {}
      },
      "operator_msg": {
        "msg": "Operator message",
        "title": "Message",
        "visible": true,
        "id": "f45ac1e7-2ce8-4a6b-bb9d-8863e30bcc78"
      },
      "process": {
        "name": "acceptance",
        "number": 1,
        "info": {}
      },
      "modules": {
        "test_1_a": {
          "status": "failed",
          "name": "Module 1",
          "start_time": 1695816884,
          "stop_time": 1695817265,
          "group": "MAIN",
          "cases": {
            "test_dut_info": {
              "status": "passed",
              "name": "DUT info ",
              "start_time": 1695817263,
              "stop_time": 1695817264,
              "assertion_msg": null,
              "measurements": [],
              "msg": null,
              "group": "MAIN",
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
              "measurements": [],
              "msg": [
                "Current minute 21"
              ],
              "group": "MAIN",
            }
          }
        }
      }
    }
```
