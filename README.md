<h1 align="center">
    <img src="https://everypinio.github.io/hardpy/img/logo512.png" alt="HardPy" style="width:200px;">
</h1>

<h1 align="center">
    <b>HardPy</b>
</h1>

<p align="center">
HardPy is a python library for creating a test bench for devices.
</p>

---

**Documentation**: <a href=https://everypinio.github.io/hardpy/ target="_blank">https://everypinio.github.io/hardpy/</a>

**Source Code**: <a href=https://github.com/everypinio/hardpy target="_blank">https://github.com/everypinio/hardpy</a>

**PyPi**: <a href=https://pypi.org/project/hardpy/ target="_blank">https://pypi.org/project/hardpy/</a>

---

## Overview

HardPy allows you to:

* Create test benches for devices using [pytest](https://docs.pytest.org/);
* Use a browser to view, run, and stop tests;
* Store test results in the [CouchDB](https://couchdb.apache.org/) database.

## To Install

```bash
pip3 install hardpy
```

## Examples

Find examples of using the **HardPy** in the `examples` folder.

## Getting Started

#### CouchDB

This is a simple instruction for Linux.
For Windows, follow the instructions from the
[documentation](https://everypinio.github.io/hardpy/documentation/database/#couchdb-instance).

Launch CouchDB with Docker.
The Docker version must be 24.0.0 or higher.
Create `couchdb.ini` file:

```ini
[chttpd]
enable_cors=true

[cors]
origins = *
methods = GET, PUT, POST, HEAD, DELETE
credentials = true
headers = accept, authorization, content-type, origin, referer, x-csrf-token
```

Run the Docker container from folder with couchdb.ini file:

```bash
docker run --rm --name couchdb -p 5984:5984 -e COUCHDB_USER=dev -e COUCHDB_PASSWORD=dev -v ./couchdb.ini:/opt/couchdb/etc/local.ini couchdb:3.3
```

Command for Windows:

```bash
docker run --rm --name couchdb -p 5984:5984 -e COUCHDB_USER=dev -e COUCHDB_PASSWORD=dev -v .\couchdb.ini:/opt/couchdb/etc/local.ini couchdb:3.3.2
```

#### Test steps

Add simple test to `tests` folder

```python
# test_1.py
import pytest

def test_one():
    assert True
```
#### Operator panel

Launch `hardpy-panel` from tests folder or launch `hardpy-panel tests` and open page http://localhost:8000/ in browser.

<h1 align="center">
    <img src="https://everypinio.github.io/hardpy/img/hardpy_operator_panel_hello_hardpy.png"
    alt="hardpy operator panel" style="width:600px;">
</h1>

#### Test report

The last test report is stored in **runstore** database, document - **current**.
You can view the CouchDB instance through Fauxton web interface: http://localhost:5984/_utils

<h1 align="center">
    <img src="https://everypinio.github.io/hardpy/img/runstore_hello_hardpy.png"
    alt="hardpy runstore" style="width:600px;">
</h1>
