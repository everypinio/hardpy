# HardPy panel

The **hardpy panel** or operator panel is a web interface that displays and controls the testing process in **HardPy**.

## Capability

**HardPy panel** allows you to:

- Start and stop testing;
- Interact with [dialog box](hardpy_panel.md#dialog-box) during testing;
- Browse:
    - Test run name.
    - Test run status.
    - Test module name.
    - Duration of test modules execution.
    - Test module status.
    - Test case name.
    - Test case message.
    - Test case status.
- Browse current [statestore](database.md#statestore-scheme) state in debug mode.

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

- **Stand name** - Name of the test stand (from `db_state.test_stand.name`)  
- **Status** - Current system status (from `db_state.status`)  
- **Start time** - Test/operation start timestamp with timezone  
- **Finish time** - Completion timestamp with timezone  
- **Alert** - Active warning or error message  
- **Test stand info** - Additional parameters from test stand configuration (dynamic key-value pairs)  

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

Sound is disabled by default.

### Dialog box

For user interaction with the test, it is possible to use dialog boxes.
An example of usage can be seen in the example [dialog box](../examples/dialog_box.md) and in [dialog box documentation](pytest_hardpy.md#run_dialog_box).
Currently, there are some types of dialog boxes.

Each dialog box can contain an image.

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
