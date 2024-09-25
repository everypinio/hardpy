# Changelog

Versions follow [Semantic Versioning](https://semver.org/): `<major>.<minor>.<patch>`.

## HardPy 0.5.1

* Add the ability to work with cloud couchdb via couchdb config.

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
