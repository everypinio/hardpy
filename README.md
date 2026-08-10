<h1 align="center">Jig</h1>

<p align="center">
    <b>Python test benches for hardware, with an operator panel people enjoy using.</b>
</p>

<p align="center">
Write your tests with <a href="https://docs.pytest.org/">pytest</a>, run them from the browser,
and let the operator pick exactly the group of tests or features to execute.
</p>

<p align="center">
    <img src="https://img.shields.io/badge/python-%3E%3D3.10-blue" alt="python versions">
    <img src="https://img.shields.io/badge/pytest-%3E%3D7.0-blue" alt="pytest versions">
    <img src="https://img.shields.io/badge/license-GPL--3.0--or--later-blue" alt="license">
    <a href="https://github.com/everypinio/hardpy"><img src="https://img.shields.io/badge/fork%20of-HardPy-ff69b4" alt="fork of HardPy"></a>
</p>

---

## About this fork

**Jig** is a fork of [HardPy](https://github.com/everypinio/hardpy) focused on improving the
user experience of running a test bench.

What the fork aims to add:

* A web GUI that organizes tests into categories, so an operator can run only a chosen
  group of tests or a set of features instead of the whole suite.

Everything documented below is inherited from HardPy and still applies.

## Overview

Jig allows you to:

* Create test benches for devices using [pytest](https://docs.pytest.org/);
* Use a browser to view, start, stop, and interact with tests;
* Store test results in the [CouchDB](https://couchdb.apache.org/) database or to simple JSON files;
* Store test results on the [StandCloud](https://standcloud.everypin.io/) analytics platform.

<h1 align="center">
    <img src="https://raw.githubusercontent.com/samuelint/jig/main/docs/img/jig_panel.gif" alt="jig panel" style="width:550px;">
</h1>

## To Install

```bash
pip install pytest-jig
```

The distribution is named `pytest-jig`; the import name and the CLI stay `jig`.
To install the unreleased `main` branch instead:

```bash
pip install git+https://github.com/samuelint/jig.git
```

## Getting Started

### With CouchDB

1. Create your first test bench.
  ```bash
  jig init
  ```
2. Launch [CouchDB](https://couchdb.apache.org/) database via [docker compose](https://docs.docker.com/compose/) 
  in the background.
  ```bash
  cd tests
  docker compose up -d
  ```
3. Launch Jig operator panel.
  ```bash
  jig run
  ```
4. View operator panel in browser: http://localhost:8000/
5. View the latest test report: http://localhost:5984/_utils

    Login and password: **dev**, database - **runstore**.

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

## Examples

From a clone of this repository, any example in the [examples](examples) folder can be
started by name:

```bash
poetry install
poetry run example full_capabilities
```

The operator panel then runs on http://localhost:8000/. Running `poetry run example`
without a name lists what is available.

[full_capabilities](examples/full_capabilities) exercises every feature the panel can
display and needs no database, which makes it the place to try out new ones.

For more examples of using **Jig**, see the [documentation](https://everypinio.github.io/jig/examples/).

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
