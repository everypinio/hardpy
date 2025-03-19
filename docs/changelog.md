# Changelog

Versions follow [Semantic Versioning](https://semver.org/): `<major>.<minor>.<patch>`.

* Remove the internal **HardPy** socket on port 6525. Pytest plugin arguments `--hardpy-sh` and `--hardpy-sp`
  are left for backward compatibility with version below 0.10.1.
* Add the ability to add html-pages to dialog boxes and operator messages.

## HardPy 0.10.1

* Fix **StandCloud** authorization process in Windows.

## HardPy 0.10.0

* Add the `[stand_cloud]` section to the **hardpy.toml** configuration file.
* Add the `StandCloudLoader` class to append the test result to the **StandCloud**.
* Add support for **StandCloud** login and logout with `sc-login` and `sc-logout` commands.
* Add **alert** field in **statestore** database.
* Add alert to control panel by calling `set_alert` method in `HardpyPlugin`.

## HardPy 0.9.0

* Add the ability to add images to operator messages like a dialog box.
* Add non-blocking mode for operator message.
* Add `clear_operator_message` function for closing operator message.
* Add **font_size** parameter for operator message and dialog box text.
* Add a 1 second pause between attempts in the `attempt` marker.
* Fix an issue where operator messages and dialog boxes sometimes did not
  open before the browser page reloaded.

## HardPy 0.8.0

* Modify API for dialog boxes with images.
* Add the ability to add images to all widgets.
* Add ability to add borders to images.
* Fix timezone format using the **tzlocal** package.
* Add ability to close `set_operator_message` with `Escape` button.
* Fix skipped test case and module status. Now skipped test status is **skipped**, not **ready**.
* Add an exception when entering the same selection items or step names in dialog boxes.
* Add the ability to clear the **runstore** database before running hardpy
  using the the `--hardpy-clear-database` option of the **pytest-hardpy** plugin.

## HardPy 0.7.0

* Add an **attempt** marker to indicate the number of attempts to run a test before it passes successfully.
* Add a **get_current_attempt** method to get the current attempt number.
* Add the ability to run multiple dialog boxes in a single test.
* Fix the problem of freezing the dialog box in some test cases.
* Add autofocus on dialog boxes (on the **Confirm** button or the first item in the list).
* Remove the **progress** field from the **runstore** database.
* Add the **hw_id** variable to the **test_stand** field in the database obtained from the stand computer.
* Add the **location** variables to the **test_stand** field in the database.
* Move the **timezone** and **driver** database variables to the **test_stand** field.
* Add a schema version. The schema version is fixed to version 1.
* Change **timezone** from two strings to one string.
* Replace the **Flake8** linter with a **Ruff** linter.

## HardPy 0.6.1

* Fix running tests with a simple `pytest` command.

## HardPy 0.6.0

In HardPy, the startup principle has changed compared to version 0.5.0 and lower.
The `hardpy-panel` command is no longer available.

The HardPy project of version 0.6.0 or later must contain the file **hardpy.toml**.

* Add the ability to clear the **statestore** database before running hardpy
  using the the `--hardpy-clear-database` option of the **pytest-hardpy** plugin.
* Add the **name** and **info** fields to **test_stand** in the database schema.
* Add the **part_number** field to **dut** in the database schema.
* Add the **attempt** field to the test case in the database schema.
* Add `set_stand_name` and `set_dut_part_number` functions.
* Add a hardpy template project using the `hardpy init` command.
* Add a hardpy config .toml file - **hardpy.toml**.
* Refactor **pytest-hardpy** plugin options.
* Add CLI to hardpy as an entry point. The `hardpy-panel` command is no longer available.
* Fix use of special characters in dialog boxes. ASCII symbols are passed from frontend to backend.
* Fix status of stopped tests.
* Fix progress bar for skipped tests. Progress bar fills to the end when tests are skipped.
* Add report name generation when serial number is missing.

## HardPy 0.5.1

* Add the ability to work with cloud couchdb via couchdb config.

## HardPy 0.5.0

* Refactor dialog box API.
* Add conda.yaml example.
* Add .vscode folder.
* Fix catching exceptions and displaying them in the operator panel.
* Add dialog box with radiobutton, checkbox, image, multiple steps.

## HardPy 0.4.0

* Add base dialog box, text input and numeric input.
* Add dialog box invocation functionality.
* Add a socket mechanism to transfer data from the uvicorn server to the pytest subprocess.

## HardPy 0.3.0

* Add implementation of test dependencies without using third-party plugins.
* Reduce the number of database calls.
* Speed up test collection.

## HardPy 0.2.0

* Add documentation page.
* Remove the ability to access the `HardPyPlugin`.
  Users can now only register via the ini file.

## HardPy 0.1.0

* Add pytest-hardpy and hardpy panel to the package.
* Add frontend data synchronization via CouchDB data replication to PouchDB.
* Add documentation.
* CouchDB is the main database.
