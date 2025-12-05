# HardPy panel

The **hardpy panel** or operator panel is a web interface that displays and controls the testing process in **HardPy**.

## Capability

**HardPy panel** allows you to:

- Start and stop testing;
- Interact with [dialog box](hardpy_panel.md#dialog-box) during testing;
- Browse:
    - Test suite name.
    - Last test run status.
    - Test module name.
    - Duration of test modules execution.
    - Test module status.
    - Test case name.
    - Test case message.
    - Test case status.
- Browse current [statestore](database.md#statestore-scheme) state in debug mode.

### Languages

You can set one of the following operator panel languages ​​via the [configuration file](hardpy_config.md#language):

- English ("en")
- German ("de")
- French ("fr")
- Spanish ("es")
- Chinese ("zh")
- Japanese ("ja")
- Russian ("ru")
- Czech ("cs")

## Usage

### Launch operator panel

Use the [hardpy run](./cli.md#hardpy-run) command to start the web server.
After this open page http://localhost:8000/ in the browser.

When the operator panel is running, you can run tests through the web interface or through
the pytest launcher (in a terminal or from another application).

### Start and stop tests

The operator panel contains a test start/stop button in the lower right corner of the screen.
The user can start/stop tests using the space key.

### Operator panel bar

Operator panel bar displays key system status information in a compact tag-based format.

**Fields:**

- **Stand name** - name of the test stand;
- **Status** - current system status;
- **Start time** - test/operation start timestamp with timezone;
- **Finish time** - completion timestamp with timezone;
- **Alert** - active warning or error message;
- **Test stand info** - additional test stand parameters
  from [set_dut_info](./pytest_hardpy.md#set_dut_info) info;

All fields appear as minimal tags and only display when data is available.

### Settings

The operator panel contains a setting button in the top right corner.

#### debug mode

The user can view the **statestore** database online by clicking on
the **Turn on the debug mode** button.

Debug mode is disabled by default.

#### sound

The user can turn on the sound of the end of the test by clicking on
the **Turn on the sound** button.

Sound can also be enabled by setting `sound_on = true` in the frontend configuration section.
Sound is disabled by default.

### Full-size start/stop button

The operator panel supports a full-size start/stop button layout for improved usability in various scenarios. 
This feature is particularly useful for:

- Touchscreen interfaces
- Mobile devices
- Situations requiring prominent control elements

**Configuration:**
Enable the full-size button in your `hardpy.toml`:

```toml
[frontend]
full_size_button = true
```

=== "Desktop layout"
    <h1 align="center">
        <img src="https://raw.githubusercontent.com/everypinio/hardpy/main/docs/img/full_screen_button_big.png" alt="Full-size button desktop layout" style="width:600px;">
    </h1>

=== "Mobile horizontal"
    <h1 align="center">
        <img src="https://raw.githubusercontent.com/everypinio/hardpy/main/docs/img/full_screen_button_phone_gorizontal.png" alt="Full-size button mobile horizontal" style="width:400px;">
    </h1>

=== "Mobile vertical"
    <h1 align="center">
        <img src="https://raw.githubusercontent.com/everypinio/hardpy/main/docs/img/ful_screen_button_phone_vertical.png" alt="Full-size button mobile vertical" style="width:200px;">
    </h1>

### Manual test selection

The operator panel supports manual test selection, allowing operators to choose specific test cases 
to run instead of executing the entire test plan.

**Features**:

- **Checkbox Interface**: Each test case displays a checkbox for selection in the test suite view.
- **Bulk Selection**: Checkboxes at the module level allow selecting/deselecting all tests in a module. 
- **Visual Indicators**: Selected tests are displayed normally, while non-selected tests are visually muted and marked as `Skipped`.

**Usage**:

1. Enable manual collect mode in your `hardpy.toml`:

```toml
[frontend]
manual_collect = true
```

2. When the operator panel loads, enable **Manual collect on** in the settings
menu - checkboxes will appear next to each test case and module
3. Select the desired tests by checking the corresponding checkboxes
4. Disable manual collect mode by selecting **Manual collect off** in the settings menu
5. Click the start button to run only the selected tests (non-selected tests will be skipped)

**Note**: When manual collect mode is disabled (default), all tests are selected and the checkboxes are hidden.

<h1 align="center">
    <img src="https://raw.githubusercontent.com/everypinio/hardpy/main/docs/img/manual_collect_enabled.png" alt="Manual collect mode enabled" style="width:600px;">
</h1>

### Dialog box

For user interaction with the test, it is possible to use dialog boxes.
An example of usage can be seen in the example [dialog box](../examples/dialog_box.md) and in [dialog box documentation](pytest_hardpy.md#run_dialog_box).
Currently, there are some types of dialog boxes.

Each dialog box can contain an image, HTML page or pass/fail buttons.

* Allows the width to be changed using the `width` parameter.
* Allows changing the border thickness with the `border` parameter.
* Allow the following image types: gif, jpeg, pjpeg, png, svg+xml, tiff, vnd.microsoft.icon, vnd.wap.wbmp, webp.

#### basic dialog box

Contains an instruction or question and a `confirm` button for confirmation.

=== "Widget"
    <h1 align="center">
        <img src="https://raw.githubusercontent.com/everypinio/hardpy/main/docs/img/dialog_box/base_dialog_box.png" alt="base_dialog_box">
    </h1>

=== "Widget with image"
    <h1 align="center">
        <img src="https://raw.githubusercontent.com/everypinio/hardpy/main/docs/img/dialog_box/base_dbx_with_image.png" alt="base_dialog_box_with_image">
    </h1>

=== "Widget with HTML with link"
    <h1 align="center">
        <img src="https://raw.githubusercontent.com/everypinio/hardpy/main/docs/img/dialog_box/dbx_with_html_link.png" alt="base_dialog_box_with_html_link">
    </h1>

=== "Widget with HTML with raw code"
    <h1 align="center">
        <img src="https://raw.githubusercontent.com/everypinio/hardpy/main/docs/img/dialog_box/dbx_with_html_raw_code.png" alt="base_dialog_box_with_html_raw_code">
    </h1>

=== "Widget with pass/fail buttons"
    <h1 align="center">
        <img src="https://raw.githubusercontent.com/everypinio/hardpy/main/docs/img/dialog_box/base_dbx_with_pass_fail.png" alt="base_dialog_box_with_pass_fail">
    </h1>


#### text input field

Contains an instruction or question, a text input field, and a `confirm` button for confirmation.
The text is transmitted in UTF-8 encoding.

=== "Widget"
    <h1 align="center">
        <img src="https://raw.githubusercontent.com/everypinio/hardpy/main/docs/img/dialog_box/text_input_dialog_box.png" alt="text_input_dialog_box">
    </h1>

=== "Widget with image"
    <h1 align="center">
        <img src="https://raw.githubusercontent.com/everypinio/hardpy/main/docs/img/dialog_box/dbx_with_text_input_and_image.png" alt="text_input_dialog_box_with_image">
    </h1>

=== "Widget with HTML"
    <h1 align="center">
        <img src="https://raw.githubusercontent.com/everypinio/hardpy/main/docs/img/dialog_box/dbx_with_text_input_and_html.png" alt="text_input_dialog_box_with_html">
    </h1>

=== "Widget with pass/fail buttons"
    <h1 align="center">
        <img src="https://raw.githubusercontent.com/everypinio/hardpy/main/docs/img/dialog_box/dbx_with_text_input_and_pass_fail.png" alt="text_input_dialog_box_with_pass_fail">
    </h1>

#### number input field

Contains an instruction or question, a number input field, and a `confirm` button for confirmation.

* Allows float numbers with a dot separator.
* Allows negative numbers.
* Allows numbers to be entered using **E notation** with `e`, e.g. `2e3`.
* The entered numbers will be converted to float.

=== "Widget"
    <h1 align="center">
        <img src="https://raw.githubusercontent.com/everypinio/hardpy/main/docs/img/dialog_box/num_input_dialog_box.png" alt="num_input_dialog_box">
    </h1>

=== "Widget with image"
    <h1 align="center">
        <img src="https://raw.githubusercontent.com/everypinio/hardpy/main/docs/img/dialog_box/dbx_with_num_input_and_image.png" alt="num_input_dialog_box_with_image">
    </h1>

=== "Widget with html"
    <h1 align="center">
        <img src="https://raw.githubusercontent.com/everypinio/hardpy/main/docs/img/dialog_box/dbx_with_num_input_and_html.png" alt="num_input_dialog_box_with_html">
    </h1>

=== "Widget with pass/fail buttons"
    <h1 align="center">
        <img src="https://raw.githubusercontent.com/everypinio/hardpy/main/docs/img/dialog_box/dbx_with_num_input_and_pass_fail.png" alt="num_input_dialog_box_with_pass_fail">
    </h1>

#### radiobutton

Contains radiobutton widget.

* The user selects one option from several possible ones.
* Returns the contents of the selected item as a string.


=== "Widget"
    <h1 align="center">
        <img src="https://raw.githubusercontent.com/everypinio/hardpy/main/docs/img/dialog_box/radiobutton_dialog_box.png" alt="radiobutton_dialog_box">
    </h1>

=== "Widget with image"
    <h1 align="center">
        <img src="https://raw.githubusercontent.com/everypinio/hardpy/main/docs/img/dialog_box/dbx_with_radio_and_image.png" alt="radiobutton_dialog_box_with_image">
    </h1>

=== "Widget with html"
    <h1 align="center">
        <img src="https://raw.githubusercontent.com/everypinio/hardpy/main/docs/img/dialog_box/dbx_with_radio_and_html.png" alt="radiobutton_dialog_box_with_html">
    </h1>

=== "Widget with pass/fail buttons"
    <h1 align="center">
        <img src="https://raw.githubusercontent.com/everypinio/hardpy/main/docs/img/dialog_box/dbx_with_radio_and_pass_fail.png" alt="radiobutton_dialog_box_with_pass_fail">
    </h1>

#### checkbox

Contains checkbox widget.

* The user selects several options from several possible ones.
* Returns a list with the contents of the selected items.


=== "Widget"
    <h1 align="center">
        <img src="https://raw.githubusercontent.com/everypinio/hardpy/main/docs/img/dialog_box/checkbox_dialog_box.png" alt="checkbox_dialog_box">
    </h1>

=== "Widget with image"
    <h1 align="center">
        <img src="https://raw.githubusercontent.com/everypinio/hardpy/main/docs/img/dialog_box/dbx_with_checkbox_and_image.png" alt="checkbox_dialog_box_with_image">
    </h1>

=== "Widget with html"
    <h1 align="center">
        <img src="https://raw.githubusercontent.com/everypinio/hardpy/main/docs/img/dialog_box/dbx_with_checkbox_and_html.png" alt="checkbox_dialog_box_with_html">
    </h1>

=== "Widget with pass/fail buttons"
    <h1 align="center">
        <img src="https://raw.githubusercontent.com/everypinio/hardpy/main/docs/img/dialog_box/dbx_with_checkbox_and_pass_fail.png" alt="checkbox_dialog_box_with_pass_fail">
    </h1>

#### multiple steps

Contains an instruction with multiple steps and `confirm` button for confirmation.
Allows steps with text and image.

=== "Step 1"
    <h1 align="center">
        <img src="https://raw.githubusercontent.com/everypinio/hardpy/main/docs/img/dialog_box/dialog_box_with_steps.png" alt="dialog_box_with_steps">
    </h1>

=== "Step 2"
    <h1 align="center">
        <img src="https://raw.githubusercontent.com/everypinio/hardpy/main/docs/img/dialog_box/dialog_box_with_step_with_image.png" alt="dialog_box_with_step_with_image">
    </h1>

=== "Step 3"
    <h1 align="center">
        <img src="https://raw.githubusercontent.com/everypinio/hardpy/main/docs/img/dialog_box/dialog_box_with_step_with_html.png" alt="dialog_box_with_step_with_html">
    </h1>

=== "Step with pass/fail buttons"
    <h1 align="center">
        <img src="https://raw.githubusercontent.com/everypinio/hardpy/main/docs/img/dialog_box/dialog_box_with_step_with_pass_fail.png" alt="dialog_box_with_step_with_pass_fail">
    </h1>

### Operator message

The messages to the operator are similar to [dialog boxes](#dialog-box),
but do not contain a **Confirm** button and can be called outside
the execution of the test plan, for example in case of exception
catching in the `conftest.py` file.
For more information, see the example [operator message](./../examples/operator_msg.md)
or in the function description [set_operator_message](./pytest_hardpy.md#set_operator_message).

#### warning window

If the user clicks `confirm` without entering anything, a warning window will be displayed.

<h1 align="center">
    <img src="https://raw.githubusercontent.com/everypinio/hardpy/main/docs/img/dialog_box/dialog_box_alert.png" alt="alert">
</h1>

#### error notification

If the user closes the dialog box (using the cross in the upper right corner),
the tests will be stopped, an error message will be displayed.

<h1 align="center">
    <img src="https://raw.githubusercontent.com/everypinio/hardpy/main/docs/img/dialog_box/dialog_box_notification.png" alt="notification">
</h1>

### Charts

For visualizing test data, it is possible to use interactive charts.
Charts provide a graphical representation of measurement results and allow operators to analyze data trends in real-time.

Charts support the following features:

* Multiple datasets on a single chart
* Zooming capabilities
* Logarithmic scales for both X and Y axes
* Collapsible/expandable view

#### Basic line chart

Displays a single dataset as a line chart with customizable styling.

<h1 align="center">
    <img src="https://raw.githubusercontent.com/everypinio/hardpy/main/docs/img/charts/basic_line_chart.png" alt="basic_line_chart">
</h1>

#### Multiple datasets

Shows multiple datasets on the same chart for comparative analysis. 
Each dataset can have different colors and styles.

<h1 align="center">
    <img src="https://raw.githubusercontent.com/everypinio/hardpy/main/docs/img/charts/mult_dataset_chart.png" alt="multiple_datasets_chart">
</h1>

#### Collapsed view

Charts can be collapsed to save screen space when not actively being analyzed.

<h1 align="center">
    <img src="https://raw.githubusercontent.com/everypinio/hardpy/main/docs/img/charts/collapsed_chart.png" alt="collapsed_chart">
</h1>

#### Expanded view

Charts can be expanded to full view for detailed analysis.

<h1 align="center">
    <img src="https://raw.githubusercontent.com/everypinio/hardpy/main/docs/img/charts/expanded_chart.png" alt="expanded_chart">
</h1>

#### Logarithmic X-axis

When dealing with data that spans multiple orders of magnitude, the X-axis can be set to logarithmic scale.

<h1 align="center">
    <img src="https://raw.githubusercontent.com/everypinio/hardpy/main/docs/img/charts/chart_log_x.png" alt="logarithmic_x_chart">
</h1>

#### Logarithmic Y-axis

The Y-axis can be set to logarithmic scale for better visualization of exponential data trends.

<h1 align="center">
    <img src="https://raw.githubusercontent.com/everypinio/hardpy/main/docs/img/charts/chart_log_y.png" alt="logarithmic_y_chart">
</h1>

#### Logarithmic X and Y axes

Both axes can be set to logarithmic scale for data that requires logarithmic representation in both dimensions.

<h1 align="center">
    <img src="https://raw.githubusercontent.com/everypinio/hardpy/main/docs/img/charts/chart_log_x_log_y.png" alt="logarithmic_xy_chart">
</h1>

#### Chart interaction

* **Zoom**: Click and drag to select an area to zoom into
* **Pan**: Click and drag to move around the chart when zoomed in
* **Reset zoom**: Double-click to reset to the original view
* **Data points**: Hover over data points to see exact values
* **Legend**: Click on legend items to show/hide specific datasets
* **Download**: Downloading plot as a PNG.

### Test completion modal results

The operator panel now displays comprehensive test completion results through modal windows that provide immediate visual feedback about test outcomes.

**Modal types**:

- **PASS Modal**: Green background with auto-dismiss countdown timer
- **FAIL Modal**: Red background with scrollable list of failed test cases including module names, test case names, and assertion messages
- **STOP Modal**: Yellow background showing the stopped test case details

**User interaction**:

- **Auto-dismiss**: PASS modals automatically close after a configurable timeout (default: 5 seconds)
- **Manual dismissal**: Click anywhere on the modal or press any key to close
- **Space key protection**: Prevents accidental test start/stop during modal display
- **Cooldown period**: Brief delay after modal dismissal before space key actions are enabled

**Configuration**:
Enable and customize modal results in your `hardpy.toml`:

```toml
[frontend.modal_result]
enable = true    
auto_dismiss_pass = true
auto_dismiss_timeout = 15
```

=== "PASS modal result"
    <h1 align="center">
        <img src="https://raw.githubusercontent.com/everypinio/hardpy/main/docs/img/modal_result_pass.png" alt="PASS modal result" style="width:400px;">
    </h1>

=== "FAIL modal result"
    <h1 align="center">
        <img src="https://raw.githubusercontent.com/everypinio/hardpy/main/docs/img/modal_result_fail.png" alt="FAIL modal result" style="width:400px;">
    </h1>

=== "STOP modal result"
    <h1 align="center">
        <img src="https://raw.githubusercontent.com/everypinio/hardpy/main/docs/img/modal_result_stop.png" alt="STOP modal result" style="width:400px;">
    </h1>
