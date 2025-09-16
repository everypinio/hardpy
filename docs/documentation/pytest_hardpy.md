# pytest-hardpy

**pytest-hardpy** is a pytest plugin that helps you save test data in a
database for test reporting and viewing test data in the web interface.

## Plugin registration

To use the **pytest-hardpy** you need to enable it.
You can do this via the `pytest.ini` file.

**Example:**

```ini
# pytest.ini
[pytest]
addopts = --hardpy-pt
```

Another way to enable a plugin without `pytest.ini` file is to run tests with the option `--hardpy-pt`.

```bash
pytest --hardpy-pt tests
```

If tests are run via [hardpy panel](hardpy_panel.md), then the pytest-hardpy plugin will be enabled for tests by default.

## Functions

#### set_user_name

Writes a string with a **HardPy** operator panel user name.
When called again, the exception `DuplicateParameterError` will be raised.

**Arguments:**

- `name` *(str)*: User name

**Example:**

```python
def test_user_name():
    set_user_name("test_operator")
    with pytest.raises(DuplicateParameterError):
        set_user_name("another_operator")
```

#### set_batch_serial_number

Writes a string with the serial number of the device batch.
When called again, the exception `DuplicateParameterError` will be raised.

**Arguments:**

- `serial_number` *(str)*: Batch serial number

**Example:**

```python
def test_batch_number():
    set_batch_serial_number("BATCH-001")
```

#### set_dut_info

This function records a dictionary containing information about the test stand.
When called again, the information will be added to DB.

**Arguments:**

- `info` *(dict)*: DUT info

**Example:**

```python
def test_dut_info():
    set_dut_info({"batch": "test_batch", "board_rev": "rev_1"})
```

#### set_dut_serial_number

Writes a string with a serial number.
When called again, the exception `DuplicateParameterError` will be caused.

**Arguments:**

- `serial_number` *(str)*: DUT serial number

**Example:**

```python
def test_serial_number():
    set_dut_serial_number("1234")
```

#### set_dut_part_number

Writes a string with a part number.
When called again, the exception `DuplicateParameterError` will be caused.

**Arguments:**

- `part_number` *(str)*: DUT part number

**Example:**

```python
def test_part_number():
    set_dut_part_number("part_1")
```

#### set_dut_name

Writes a string with a human-readable name of the DUT.
When called again, the exception `DuplicateParameterError` will be raised.

**Arguments:**

- `name` *(str)*: DUT name

**Example:**

```python
def test_dut_name():
    set_dut_name("Test Device")
```

#### set_dut_type

Writes a string with a type of DUT, f.e "PCBA", "Casing", etc.
When called again, the exception `DuplicateParameterError` will be raised.

**Arguments:**

- `dut_type` *(str)*: DUT type

**Example:**

```python
def test_dut_type():
    set_dut_type("PCBA")
```

#### set_dut_revision

Writes a string with a DUT revision.
When called again, the exception `DuplicateParameterError` will be raised.

**Arguments:**

- `revision` *(str)*: DUT revision (e.g. "REV1.0")

**Example:**

```python
def test_dut_revision():
    set_dut_revision("HW1.0")
```

#### set_dut_sub_unit

Writes a sub unit of DUT.
It accepts a [SubUnit](#subunit) object containing all the details of the sub unit.

**Arguments:**

- `sub_unit` *(SubUnit)*: SubUnit object

**Returns:**

- *(int)*: sub unit index

**Example:**

```python
def test_dut_sub_unit():
    sub_unit = SubUnit(
        serial_number="12345",
        part_number="part_number_1",
        name="Test Device",
        type="PCBA",
        revision="REV1.0",
        info={"sw_version": "1.0"},
    )
    hardpy.set_dut_sub_unit(sub_unit)
```

#### set_dut_revision

Writes a string with a DUT revision.
When called again, the exception `DuplicateParameterError` will be raised.

**Arguments:**

- `revision` *(str)*: DUT revision (e.g. "REV1.0")

**Example:**

```python
def test_dut_revision():
    set_dut_revision("HW1.0")
```

#### set_stand_name

Writes a string with a test stand name.
When called again, the exception `DuplicateParameterError` will be caused.

**Arguments:**

- `name` *(str)*: test stand name

**Example:**

```python
def test_stand_name():
    set_stand_name("name 1")
```

#### set_stand_info

Writes a dictionary with information about the test stand.
When called again, the information will be merged with existing data.

**Arguments:**

- `info` *(Mapping[str, str | int | float ])*: Test stand info dictionary

**Example:**

```python
def test_stand_info():
    set_stand_info({
        "calibration_date": "2023-01-15",
        "temperature": 23.5,
        "firmware_version": "2.1.4"
    })
```

#### set_stand_location

Writes a string with a test stand location.
When called again, the exception `DuplicateParameterError` will be caused.

**Example:**

```python
def test_stand_info():
    set_stand_location("Moon")
```

#### set_stand_number

Writes a integer number with a test stand number.
When called again, the exception `DuplicateParameterError` will be caused.
When called with negative or non-integer number, the exception `TestStandNumberError` will be caused.

**Arguments:**

- `number` *(int)*: test stand number

**Example:**

```python
def test_stand_number():
    set_stand_number(3)
```

#### set_stand_revision

Writes a string with a test stand revision.
When called again, the exception `DuplicateParameterError` will be raised.

**Arguments:**

- `revision` *(str)*: Test stand revision

**Example:**

```python
def test_stand_revision():
    set_stand_revision("HW1.0")
```


#### set_driver_info

**DEPRECATED, DO NOT USE IT.**

The function records a dictionary containing information about the test stand driver.
The data is updated with new information each time the function is called.

Driver data is stored in both **statestore** and **runstore** databases.

**Arguments:**

- `drivers` *(dict)*: A dictionary of drivers, where keys are driver names and values are driver-specific data.

**Example:**

```python
def test_driver_info():
    drivers = {
        "driver_1": {
            "name": "Driver A",
            "type": "network"
        }
    }
    set_driver_info(drivers)
```

#### set_instrument

Adds a new information about the instrument (i.e equipment) that form part of the test bench.

Can be called multiple times to add multiple instruments.
Accepts an [Instrument](#instrument) object containing all instrument details.

**Instrument Parameters:**

- `name` *(str | None)*: Instrument name
- `revision` *(str | None)*: Instrument revision  
- `number` *(int | None)*: Instrument number  
- `comment` *(str | None)*: Instrument comment  
- `info` *(Mapping[str, str | int | float ] | None)*: Additional instrument info 

**Example:**

```python
def test_instruments():
    instrument = Instrument(
        name="Oscilloscope",
        revision="1.2",
        number=1,
        info={"model": "DSO-X 2024A", "bandwidth": "200MHz"}
    )
    set_instrument(instrument)
```

#### set_process_name

Writes a string with a process name.
When called again, the exception `DuplicateParameterError` will be raised.

**Arguments:**

- `name` *(str)*: Process name (e.g. "Production Test")

**Example:**

```python
def test_process():
    set_process_name("Acceptance Test")
```

#### set_process_number

Writes an integer with a process number.
When called again, the exception `DuplicateParameterError` will be raised.

**Arguments:**

- `number` *(int)*: Process number

**Example:**

```python
def test_process():
    set_process_number(1)
```

#### set_process_info

Writes a dictionary with additional information about the process.
When called again, the information will be merged with existing data.

**Arguments:**

- `info` *(Mapping[str, str | int | float ])*: Process info dictionary

**Example:**

```python
def test_process_info():
    set_process_info({
        "stage": "production",
        "version": "1.0",
    })
```

#### set_case_measurement

Writes measurement information to a database in the form of a case measurement list.
When called again, the information will be added to case measurement list.

**Arguments:**

- `measurement` [NumericMeasurement](#numericmeasurement) | 
  [StringMeasurement](#stringmeasurement): measurement data.

**Returns:**

- *(int)*: measurement index

**Example:**

```python
def test_measurement():
    meas_1 = NumericMeasurement(value=10, operation=ComparisonOperation.EQ, comparison_value=10)
    set_case_measurement(meas_1)
    meas_2 = NumericMeasurement(value=3, unit="V", operation=ComparisonOperation.GTLT, lower_limit=2.9, upper_limit=3.5)
    set_case_measurement(meas_2)
    meas_3 = NumericMeasurement(value=1.0)
    set_case_measurement(meas_3)

    assert meas_1.result
    assert meas_2.result

    meas_4 = StringMeasurement(value="1.2.0", operation=ComparisonOperation.EQ, comparison_value="1.2.0")
    set_case_measurement(meas_4)
    assert meas_4.result
```

#### set_case_chart

Writes chart (data series) information to a test case in the database.
Only one [Chart](#chart) object can be stored per test case in the database.
When called again, the exception `DuplicateParameterError` will be raised.

**Arguments:**

- `chart` [Chart](#chart): chart data.

**Example:**

```python
def test_chart():
    chart = hardpy.Chart(
        type=hardpy.ChartType.LINE,
        title="title",
        x_label="x_label",
        y_label="y_label",
        marker_name=["marker_name", None],
        x_data=[ [1, 2], [1, 2] ],
        y_data=[ [3, 4], [3, 4] ]
    )
    hardpy.set_case_chart(chart)
```

#### set_case_artifact

Writes a dictionary with a test case artifact.
When called again, the data will be added to DB.

Artifacts are saved only in the **runstore** database
because the state in **statestore** and case artifact must be separated.

The `set_case_artifact` function must be called from a test case.

**Arguments:**

- `data` *(dict)*: data

**Example:**

```python
def test_case_artifact():
    set_case_artifact({"data_str": "123DATA"})
```

#### set_module_artifact

Writes a dictionary with a module test artifact.
When called again, the data will be added to DB.

Artifacts are saved only in the **runstore** database
because the state in **statestore** and module artifact must be separated.

The `set_module_artifact` function must be called from a test case.

**Arguments:**

- `data` *(dict)*: data

**Example:**

```python
def test_module_artifact():
    set_module_artifact({"data_str": "456DATA"})
```

#### set_run_artifact

Writes a dictionary with a test run artifact.
When called again, the data will be added to DB.

Artifacts are saved only in the **runstore** database
because the state in **statestore** and run artifact must be separated.

**Arguments:**

- `data` *(dict)*: data

**Example:**

```python
def test_run_artifact():
    set_run_artifact({"data_str": "789DATA"})
```

#### set_message

Writes a string with a message.
If a message is sent without a key, the key will be generated
automatically and the messages will be appended.
If the message is sent with a known key, it will be updated.

The `set_message` function must be called from a test case.

**Arguments:**

- `msg` *(str)*: Message content.
- `msg_key` *(Optional[str])*: Message ID. If not specified, a random ID will be generated.

**Example:**

```python
def test_message():
    set_message("Test message")
    set_message("Update message 1", "msg_upd")
    set_message("Update message 2", "msg_upd")
```

#### set_operator_message

Sets an operator message in the **statestore** database and updates the database.
Does not provide user interaction unlike the [run_dialog_box](#run_dialog_box) function.

**Arguments:**

- `msg` *(str)*: The message to be displayed.
- `title` *(str | None)*: The optional title for the message.
- `block` *(bool=True)*: If True, the function will block until the message is closed.
- `image` *([ImageComponent](#imagecomponent) | None)*: Image information.
- `html` *([HTMLComponent](#htmlcomponent) | None)*: HTML information.
- `font_size`: *(int=14)*: Text font size.

**Example:**

```python
from hardpy import set_operator_message

def test_set_operator_msg():
    set_operator_message(msg="This is a sample operator message.", title="Important Notice")
```

#### clear_operator_message

Clears the current message to the operator if it exists, otherwise does nothing.

**Example:**

```python
from time import sleep
from hardpy import set_operator_message, clear_operator_message

def test_clear_operator_msg():
    hardpy.set_operator_message(msg="Clearing operator message.", title="Operator message", block=False)
    sleep(2)
    clear_operator_message()
```

#### run_dialog_box

Displays a dialog box and updates the `dialog_box` field in the **statestore** database.

The `run_dialog_box` function must be called from a test case.

**Arguments:**

- `dialog_box_data` *(DialogBox)*: Data for the dialog box.

**Returns:**

- *(Any)*: An object containing the user's response.

The type of the return value depends on the widget type:

- Without widget (BASE): bool.
- NUMERIC_INPUT: float.
- TEXT_INPUT: str.
- RADIOBUTTON: str.
- CHECKBOX: List(str).
- MULTISTEP: bool.

**Raises**

- `ValueError`: If the `message` argument is empty.

**Example:**

```python
from hardpy import dialog_box
def test_text_input():
    dbx = DialogBox(
        dialog_text="Type 'ok' and press the Confirm button",
        title_bar="Example of text input",
        widget=TextInputWidget(),
        image=ImageComponent(address="assets/test.png", width=50),
    )
    response = run_dialog_box(dbx)
    set_message(f"Entered text {response}")
    assert response == "ok", "The entered text is not correct"
```

#### get_current_report

Returns the current report from the database **runstore**.

**Returns:**

- *(ResultRunStore | None)*: report, or None if not found or invalid

**Example:**

```python
def test_current_report():
    report = get_current_report()
```

#### get_current_attempt

Returns the num of current attempt.

The `get_current_attempt` function must be called from a test case.

**Returns:**

- *(int)*: num of current attempt

**Example:**

```python
@pytest.mark.attempt(5)
def test_attempt_message():
    attempt = hardpy.get_current_attempt()
    hardpy.set_message(f"Current attempt {attempt}")
    if attempt < 5:
        assert False
```

## Class

#### DialogBox

The class is used to configure the dialogue box and is used with
the [run_dialog_box](#run_dialog_box) function.

**Arguments:**

- `dialog_text` *(str)*: The text of the dialog box.
- `title_bar` *(str | None)*: The title bar of the dialog box.
If the title_bar field is missing, it is the case name.
- `widget` *(IWidget | None)*: Widget information.
- `image` *([ImageComponent](#imagecomponent) | None)*: Image information.
- `html` *([HTMLComponent](#htmlcomponent) | None)*: HTML information.
- `font_size`: *(int=14)*: Text font size.

Widget list:

- Base, only dialog text;
- Text input, [TextInputWidget](#textinputwidget);
- Numeric input, [NumericInputWidget](#numericinputwidget);
- Radiobutton, [RadiobuttonWidget](#radiobuttonwidget);
- Checkbox, [CheckboxWidget](#checkboxwidget);
- Multistep, [MultistepWidget](#multistepwidget).

**Example:**

```python
    DialogBox(title_bar="Example title", dialog_text="Example text")
```

#### TextInputWidget

The class is used to configure text input widget in [dialog box](#dialogbox).
Further information can be found in section
[text input field](./hardpy_panel.md/#text-input-field).
Widget returns a string when using [run_dialog_box](#run_dialog_box).

**Example:**

```python
    dbx = DialogBox(
        dialog_text="Type 'ok' and press the Confirm button",
        title_bar="Example of text input",
        widget=TextInputWidget(),
    )
    response = run_dialog_box(dbx)
```

#### NumericInputWidget

The class is used to configure numeric input widget in [dialog box](#dialogbox).
Further information can be found in section
[numeric input field](./hardpy_panel.md/#number-input-field).
Widget returns a float when using [run_dialog_box](#run_dialog_box).

**Example:**

```python
    dbx = DialogBox(
        dialog_text=f"Enter the number {test_num} and press the Confirm button",
        title_bar="Example of entering a number",
        widget=NumericInputWidget(),
    )
    response = int(run_dialog_box(dbx))
```

#### RadiobuttonWidget

The class is used to configure radiobutton widget in [dialog box](#dialogbox).
Further information can be found in section
[radiobutton](./hardpy_panel.md/#radiobutton).
Widget returns a string with the selected radiobutton value
[run_dialog_box](#run_dialog_box).

**Arguments:**

- `fields` *(list[str])*: Radiobutton fields.

**Example:**

```python
    dbx = DialogBox(
        dialog_text='Select item "one" out of several and click Confirm.',
        title_bar="Radiobutton example",
        widget=RadiobuttonWidget(fields=["one", "two", "three"]),
    )
    response = run_dialog_box(dbx)
```

#### CheckboxWidget

The class is used to configure checkbox widget in [dialog box](#dialogbox).
Further information can be found in section
[checkbox](./hardpy_panel.md/#checkbox).
Widget returns a list of string with the selected checkbox value
[run_dialog_box](#run_dialog_box).

**Arguments:**

- `fields` *(list[str])*: Checkbox fields.

**Example:**

```python
    dbx = DialogBox(
        dialog_text='Select items "one" and "two" and click the Confirm button',
        title_bar="Checkbox example",
        widget=CheckboxWidget(fields=["one", "two", "three"]),
    )
    response = run_dialog_box(dbx)
```

#### StepWidget

The class is used to configure the step for the
[multistep](#multistepwidget) widget in [dialog box](#dialogbox).

**Arguments:**

- `title` *(str)*: Step title.
- `text` *(str | None)*: Step text.
- `image` *([ImageComponent](#imagecomponent) | None)*: Step image.
- `html` *([HTMLComponent](#htmlcomponent) | None)*: Step HTML.

**Example:**

```python
    StepWidget("Step 1", text="Content for step")
```

#### MultistepWidget

The class is used to configure multistep widget in [dialog box](#dialogbox).
Further information can be found in section
[multiple steps](./hardpy_panel.md/#multiple-steps).

**Arguments:**

- `steps` *(list[[StepWidget](#stepwidget)])*: A list with info about the steps.

**Example:**

```python
    steps = [
        StepWidget("Step 1", text="Content for step"),
        StepWidget("Step 2", text="Content for step 2", image=ImageComponent(address="assets/test.png", width=100)),
        StepWidget("Step 3", text="Content for step 3", html=HTMLComponent(html="https://everypinio.github.io/hardpy/", width=50)),
    ]
    dbx = DialogBox(dialog_text="Follow the steps and click Confirm", widget=MultistepWidget(steps))
    response = run_dialog_box(dbx)
```

#### ImageComponent

A class for configuring an image for a dialogue box or operator message box and is used with
the [run_dialog_box](#run_dialog_box) and [set_operator_message](#set_operator_message) functions.

**Arguments:**

- `address` *(str)*: Image address.
- `width` *(int | None)*: Image width in %.
- `border` *(int | None)*: Image border width.

**Example:**

```python
    ImageComponent(address="assets/test.png", width=100)
```

#### HTMLComponent

A class for configurating HTML for a dialogue box or operator message box and is used with
the [run_dialog_box](#run_dialog_box) and [set_operator_message](#set_operator_message) functions.

**Arguments:**

- `code_or_url` *(str)*: HTML code or link.
- `width` *(int | None)*: HTML width in %.
- `border` *(int | None)*: HTML border width.
- `is_raw_html` *(bool)*: Is HTML code is raw.

**Example:**

```python
    HTMLComponent(code_or_url="https://everypinio.github.io/hardpy/", width=100, is_raw_html=False)
```

#### CouchdbLoader

Used to write reports to the database **CouchDB**.

Report names (revision id) are automatically generated based on the test
completion date and the device serial number.
If the serial number dut is empty, a random identifier with
prefix `no_serial` is used.
The random identifier is a unique string generated using the `uuid4()`
function from the `uuid` module in Python.
This allows for easy identification and sorting of reports.

* Valid report name: `report_1726496218_1234567890`
* Valid report name (no serial number): `report_1726496218_no_serial_808007`

**Functions:**

- `load` *(ResultRunStore)*: Load report to the CouchDB **report** database.

**Example:**

```python
# conftest
def finish_executing():
    report = get_current_report()
    if report:
        loader = CouchdbLoader(CouchdbConfig())
        loader.load(report)

@pytest.fixture(scope="session", autouse=True)
def fill_actions_after_test(post_run_functions: list):
    post_run_functions.append(finish_executing)
    yield
```

#### StandCloudLoader

Used to write reports to the **StandCloud**.
A login to **StandCloud** is required to work.

**Arguments:**

- `address` *(str | None)*: StandCloud address. Defaults to None
  (the value is taken from [hardpy.toml](./hardpy_config.md)). Can be used outside of **HardPy** applications.

**Functions:**

- `healthcheck`: Healthcheck of StandCloud API.
  Returns the `requests.Response` object.
- `load` *(ResultRunStore)*: Load report to the StandCloud.
  Returns the `requests.Response` object.
  Status code 201 is considered a successful status.

**Example:**

```python
# conftest
def finish_executing():
    report = get_current_report()
    if report:
        try:
            loader = StandCloudLoader()
            response = loader.load(report)
            if response.status_code != HTTPStatus.CREATED:
                set_operator_message(
                    "Report not uploaded to StandCloud, "
                    f"status code: {response.status_code}, text: {response.text}",
                )
        except StandCloudError as exc:
            set_operator_message(f"{exc}")

@pytest.fixture(scope="session", autouse=True)
def fill_actions_after_test(post_run_functions: list):
    post_run_functions.append(finish_executing)
    yield
```

#### StandCloudConnector

Used to create the **StandCloud** connection addresses.

**Arguments:**

- `addr` *(str)*: StandCloud service name.
  For example: **demo.standcloud.io**
- `api_mode` *(StandCloudAPIMode)*: StandCloud API mode:
  **hardpy** for test stand, **integration** for third-party service.
  Default: `StandCloudAPIMode.HARDPY`
- `api_version` *(int)*: StandCloud API version.
  Default: 1.

#### StandCloudReader

Used to read data from the **StandCloud**.
A login to **StandCloud** is required to work.
For more information, see the example [StandCloud reader](./../examples/stand_cloud_reader.md)

**Arguments:**

- `sc_connector` ([StandCloudConnector](#standcloudconnector)): **StandCloud** connection data.

**Functions:**

- `test_run` *(run_id: str, params: dict[str, Any])* - get run data from `/test_run` endpoint.
  All test run filters can view in REST documentation.
  Return `requests.Response` class with test run data.
- `tested_dut` *(params: dict[str, Any])* - get last tested DUT's data from `/tested_dut` endpoint.
  All tested dut's filters can view in REST documentation.
  Return `requests.Response` class with tested DUT's data.

In terms of filters, the difference between `test_run` and `tested_dut` in terms of filters
is that in test_run allows you to request a filter for the number of runs - `number_of_attempt`,
while tested_dut allows you to request a filter for the number of runs - `attempt_count`.
In other words, `tested_dut` will return the last run with the specified number of runs specified in `attempt_count`,
and `test_run` will return the runs whose start number is equal to the `number_of_attempt` specified in the filter.

**Examples:**

```python
    reader = StandCloudReader(StandCloudConnector(addr="demo.standcloud.io"))

    response = reader.test_run(run_id="0196434d-e8f7-7ce1-81f7-e16f20487494")
    status_code = response.status_code
    response_data = response.json()
    print(response_data)

    param = {"part_number": "part_number_1", "status": "pass", "firmware_version": "1.2.3"}
    response = reader.test_run(params=param)
    status_code = response.status_code
    response_data = response.json()
    print(response_data)

    response = reader.tested_dut(param)
    status_code = response.status_code
    response_data = response.json()
    print(response_data)
```

#### Instrument

The class is used to store information about test equipment that forms part of the test bench. 
It is used with the [set_instrument](#set_instrument) function.

**Arguments:**

- `name` *(str | None)*: Instrument name  
- `revision` *(str | None)*: Instrument revision  
- `number` *(int | None)*: Instrument number  
- `comment` *(str | None)*: Instrument comment  
- `info` *(Mapping[str, str | int | float | None)*: Additional instrument info as key-value pairs  

**Returns:**

- *(int)*: instrument index

**Validation Rules:**

- `number` must be positive if specified (≥ 0)

**Example:**

```python
oscilloscope = Instrument(
    name="Oscilloscope",
    revision="1.2.3",
    number=1,
    info={
        "model": "DSO-X 2024A",
        "bandwidth": "200MHz",
    }
)

set_instrument(oscilloscope)
```

#### SubUnit

This class contains information about the sub-unit of the DUT. 
It is used with the [set_dut_sub_unit](#set_dut_sub_unit) function.

**Arguments:**

- `serial_number` *(str | None)*: unit serial number
- `part_number` *(str | None)*: unit part number
- `name` *(str | None)*: unit name  
- `type` *(str | None)*: unit type
- `revision` *(str | None)*: unit revision  
- `info` *(Mapping[str, str | int | float ] | None)*: additional unit info as key-value pairs  

**Example:**

```python
def test_dut_sub_unit():
    sub_unit = SubUnit(
        serial_number="12345",
        part_number="part_number_1",
        name="Test Device",
        type="PCBA",
        revision="REV1.0",
        info={"sw_version": "1.0"},
    )
    hardpy.set_dut_sub_unit(sub_unit)
```

### NumericMeasurement

This class contains information about numeric measurement. 
It is used with the [set_case_measurement](#set_case_measurement) function.

**Arguments:**

- `value` *(float | int)*: numeric measure value.
- `name` *(str | None)*: numeric measure name.
- `unit` *(str | None)*: unit of numeric measure.
- `operation`: comparison operators of numeric measure.
- `comparison_value` *(ComparisonOperation | None)*: value to compare against.
- `lower_limit`: *(float | int)*: lower limit for range operations.
- `upper_limit` *(float | int)*:upper limit for range operations.

**Returns:**

- *(int)*: measurement index

**Example:**

```python
def test_measurement():
    meas_1 = NumericMeasurement(value=10, operation=ComparisonOperation.EQ, comparison_value=10)
    set_case_measurement(meas_1)
    meas_2 = NumericMeasurement(value=3, unit="V", operation=ComparisonOperation.GTLT, lower_limit=2.9, upper_limit=3.5)
    set_case_measurement(meas_2)
    meas_3 = NumericMeasurement(value=1.0)
    set_case_measurement(meas_3)

    assert meas_1.result
    assert meas_2.result
```

### StringMeasurement

This class contains information about string measurement. 
It is used with the [set_case_measurement](#set_case_measurement) function.

**Arguments:**

- `value` *(str)*: string measure value.
- `name` *(str | None)*: string measure name.
- `operation`: comparison operators of string measure (**EQ** and **NE**).
- `comparison_value`: *(ComparisonOperation | None)*: value to compare against.
- `casesensitive`: *bool=True*: case sensitivity.

**Example:**

```python
def test_measurement():
    meas_1 = StringMeasurement(value="1.2.0", operation=ComparisonOperation.EQ, comparison_value="1.2.0")
    set_case_measurement(meas_1)

    meas_2 = StringMeasurement(value="abc", operation=ComparisonOperation.EQ, casesensitive=False, comparison_value="ABC")
    set_case_measurement(meas_2)

    assert meas_1.result
    assert meas_2.result
```

### Chart

This class contains information about chart (data series). 
It is used with the [set_case_chart](#set_case_chart) function.

A `ValidationError` will result if the lengths of x_data, y_data, and marker_name differ.

**Arguments:**

- `type` *([ChartType](#charttype))*: chart type, LINE by default.
- `title` *(str | None)*: chart title.
- `x_label` *(str | None)*: x label name.
- `y_label` *(str | None)*: y label name.
- `marker_name` *(list[str | None])*: data series marker name.
- `x_data` *(list[list[int | float]])*: x data series. Each data series is its own list.
- `y_data` *(list[list[int | float]])*: y data series. Each data series is its own list.

**Functions:**

- `add_series` *(x_data: list[int | float], y_data:* 
  *list[int | float], marker_name: str | None = None)*: add data series to current `Chart`. 

**Example:**

```python
def test_chart():
    chart = hardpy.Chart(
        type=hardpy.ChartType.LINE,
        title="title",
        x_label="x_label",
        y_label="y_label",
        marker_name=["marker_name", None],
        x_data=[ [1, 2], [1, 2] ],
        y_data=[ [3, 4], [3, 4] ]
    )
    chart.add_series(x_data=[0, 3], y_data=[2, 4], marker_name="A")
    hardpy.set_case_chart(chart)
```

### ErrorCode

This class saves the error code of the test plan to the database.
Only the first error code from this class is saved.

The `ErrorCode` class must be called from the `assert`. 
Otherwise, an extra error code may be saved.

**Arguments:**

- `error_code` *(int)*: error code (non-negative integer).
- `message` *(str | None)*: error code message.

**Example:**

```python
def test_error_code():
    assert False, hardpy.ErrorCode(1, "error code message")
```

## Enum

### ComparisonOperation

A comparison operation for the measurements.

**Values:**

- *EQ*: equal.
- *NE*: not equal.
- *GT*: greater than.
- *GE*: greater or equal.
- *LT*: less than.
- *LE*: less or equal.
- *GTLT*: greater than lower limit, less than upper limit.
- *GELE*: greater or equal than lower limit, less or equal than upper limit.
- *GELT*: greater or equal than lower limit, less than upper limit.
- *GTLE*: greater than lower limit, less or equal than upper limit.
- *LTGT*: less than lower limit or greater than upper limit.
- *LEGE*: less or equal than lower limit or greater or equal than upper limit.
- *LEGT*: less or equal than lower limit or greater than upper limit.
- *LTGE*: less than lower limit or greater or equal than upper limit.

### ChartType

This is a chart type for the [Chart](#chart) class.

**Values:**

- *LINE*: line.
- *LINE_LOG_X*: line_log_x.
- *LINE_LOG_Y*: line_log_y.
- *LOG_X_Y*: log_x_y.

## Fixture

#### post_run_functions

To execute actions at the end of testing, you can use the fixture **post_run_functions**.
This fixture is a `list[Callable]` and you can write functions into it that must be executed at the end of testing.

Fill this list in conftest.py and functions from this list will be called after tests run (at the end of pytest_sessionfinish).

**Returns:**

- *(list[Callable])*: list of post run methods

**Example:**

```python
# conftest.py file
def finish_executing():
    print("Pytest finished")


@pytest.fixture(scope="session", autouse=True)
def fill_actions_after_test(post_run_functions: list):
    post_run_functions.append(finish_executing)
    yield
```

#### hardpy_start_args

To access **HardPy** start arguments passed via command line, you can use the `hardpy_start_args` fixture.
This fixture returns a `dict` containing parsed key-value pairs from `--hardpy-start-arg` options.

**Returns:**

- *(dict)*: dictionary of start arguments (key-value pairs)

**Example:**

```python
def test_with_start_args(hardpy_start_args):
   
    if hardpy_start_args.get("test_mode") == "debug":
        hardpy.set_message("Running in debug mode")
```

## Marker

#### case_name

Sets a text name for the test case (default: function name)

**Example:**

```python
@pytest.mark.case_name("Simple case 1")
def test_one():
    assert True
```

#### module_name

Sets a text name for the test module (file) (default: module name)

**Example:**

```python
pytestmark = pytest.mark.module_name("Module 1")
```

#### case_group

Sets the group for a test case. Valid groups: `setup`, `main`, `teardown` (default: `main`)

**Example:**

```python
from hardpy import Group

@pytest.mark.case_group(Group.SETUP)
def test_setup_case():
    assert True

@pytest.mark.case_group("teardown")  
def test_teardown_case():
    assert True
```

#### module_group

Sets the group for all test cases in a module. Valid groups: `setup`, `main`, `teardown` (default: `main`)

**Example:**

```python
import pytest
from hardpy import Group

pytestmark = pytest.mark.module_group(Group.TEARDOWN)

def test_cleanup1():
    assert True

def test_cleanup2():
    assert True
```

#### dependency

Skips the test case/module if the main test fails/skipped/errored.
For more information, see the example [skip test](./../examples/skip_test.md)
and [skip feature description](./../features/features.md#skipping-the-tests).

**Example:**

```python
#test_1.py
def test_one():
    assert False

@pytest.mark.dependency("test_1::test_one")
def test_two():
    assert True
```

#### attempt

If a test is marked `attempt`, it will be repeated if it fails the number of
attempts specified by the mark.
The test will be repeated until it is passed.
There is a 1 second pause between attempts.
For more information, see the example [attempts](./../examples/attempts.md).

**Example:**

```python
@pytest.mark.attempt(5)
def test_attempts():
    assert False
```

#### critical

Marks test or module as critical.
Failing/skipped critical tests skip all subsequent tests.
For implementation details see [critical tests example](./../examples/critical_test.md).

**Example (test level):**

```python
@pytest.mark.critical
def test_core_feature():
    assert check_core_functionality()
```

**Example (module level):**

```python
pytestmark = pytest.mark.critical

def test_db_connection():
    assert connect_to_database()
```

**Behavior:**

- Critical test passes - Continue normally
- Critical test fails/skips - Skip all remaining tests
- Any test fails in critical module - Skip all remaining tests

## Options

**pytest-hardpy** has several options to run:

#### hardpy-pt

Option to enable the **pytest-hardpy** plugin.

```bash
--hardpy-pt
```

#### hardpy-db-url

The CouchDB instance url for the **statestore** and **runstore** databases.
The default is `http://dev:dev@localhost:5984/`.

```bash
--hardpy-db-url
```

#### hardpy-tests-name

The **HardPy** tests name.
The default value is **Tests**.

```bash
--hardpy-tests-name
```

#### hardpy-clear-database

Option to clean **statestore** and **runstore** databases before running pytest.

```bash
--hardpy-clear-database
```

#### sc-address

**StandCloud** address.
The default is empty string.

```bash
--sc-address
```

#### sc-connection-only

Check **StandCloud** service availability.
The default is *False*.

```bash
--sc-connection-only
```

#### hardpy-start-arg

Dynamic arguments for test execution in key=value format. Can be specified multiple times.

```bash
--hardpy-start-arg key=value
```
