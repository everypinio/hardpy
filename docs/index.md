<h1 align="center">
    <img src="https://raw.githubusercontent.com/everypinio/hardpy/main/docs/img/logo256.png" alt="HardPy" style="width:150px;">
</h1>

<p align="center">
HardPy is a python library for creating a test bench for devices.
</p>

---

## Overview

HardPy allows you to:

* Create test benches for devices using [pytest](https://docs.pytest.org/);
* Use a browser to view, start, stop, and interact with tests;
* Store test results in the [CouchDB](https://couchdb.apache.org/) database;
* Store test results on the [StandCloud](https://standcloud.io/) analytics platform.

<h1 align="center">
    <img src="https://raw.githubusercontent.com/everypinio/hardpy/main/docs/img/hardpy_panel.gif" alt="hardpy panel" style="width:600;">
</h1>

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
      <img src="https://raw.githubusercontent.com/everypinio/hardpy/main/docs/img/hardpy_operator_panel_hello_hardpy.png"
      alt="hardpy operator panel" style="width:600px;">
  </h1>
5. View the latest test report: http://localhost:5984/_utils

    Login and password: **dev**, database - **runstore**.

  <h1 align="center">
      <img src="https://raw.githubusercontent.com/everypinio/hardpy/main/docs/img/runstore_hello_hardpy.png"
      alt="hardpy runstore" style="width:500px;">
  </h1>

## Measurement instruments

**HardPy** does not contain any drivers for interacting with measuring equipment. 
However, **HardPy** allows you to work with any Python code, meaning you can use 
open libraries to interact with measuring equipment.

* [InstrumentKit](https://github.com/instrumentkit/InstrumentKit)
* [Instrumental](https://github.com/mabuchilab/Instrumental)
* [PyMeasure](https://github.com/pymeasure/pymeasure)
* [PyTango](https://gitlab.com/tango-controls/pytango)
* [QCoDeS](https://github.com/microsoft/Qcodes)
* [QCoDeS contrib drivers](https://github.com/QCoDeS/Qcodes_contrib_drivers) 
