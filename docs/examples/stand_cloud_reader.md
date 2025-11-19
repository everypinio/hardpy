# StandCloud reader

???+ warning
    The information on this page is currently out of date!

**HardPy** allows you to read test data from the **StandCloud**.
For this purpose, the [StandCloudReader](./../documentation/pytest_hardpy.md#standcloudreader)
class is available in **HardPy**, which provides access to the REST API of the **StandCloud** service.
To read data from the **StandCloud**, the user must log in to the **StandCloud**
using the [hardpy sc-login](./../documentation/cli.md#sc-login).

To view the REST API documentation, the user can navigate to the format page
https://service_name/integration/api/v1/docs,
where `service_name` is the address of the **StandCloud** client.

Example of documentation page address: https://demo.standcloud.io/integration/api/v1/docs

To access **StandCloud**, contact **info@everypin.io**.

## Functions

### test_run

Provides access to 2 endpoints: `/test_run/{test_run_id}` and `/test_run`.
This function does not allow two arguments to be used at the same time.
The argument must be either `run_id` or the filter `params`.

**run_id**

Allows the user to retrieve data about a specific test run by its id from `/test_run` URL.
User can get id from [StandCloudLoader.load()](./../documentation/pytest_hardpy.md#standcloudloader)
function.

**Example:**

```python
import hardpy

sc_connector = hardpy.StandCloudConnector(api_key="your_api_key")
reader = hardpy.StandCloudReader(sc_connector)

response = reader.test_run(run_id="0196434d-e8f7-7ce1-81f7-e16f20487494")
print(response.json())
```

Request URL of this example:

```bash
https://demo.standcloud.io/hardpy/api/v1/test_run/0196434d-e8f7-7ce1-81f7-e16f20487494
```

REST API documentation page of this example:

```bash
https://demo.standcloud.io/integration/api/v1/docs
```

**Response data example:**

```json
{
  "test_run_id": "0196434d-e8f7-7ce1-81f7-e16f20487494",
  "test_plan_name": "Test Plan A",
  "serial_number": "SN-98765",
  "part_number": "PN-54321AB",
  "status": "FAIL",
  "status_icon": "❌",
  "number_of_attempt": 1,
  "start_time": "2024-02-20T14:23:45Z",
  "stop_time": "2024-02-20T14:23:45Z",
  "duration": "00:12:34",
  "test_stand_name": "EMC Chamber #2",
  "test_stand_hw_id": "TS-CH45",
  "test_run_artifact": {
    "test_run_parameter": "test_run_value"
  },
  "test_stand_info": {
    "calibration_date": "2025-01-15"
  },
  "dut_info": {
    "manufacturer": "ABC Corp"
  }
}
```

**params**

Allows the user to retrieve data about a test run by filters from `/test_run` URL.
Filters are specified as parameters. A special place is occupied by the filter by field `dut.info`,
which allows to add fields `dut.info` as keys for the filter in the parameters.

The difference between the test run with filters and the tested DUT is described in the
[StandCloudReader](./../documentation/pytest_hardpy.md#standcloudreader) documentation.

**Example:**

```python
import hardpy

sc_connector = hardpy.StandCloudConnector(addr="demo.standcloud.io")
reader = hardpy.StandCloudReader(sc_connector)

param = {
    "part_number": "PN-54321AB",
    "status": "pass",
    "manufacturer": "ABC_Corp",
    "number_of_attempt": 2,
}
response = reader.test_run(params=param)
print(response.json())
```

Request URL of this example:

```bash
https://demo.standcloud.io/hardpy/api/v1/test_run?part_number=PN-54321AB&status=pass&manufacturer=ABC_Corp&number_of_attempt=2
```

REST API documentation page of this example:

```bash
https://demo.standcloud.io/integration/api/v1/docs
```

**Response data example:**

```json
{
  "test_run_id": "0196434d-e8f7-7ce1-81f7-e16f20487494",
  "test_plan_name": "Test Plan A",
  "serial_number": "SN-98765",
  "part_number": "PN-54321AB",
  "status": "FAIL",
  "status_icon": "❌",
  "number_of_attempt": 1,
  "start_time": "2024-02-20T14:23:45Z",
  "stop_time": "2024-02-20T14:23:45Z",
  "duration": "00:12:34",
  "test_stand_name": "EMC Chamber #2",
  "test_stand_hw_id": "TS-CH45",
  "test_run_artifact": {
    "test_run_parameter": "test_run_value"
  },
  "test_stand_info": {
    "calibration_date": "2025-01-15"
  },
  "dut_info": {
    "serial_number": "SN-98765",
    "part_number": "PN-54321AB",
    "info": {
      "manufacturer": "ABC Corp"
    }
  }
}
```

### tested_dut

Allows the user to retrieve data about the **last** tested dut's by filters from `/tested_dut` URL.
Filters are specified as parameters. A special place is occupied by the filter by field `dut.info`,
which allows to add fields `dut.info` as keys for the filter in the parameters.

The difference between the test run with filters and the tested DUT is described in the
[StandCloudReader](./../documentation/pytest_hardpy.md#standcloudreader) documentation.

**Example:**

```python
import hardpy

sc_connector = hardpy.StandCloudConnector(addr="demo.standcloud.io")
reader = hardpy.StandCloudReader(sc_connector)

param = {
    "part_number": "PN-54321AB",
    "status": "pass",
    "manufacturer": "ABC_Corp",
    "attempt_count": 3,
}
response = reader.tested_dut(param)
print(response.json())
```

Request URL of this example:

```bash
https://demo.standcloud.io/hardpy/api/v1/tested_dut?part_number=PN-54321AB&status=pass&manufacturer=ABC_Corp&attempt_count=3
```

REST API documentation page of this example:

```bash
https://demo.standcloud.io/integration/api/v1/docs
```

**Response data example:**

```json
[
  {
    "test_plan_name": "Test run #A",
    "serial_number": "SN-12345",
    "part_number": "PN-54321AB",
    "status": "pass",
    "status_icon": "✅",
    "attempt_count": 1,
    "start_time": "2025-03-28T09:34:05Z",
    "finish_time": "2025-03-28T09:34:55Z",
    "duration": "PT50S",
    "test_stand_name": "EMC Chamber #2",
    "test_stand_hw_id": "TS-CH45",
    "dut_info": {
      "manufacturer": "ABC_Corp"
    },
    "test_stand_info": {
      "calibration_date": "2025-01-15"
    },
    "test_run_artifact": {
      "test_run_parameter": "test_run_value"
    }
  },
  {
    "test_plan_name": "Test run #B",
    "serial_number": "SN-98766",
    "part_number": "PN-54321AB",
    "status": "pass",
    "status_icon": "✅",
    "attempt_count": 1,
    "start_time": "2025-03-28T09:35:05Z",
    "finish_time": "2025-03-28T09:35:55Z",
    "duration": "PT50S",
    "test_stand_name": "EMC Chamber #2",
    "test_stand_hw_id": "TS-CH45",
    "dut_info": {
      "manufacturer": "ABC_Corp"
    },
    "test_stand_info": {
      "calibration_date": "2025-01-15"
    },
    "test_run_artifact": {
      "test_run_parameter": "test_run_value"
    }
  }
]
```
