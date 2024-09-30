<h1 align="center">
    <img src="https://everypinio.github.io/hardpy/img/logo256.png" alt="HardPy" style="width:200px;">
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
* Use a browser to view, start, stop, and interact with tests;
* Store test results in the [CouchDB](https://couchdb.apache.org/) database.

## To Install

```bash
pip install hardpy
```

## Getting Started

1. Create your first test bench.
```bash
hardpy init
```
2. Launch [CouchDB](https://couchdb.apache.org/) database via [docker compose](https://docs.docker.com/compose/) in the background.
```bash
cd tests
docker compose up -d
```
3. Launch HardPy operator panel.
```bash
hardpy run
```
4. View operator panel in browser: http://localhost:8000/

  <h1 align="center">
      <img src="https://everypinio.github.io/hardpy/img/hardpy_operator_panel_hello_hardpy.png"
      alt="hardpy operator panel" style="width:600px;">
  </h1>

5. View the latest test report: http://localhost:5984/_utils

    Login and password: **dev**, database - **runstore**, document - **current**.

  <h1 align="center">
      <img src="https://everypinio.github.io/hardpy/img/runstore_hello_hardpy.png"
      alt="hardpy runstore" style="width:500px;">
  </h1>

## Examples

Find more examples of using the **HardPy** in the [examples](https://github.com/everypinio/hardpy/tree/main/examples) folder.
