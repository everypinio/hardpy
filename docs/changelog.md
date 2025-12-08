# Changelog

Versions follow [Semantic Versioning](https://semver.org/): `<major>.<minor>.<patch>`.

## 0.19.1

* Add a `stop_time` validator function. If a case or module has a start time,
  it must also have a stop time.
  [[PR-237](https://github.com/everypinio/hardpy/pull/237)]
* Add a "Manual mode" string to the tests name if the `manual_collect` 
  setting in the **hardpy.toml** file is set to `true`. 
  [[PR-237](https://github.com/everypinio/hardpy/pull/237)]
* Add a Czech translation of the operator panel.
  [[PR-236](https://github.com/everypinio/hardpy/pull/236)]

## 0.19.0

* Add manual test selection mode allowing users to choose specific 
  tests to run via UI checkboxes.
  [[PR-224](https://github.com/everypinio/hardpy/pull/224)]
* Add multiple test plan configurations.
  [[PR-225]](https://github.com/everypinio/hardpy/pull/225)

## 0.18.3

* Add support for pytest 9.
  [[PR-233](https://github.com/everypinio/hardpy/pull/233)]

## 0.18.2

* Add support for working with macOS.
  [[PR-231](https://github.com/everypinio/hardpy/pull/231)]

## 0.18.1

* Expand the log for the StandCloud data synchronization process.
  [[PR-228](https://github.com/everypinio/hardpy/pull/228)]

## 0.18.0

* Add a mechanism to automatically synchronize test data with the StandCloud platform.
  [[PR-205](https://github.com/everypinio/hardpy/pull/205)]
* Add an authorization mechanism to StandCloud via API keys.
  [[PR-205](https://github.com/everypinio/hardpy/pull/205)]
* Enhance measurement display with mathematical interval notation and proper bracket handling.
  [[PR-226](https://github.com/everypinio/hardpy/pull/226)]
* Add measurement display functionality to operator panel showing numeric and string measurements with name-value-unit formatting.
  [[PR-223](https://github.com/everypinio/hardpy/pull/223)]

## 0.17.1

* Fix issue where when using a large button, it overlaps the content.
  [[PR-219](https://github.com/everypinio/hardpy/pull/219)]

## 0.17.0

* Add a named volume to the **docker-compose.yaml** generator.
  [[PR-216](https://github.com/everypinio/hardpy/pull/216)]
* Add database updating after the alert has been called.
  [[PR-211](https://github.com/everypinio/hardpy/pull/211)]
* Add a handler for JSON objects that cannot be serialized for the database.
  [[PR-211](https://github.com/everypinio/hardpy/pull/211)]
* Add `sound_on` configuration option to the frontend settings for enabling/disabling test completion sound notifications.
  [[PR-208](https://github.com/everypinio/hardpy/pull/208)]
* Add pass/fail button functionality to dialog boxes for manual test verification.
  [[PR-207](https://github.com/everypinio/hardpy/pull/207)]
* Add configurable full-size start/stop button for the operator panel with full-size layout option.
  [[PR-206](https://github.com/everypinio/hardpy/pull/206)]
* Add configurable modal result windows that display test completion status (PASS/FAIL/STOP)
  with auto-dismiss functionality and enhanced keyboard interaction handling.
  [[PR-204](https://github.com/everypinio/hardpy/pull/204)]
* Exclude the `Skipped` status from the `caused_dut_failure_id` reason.
  [[PR-202](https://github.com/everypinio/hardpy/pull/202)]

## 0.16.0

* Add error code cleanup in the `attempts`.
  [[PR-200](https://github.com/everypinio/hardpy/pull/200)]
* Add an event handler for the inability to collect tests and the
  absence of a database launch.
  [[PR-200](https://github.com/everypinio/hardpy/pull/200)]
* Add **unknown** values in the `StandCloudLoader` class.
  [[PR-200](https://github.com/everypinio/hardpy/pull/200)]
* Add the type `None` to info field in the `Dut`, `SubUnit`, `Instrument`,
  and `TestStand` tables.
  [[PR-200](https://github.com/everypinio/hardpy/pull/200)]
* Add `serial_number` and `part_number` to the **Instrument** table.
  [[PR-200](https://github.com/everypinio/hardpy/pull/200)]
* Update js packages.
  [[PR-197](https://github.com/everypinio/hardpy/pull/197)]
* Add the charts view to the HardPy operator panel.
  [[PR-186](https://github.com/everypinio/hardpy/pull/186)]
* Added storage of the operator message state to avoid reopening the window after closing.
  [[PR-190](https://github.com/everypinio/hardpy/pull/190)]
* Change the database and interface synchronization mechanism.
  The **statestore** and **runstore** databases can contain multiple documents,
  which are defined by the frontend host name and port.
  The **current** document is no longer being created.
  The name of the document in the database consists of the
  host name and port for the frontend, as described in the **hardpy.toml** file.
  [[PR-187](https://github.com/everypinio/hardpy/pull/187)]
* Simplify the process of working with multiple **HardPy** instances by
  using a single **CouchDB** instance instead of multiple instances.
  [[PR-187](https://github.com/everypinio/hardpy/pull/187)]

## HardPy 0.15.2

* Change the logic of the test case attempts.
  The test case fields (msg, assertion_message, chart, measurements, and artifact)
  are now cleared when the test case passes on the second or subsequent attempt.
  The error code is now cleared when a test case passes on the second or subsequent attempt.
  [[PR-192](https://github.com/everypinio/hardpy/pull/192)]

## HardPy 0.15.1

* Remove the `datetime` type from the info fields in all tables.
  [[PR-188](https://github.com/everypinio/hardpy/pull/188)]

## HardPy 0.15.0

* Remove `tests_dir` variable from **hardpy.toml**. 
  [[PR-182](https://github.com/everypinio/hardpy/pull/182)]
* Add check for message presence in set_operator_message.
  [[PR-180](https://github.com/everypinio/hardpy/pull/180)]
* Add the `ErrorCode` class.
  [[PR-180](https://github.com/everypinio/hardpy/pull/180)]
* Add the ability to store charts (data series) in the database.
  Add `set_case_chart` function and `Chart` class.
  [[PR-179](https://github.com/everypinio/hardpy/pull/179)]
* Add arguments for `hardpy start`.
  [[PR-175](https://github.com/everypinio/hardpy/pull/175)]
* Add numeric and string measurements: `set_case_measurement` function and
  `NumericMeasurement` and `StringMeasurement` classes.
  [[PR-177](https://github.com/everypinio/hardpy/pull/177)]
* Update database schema by **SubUnit** table.
  [[PR-174](https://github.com/everypinio/hardpy/pull/174)]
* Add `set_dut_sub_unit` function.
  [[PR-174](https://github.com/everypinio/hardpy/pull/174)]
* Add markers `case_group` and `module_group`.
  [[PR-173](https://github.com/everypinio/hardpy/pull/173)]
* Add functions: `set_user_name`, `set_batch_serial_number`, `set_stand_revision`, `set_instrument`
  `set_process_name`, `set_process_number`, `set_process_info`, `set_dut_name`, `set_dut_type`,
  `set_dut_revision`, `set_stand_info`.
  [[PR-172](https://github.com/everypinio/hardpy/pull/172)]
* Change `DuplicateSerialNumberError` and `DuplicatePartNumberError` to `DuplicateParameterError`.
  [[PR-172](https://github.com/everypinio/hardpy/pull/172)]
* Update database schema by some tables: **Process**, **Instrument**, **NumericMeasurement**.
  [[PR-162](https://github.com/everypinio/hardpy/pull/162)]
* Update database schema by some fields: **user**, **batch_serial_number**, **caused_dut_failure_id**, **error_code**
  **process**, **revision**, **instruments**, **group**, **measurements**.
  [[PR-162](https://github.com/everypinio/hardpy/pull/162)]
* Add the `caused_dut_failure_id` logic to the filling process.
  [[PR-162](https://github.com/everypinio/hardpy/pull/162)]

## HardPy 0.14.0

* Add status display in words depending on the testing status.
  [[PR-165](https://github.com/everypinio/hardpy/pull/165)]
* Add a timeout to the `load` function of the `StandCloudLoader` class.
  [[PR-166](https://github.com/everypinio/hardpy/pull/166)]
* Fix logic for processing spacebar pressing.
  [[PR-164](https://github.com/everypinio/hardpy/pull/164)]
* Fix the display of the module duration after the operator panel has been restarted.
  [[PR-163](https://github.com/everypinio/hardpy/pull/163)]
* Add the display of last test run duration.
  [[PR-163](https://github.com/everypinio/hardpy/pull/163)]
* Add the option to translate the HardPy operator panel using ISO 639 language codes.
  [[PR-159](https://github.com/everypinio/hardpy/pull/159)]

## HardPy 0.13.0

* Change CI settings, add testing of tests on different versions of packages.
  [[PR-157](https://github.com/everypinio/hardpy/pull/157)]
* Add an alert to operator panel when the following are called not from tests:
  `set_message`, `set_case_artifact`, `set_module_artifact`, `run_dialog_box`,
  and `get_current_attempt`.
  [[PR-154](https://github.com/everypinio/hardpy/pull/154)]
* Update the status of the test case and module when the test stops.
  Only one case and one module receive the "stopped" status, while the rest are marked as "skipped."
  [[PR-154](https://github.com/everypinio/hardpy/pull/154)]
* Change **StandCloud** authorization process to OAuth2 Device Flow by
  [RFC8628](https://datatracker.ietf.org/doc/html/rfc8628).
  [[PR-152](https://github.com/everypinio/hardpy/pull/152)]

## HardPy 0.12.1

* Fix the situation in which the module and case stop times stop updating when the user stops the tests.
  [[PR-149](https://github.com/everypinio/hardpy/pull/149)]

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
