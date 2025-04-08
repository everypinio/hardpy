# Documentation

## Python version

**HardPy** is based on the **python 3.10** and supports versions **3.11**, **3.12**, **3.13**.

## HardPy structure

**HardPy** includes several parts.

### HardPy CLI

**HardPy CLI** on a [structural scheme](#structural-scheme).

* Entry point for **HardPy**.
* **HardPy** test bench creator.
* Launcher for [operator panel](#hardpy-operator-panel).
* **StandCloud** [authorization](./cli.md#sc-login) tool.

For more info, read [CLI](./cli.md).

### HardPy pytest plugin

**HardPy** includes the pytest-hardpy plugin for **pytest**.
Compatible with pytest versions above 7.
You can run tests not only through the operator panel but also through the **pytest** itself.

**pytest-hardpy** on a [structural scheme](#structural-scheme).

* The pytest wrapper for running pytest from the **HardPy** operator panel.
* The pytest plugin with API for storing data in a database.

For more info, read [pytest-hardpy](./pytest_hardpy.md).

### HardPy operator panel

**HardPy** includes a **React** application - **HardPy operator panel**.
It allows you to use a browser to view and interact with your tests and write test results to a database.

**hardpy-panel** on a [structural scheme](#structural-scheme).

* Web interface for viewing tests and starting/stopping tests.
* FastAPI application for processing frontend commands.
* PouchDB - web database for synchronizing data from CouchDB and the hardpy operator panel.

For more info, read [hardpy-panel](./hardpy_panel.md).

### CouchDB

**HardPy** uses [CouchDB](https://couchdb.apache.org/) as its database but you can write
final result to any database because **CouchDB** stores data in a simple document.
Developers can create their adapter for any database and store the test report in a way that suits them.
By default **HardPy** allows you to store all reports in **CouchDB**.
**HardPy** is compatible with **CouchDB** versions above 3.2.

* Database to store current test data and store all test results.

For more info, read [database](./database.md).

### Database adapter

* **HardPy** allows you to use a simple database adapter to store test results in CouchDB
  using the [CouchdbLoader](./pytest_hardpy.md#couchdbloader).
* **HardPy** allows you to use a [StandCloud](./stand_cloud.md) database adapter to store test results in **StandCloud**
  using the [StandCloudLoader](./pytest_hardpy.md#standcloudloader).
* A developer can create a database adapter to store test results in any database.

### Structural scheme

<figure align="left" width="800">
    <img src="https://raw.githubusercontent.com/everypinio/hardpy/main/docs/img/hardpy_struct.drawio.png" alt="hardpy structure">
    <figcaption align="center">
        HardPy structure
    </figcaption>
</figure>
