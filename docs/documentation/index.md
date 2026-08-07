# Documentation

## Python version

**Jig** is based on the **python 3.10** and supports versions **3.11**, **3.12**, **3.13**.

## Jig structure

**Jig** includes several parts.

### Jig CLI

**Jig CLI** on a [structural scheme](#structural-scheme).

* Entry point for **Jig**.
* **Jig** test bench creator.
* Launcher for [operator panel](#jig-operator-panel).
* **StandCloud** [authorization](./cli.md#sc-login) tool.

For more info, read [CLI](./cli.md).

### Jig pytest plugin

**Jig** includes the pytest-jig plugin for **pytest**.
Compatible with pytest versions above 7.
You can run tests not only through the operator panel but also through the **pytest** itself.

**pytest-jig** on a [structural scheme](#structural-scheme).

* The pytest wrapper for running pytest from the **Jig** operator panel.
* The pytest plugin with API for storing data in a database.

For more info, read [pytest-jig](./pytest_jig.md).

### Jig operator panel

**Jig** includes a **React** application - **Jig operator panel**.
It allows you to use a browser to view and interact with your tests and write test results to a database.

**jig-panel** on a [structural scheme](#structural-scheme).

* Web interface for viewing tests and starting/stopping tests.
* FastAPI application for processing frontend commands.
* PouchDB - web database for synchronizing data from CouchDB and the jig operator panel.

For more info, read [jig-panel](./jig_panel.md).

### CouchDB

**Jig** uses [CouchDB](https://couchdb.apache.org/) as its database but you can write
final result to any database because **CouchDB** stores data in a simple document.
Developers can create their adapter for any database and store the test report in a way that suits them.
By default **Jig** allows you to store all reports in **CouchDB**.
**Jig** is compatible with **CouchDB** versions above 3.2.

* Database to store current test data and store all test results.

For more info, read [database](./database.md).

### Database adapter

* **Jig** allows you to use a simple database adapter to store test results in CouchDB
  using the [CouchdbLoader](./pytest_jig.md#couchdbloader).
* **Jig** allows you to use a [StandCloud](./stand_cloud.md) database adapter to store test results in **StandCloud**
  using the [StandCloudLoader](./pytest_jig.md#standcloudloader).
* A developer can create a database adapter to store test results in any database.

### Structural scheme

<figure align="left" width="800">
    <img src="https://raw.githubusercontent.com/everypinio/jig/main/docs/img/jig_struct.drawio.png" alt="jig structure">
    <figcaption align="center">
        Jig structure
    </figcaption>
</figure>
