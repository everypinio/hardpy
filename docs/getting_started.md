# Getting started

## Overview

Jig allows you to:

* Create test benches for devices using [pytest](https://docs.pytest.org/);
* Use a browser to view, start, stop, and interact with tests;
* Store test results in the [CouchDB](https://couchdb.apache.org/) database or to simple JSON files;
* Store test results on the [StandCloud](https://standcloud.everypin.io/) analytics platform.

<h1 align="center">
    <img src="https://raw.githubusercontent.com/everypinio/jig/main/docs/img/jig_panel.gif" alt="jig panel" style="width:600;">
</h1>

## To Install

```bash
pip install pytest-jig
```

The distribution is named `pytest-jig`; the import name and the CLI stay `jig`.

## Launch

### With CouchDB

1. Create your first test bench.
  ```bash
  jig init
  ```
2. Launch [CouchDB](https://couchdb.apache.org/) database via [docker compose](https://docs.docker.com/compose/) 
  in the   background.
  ```bash
  cd tests
  docker compose up -d
  ```
3. Launch Jig operator panel.
  ```bash
  jig run
  ```
4. View operator panel in browser: http://localhost:8000/
  <h1 align="center">
      <img src="https://raw.githubusercontent.com/everypinio/jig/main/docs/img/jig_operator_panel_hello_jig.png"
      alt="jig operator panel" style="width:600px;">
  </h1>
5. View the latest test report: http://localhost:5984/_utils

    Login and password: **dev**, database - **runstore**.

  <h1 align="center">
      <img src="https://raw.githubusercontent.com/everypinio/jig/main/docs/img/runstore_hello_jig.png"
      alt="jig runstore" style="width:500px;">
  </h1>

### Without a database

1. Create your first test bench.
  ```bash
  jig init --no-create-database --storage-type json
  ```
2. Launch Jig operator panel.
  ```bash
  jig run
  ```
3. View operator panel in browser: http://localhost:8000/

## Measurement instruments

**Jig** does not contain any drivers for interacting with measuring equipment. 
However, **Jig** allows you to work with any Python code, meaning you can use 
open libraries to interact with measuring equipment.

* [InstrumentKit](https://github.com/instrumentkit/InstrumentKit)
* [Instrumental](https://github.com/mabuchilab/Instrumental)
* [PyMeasure](https://github.com/pymeasure/pymeasure)
* [PyTango](https://gitlab.com/tango-controls/pytango)
* [QCoDeS](https://github.com/microsoft/Qcodes)
* [QCoDeS contrib drivers](https://github.com/QCoDeS/Qcodes_contrib_drivers)
* [Labgrid](https://github.com/labgrid-project/labgrid)
