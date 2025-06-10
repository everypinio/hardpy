# Changelog

Versions follow [Semantic Versioning](https://semver.org/): `<major>.<minor>.<patch>`.

* Update parallel tests example.
  [[PR-150](https://github.com/everypinio/hardpy/pull/150)]

## HardPy 0.12.0

* Update `test_run` **StandCloudReader** function.
  The `test_run` function provides access to 2 endpoints: `/test_run/{test_run_id}` and `/test_run`.
  [[PR-145](https://github.com/everypinio/hardpy/pull/145)]
* Update database scheme description.
  [[PR-140](https://github.com/everypinio/hardpy/pull/140)]
* Add test stand number by using `set_stand_number` function.
  [[PR-140](https://github.com/everypinio/hardpy/pull/140)]
* Add prohibition to run tests on the port if the port is busy.
  [[PR-136](https://github.com/everypinio/hardpy/pull/136)]
* Add marker **critical**.
  [[PR-135](https://github.com/everypinio/hardpy/pull/135)],
  [[PR-142](https://github.com/everypinio/hardpy/pull/142)],
  [[PR-143](https://github.com/everypinio/hardpy/pull/143)]
* Change dependency behaviour when a case or module name does not exist.
  Such a test or module will be executed.
  [[PR-130](https://github.com/everypinio/hardpy/pull/130)]
* Add the ability to add dependency from multiple tests.
  [[PR-130](https://github.com/everypinio/hardpy/pull/130)]
* Transfer frontend from CRA to Vite.
  [[PR-122](https://github.com/everypinio/hardpy/pull/122)]
* Remove bug with scrolling tests with operator messages.
  [[PR-122](https://github.com/everypinio/hardpy/pull/122)]
* Logging to **pytest.ini** is no longer configured during **HardPy** project initialization by `hardpy init`.
  [[PR-122](https://github.com/everypinio/hardpy/pull/122)]

## HardPy 0.11.2

* Fix StandCloud login support in version 3.12+.
  [[PR-134](https://github.com/everypinio/hardpy/pull/134)]

## HardPy 0.11.1

* Change **StandCloud** URL for publish test report to `/test_report`.
  [[PR-131](https://github.com/everypinio/hardpy/pull/131)]
* Add `StandCloudReader` class for reading data from **StandCloud**.
  [[PR-131](https://github.com/everypinio/hardpy/pull/131)]
* Fix the behavior with empty module start time with skipped test.
  [[PR-131](https://github.com/everypinio/hardpy/pull/131)]
* Fix the behavior with empty module stop time with skipped test.
  [[PR-129](https://github.com/everypinio/hardpy/pull/129)]
* Add Stand info to Operator panel.
  [[PR-127](https://github.com/everypinio/hardpy/pull/127)]
* Add the `tests_name` field to **hardpy.toml**.
  The `tests_name` allows to name the test suite in the operator panel.
  [[PR-126](https://github.com/everypinio/hardpy/pull/126)]
* Add CLI commands: `hardpy start`, `hardpy stop` and `hardpy status`.
  [[PR-126](https://github.com/everypinio/hardpy/pull/126)]
* Change the StandCloud API address to `/hardpy/api`.
  [[PR-125](https://github.com/everypinio/hardpy/pull/125)]

## HardPy 0.11.0

* Remove the internal **HardPy** socket on port 6525. Pytest plugin arguments `--hardpy-sh` and `--hardpy-sp`
  are left for backward compatibility with version below 0.10.1.
  [[PR-114](https://github.com/everypinio/hardpy/pull/114)]
* Add the ability to add HTML pages using `HTMLComponent` to dialog boxes and operator messages.
  [[PR-104](https://github.com/everypinio/hardpy/pull/104)]

## HardPy 0.10.1

* Fix **StandCloud** authorization process in Windows.
  [[PR-110](https://github.com/everypinio/hardpy/pull/110)]

## HardPy 0.10.0

* Add the `[stand_cloud]` section to the **hardpy.toml** configuration file.
  [[PR-85](https://github.com/everypinio/hardpy/pull/85)]
* Add the `StandCloudLoader` class to append the test result to the **StandCloud**.
  [[PR-85](https://github.com/everypinio/hardpy/pull/85)]
* Add support for **StandCloud** login and logout with `sc-login` and `sc-logout` commands.
  [[PR-85](https://github.com/everypinio/hardpy/pull/85)]
* Add **alert** field in **statestore** database.
  [[PR-85](https://github.com/everypinio/hardpy/pull/85)]
* Add alert to control panel by calling `set_alert` method in `HardpyPlugin`.
  [[PR-85](https://github.com/everypinio/hardpy/pull/85)]

## HardPy 0.9.0

* Add the ability to add images to operator messages like a dialog box.
  [[PR-95](https://github.com/everypinio/hardpy/pull/95)]
* Add non-blocking mode for operator message.
  [[PR-95](https://github.com/everypinio/hardpy/pull/95)]
* Add `clear_operator_message` function for closing operator message.
  [[PR-95](https://github.com/everypinio/hardpy/pull/95)]
* Add **font_size** parameter for operator message and dialog box text.
  [[PR-97](https://github.com/everypinio/hardpy/pull/97)]
* Add a 1 second pause between attempts in the `attempt` marker.
  [[PR-98](https://github.com/everypinio/hardpy/pull/98)]
* Fix an issue where operator messages and dialog boxes sometimes did not
  open before the browser page reloaded.
  [[PR-98](https://github.com/everypinio/hardpy/pull/98)]

## HardPy 0.8.0

* Modify API for dialog boxes with images.
  [[PR-84](https://github.com/everypinio/hardpy/pull/84)]
* Add the ability to add images to all widgets.
  [[PR-84](https://github.com/everypinio/hardpy/pull/84)]
* Add ability to add borders to images.
  [[PR-84](https://github.com/everypinio/hardpy/pull/84)]
* Fix timezone format using the **tzlocal** package.
  [[PR-79](https://github.com/everypinio/hardpy/pull/79)]
* Add ability to close `set_operator_message` with `Escape` button.
  [[PR-84](https://github.com/everypinio/hardpy/pull/84)]
* Fix skipped test case and module status. Now skipped test status is **skipped**, not **ready**.
  [[PR-77](https://github.com/everypinio/hardpy/pull/77)]
* Add an exception when entering the same selection items or step names in dialog boxes.
  [[PR-86](https://github.com/everypinio/hardpy/pull/86)]
* Add the ability to clear the **runstore** database before running hardpy
  using the the `--hardpy-clear-database` option of the **pytest-hardpy** plugin.
  [[PR-83](https://github.com/everypinio/hardpy/pull/83)]

## HardPy 0.7.0

* Add an **attempt** marker to indicate the number of attempts to run a test before it passes successfully.
  [[PR-65](https://github.com/everypinio/hardpy/pull/65)]
* Add a **get_current_attempt** method to get the current attempt number.
  [[PR-65](https://github.com/everypinio/hardpy/pull/65)]
* Add the ability to run multiple dialog boxes in a single test.
  [[PR-65](https://github.com/everypinio/hardpy/pull/65)]
* Fix the problem of freezing the dialog box in some test cases.
  [[PR-65](https://github.com/everypinio/hardpy/pull/65)]
* Add autofocus on dialog boxes (on the **Confirm** button or the first item in the list).
  [[PR-65](https://github.com/everypinio/hardpy/pull/65)]
* Remove the **progress** field from the **runstore** database.
  [[PR-66](https://github.com/everypinio/hardpy/pull/66)]
* Add the **hw_id** variable to the **test_stand** field in the database obtained from the stand computer.
  [[PR-67](https://github.com/everypinio/hardpy/pull/67)]
* Add the **location** variables to the **test_stand** field in the database.
  [[PR-66](https://github.com/everypinio/hardpy/pull/66)]
* Move the **timezone** and **driver** database variables to the **test_stand** field.
  [[PR-66](https://github.com/everypinio/hardpy/pull/66)]
* Add a schema version. The schema version is fixed to version 1.
  [[PR-66](https://github.com/everypinio/hardpy/pull/66)]
* Change **timezone** from two strings to one string.
  [[PR-69](https://github.com/everypinio/hardpy/pull/69)]
* Replace the **Flake8** linter with a **Ruff** linter.
  [[PR-58](https://github.com/everypinio/hardpy/pull/58)]

## HardPy 0.6.1

* Fix running tests with a simple `pytest` command.
  [[PR-60](https://github.com/everypinio/hardpy/pull/60)]

## HardPy 0.6.0

In HardPy, the startup principle has changed compared to version 0.5.0 and lower.
The `hardpy-panel` command is no longer available.

The HardPy project of version 0.6.0 or later must contain the file **hardpy.toml**.

* Add the ability to clear the **statestore** database before running hardpy
  using the the `--hardpy-clear-database` option of the **pytest-hardpy** plugin.
  [[PR-49](https://github.com/everypinio/hardpy/pull/49)]
* Add the **name** and **info** fields to **test_stand** in the database schema.
  [[PR-49](https://github.com/everypinio/hardpy/pull/49)]
* Add the **part_number** field to **dut** in the database schema.
  [[PR-49](https://github.com/everypinio/hardpy/pull/49)]
* Add the **attempt** field to the test case in the database schema.
  [[PR-54](https://github.com/everypinio/hardpy/pull/54)]
* Add `set_stand_name` and `set_dut_part_number` functions.
  [[PR-49](https://github.com/everypinio/hardpy/pull/49)]
* Add a hardpy template project using the `hardpy init` command.
  [[PR-44](https://github.com/everypinio/hardpy/pull/44)]
* Add a hardpy config .toml file - **hardpy.toml**.
  [[PR-44](https://github.com/everypinio/hardpy/pull/44)]
* Refactor **pytest-hardpy** plugin options.
  [[PR-44](https://github.com/everypinio/hardpy/pull/44)]
* Add CLI to hardpy as an entry point. The `hardpy-panel` command is no longer available.
  [[PR-44](https://github.com/everypinio/hardpy/pull/44)]
* Fix use of special characters in dialog boxes. ASCII symbols are passed from frontend to backend.
  [[PR-40](https://github.com/everypinio/hardpy/pull/40)]
* Fix status of stopped tests.
  [[PR-45](https://github.com/everypinio/hardpy/pull/45)]
* Fix progress bar for skipped tests. Progress bar fills to the end when tests are skipped.
  [[PR-43](https://github.com/everypinio/hardpy/pull/43)]
* Add report name generation when serial number is missing.
  [[PR-47](https://github.com/everypinio/hardpy/pull/47)]

## HardPy 0.5.1

* Add the ability to work with cloud couchdb via couchdb config.
  [[PR-51](https://github.com/everypinio/hardpy/pull/51)]

## HardPy 0.5.0

* Refactor dialog box API.
  [[PR-33](https://github.com/everypinio/hardpy/pull/33)]
* Add conda.yaml example.
  [[PR-32](https://github.com/everypinio/hardpy/pull/32)]
* Add .vscode folder.
  [[PR-32](https://github.com/everypinio/hardpy/pull/32)]
* Fix catching exceptions and displaying them in the operator panel.
  [[PR-32](https://github.com/everypinio/hardpy/pull/32)]
* Add dialog box with radiobutton, checkbox, image, multiple steps.
  [[PR-29](https://github.com/everypinio/hardpy/pull/29)]
  [[PR-31](https://github.com/everypinio/hardpy/pull/31)]
  [[PR-31](https://github.com/everypinio/hardpy/pull/31)]

## HardPy 0.4.0

* Add base dialog box, text input and numeric input.
  [[PR-24](https://github.com/everypinio/hardpy/pull/24)]
* Add dialog box invocation functionality.
  [[PR-25](https://github.com/everypinio/hardpy/pull/25)]
* Add a socket mechanism to transfer data from the uvicorn server to the pytest subprocess.
  [[PR-25](https://github.com/everypinio/hardpy/pull/25)]

## HardPy 0.3.0

* Add implementation of test dependencies without using third-party plugins.
  [[PR-15](https://github.com/everypinio/hardpy/pull/15)]
* Reduce the number of database calls.
  [[PR-12](https://github.com/everypinio/hardpy/pull/12)]
* Speed up test collection.
  [[PR-12](https://github.com/everypinio/hardpy/pull/12)]

## HardPy 0.2.0

* Add documentation page.
  [[PR-5](https://github.com/everypinio/hardpy/pull/5)]
* Remove the ability to access the `HardPyPlugin`.
  Users can now only register via the ini file.
  [[PR-6](https://github.com/everypinio/hardpy/pull/6)]

## HardPy 0.1.0

* Add pytest-hardpy and hardpy panel to the package.
  [[PR-1](https://github.com/everypinio/hardpy/pull/1)]
* Add frontend data synchronization via CouchDB data replication to PouchDB.
  [[PR-1](https://github.com/everypinio/hardpy/pull/1)]
* Add documentation.
  [[PR-1](https://github.com/everypinio/hardpy/pull/1)]
* CouchDB is the main database.
  [[PR-1](https://github.com/everypinio/hardpy/pull/1)]
