# HardPy structure

**HardPy** includes several parts.

## HardPy CLI

**HardPy CLI** on a [structural scheme](#structural-scheme).

* Entry point for **HardPy**.
* **HardPy** test bench creator.
* Launcher for [operator panel](#hardpy-operator-panel).

For more info, read [CLI](./cli.md).

## HardPy pytest plugin 

**pytest-hardpy** on a [structural scheme](#structural-scheme).

* The pytest wrapper for running pytest from the **HardPy** operator panel.
* The pytest plugin with API for storing data in a database.

For more info, read [pytest-hardpy](./pytest_hardpy.md).

## HardPy operator panel

**hardpy-panel** on a [structural scheme](#structural-scheme).

* Web interface for viewing tests and starting/stopping tests.
* FastAPI application for processing frontend commands.
* PouchDB - web database for synchronizing data from CouchDB and the hardpy operator panel.

For more info, read [hardpy-panel](./hardpy_panel.md).

## CouchDB

* Database to store current test data and store all test results.

For more info, read [database](./database.md).

## Database adapter

* **HardPy** allows you to use a simple database adapter to store test results in CouchDB.
* A developer can create a database adapter to store test results in any database.

## Structural scheme

<figure align="left" width="800">
    <img src="../img/hardpy_struct.drawio.png" alt="hardpy_structure">
    <figcaption align="center">
        Hardpy structure
    </figcaption>
</figure>
