# Changelog

Versions follow [Semantic Versioning](https://semver.org/): `<major>.<minor>.<patch>`.

* Add a hardpy template project using the `hardpy init` command.
* Add hardpy config .toml file.
* Refactor pytest-hardpy plugin options.
* Add CLI to hardpy as an entry point. The `hardpy-panel` command is now unavailable.
* Fix using special characters in dialog boxes. ASCII symbols are passed from frontend to backend.
* Add unit tests for dialog widgets.
* Fix statuses of stopped tests.
* Fix progress bar with skipping tests. Progress bar fills to the end when tests are skipped.

## HardPy 0.5.0

* Refactor dialog box API.
* Add conda.yaml example.
* Add .vscode folder.
* Fix capturing exceptions and displaying them in the operator panel.
* Add dialog box with radiobutton, checkbox, image, multiple steps.

## HardPy 0.4.0

* Add base dialog box, text input and numeric input.
* Add dialog box invocation functionality.
* Add a socket mechanism to transfer data from the uvicorn server to the pytest subprocess.

## HardPy 0.3.0

* Add implementation of test dependencies without using third party plugins.
* Reduce the number of database calls.
* Speed up test collection.

## HardPy 0.2.0

* Add documentation site.
* Remove the ability to access the HardpyPlugin. Users can now only register through the ini file.

## HardPy 0.1.0

* Add pytest-hardpy and hardpy panel into one package.
* Add frontend data synchronization via CouchDB data replication to PouchDB.
* Add documentation.
* CouchDB is main database.
