<h1 align="center">
    <img src="https://raw.githubusercontent.com/everypinio/hardpy/main/docs/img/logo256.png" alt="HardPy" style="width:150px;">
</h1>

<p align="center">
HardPy is a python library for creating a test bench for devices.
</p>

<div align="center">

[![PyPI version](https://img.shields.io/pypi/v/hardpy)](https://pypi.org/project/hardpy/)
![python versions](https://img.shields.io/pypi/pyversions/hardpy.svg)
[![pytest versions](https://img.shields.io/badge/pytest-%3E%3D7.0-blue)](https://docs.pytest.org/en/latest/)
[![Documentation](https://img.shields.io/badge/Documentation%20-Overview%20-%20%23007ec6)](https://everypinio.github.io/hardpy/)
[![Reddit](https://img.shields.io/badge/-Reddit-FF4500?style=flat&logo=reddit&logoColor=white)](https://www.reddit.com/r/HardPy)
[![Discord](https://img.shields.io/discord/1304494076799877172?color=7389D8&label&logo=discord&logoColor=ffffff)](https://discord.gg/98bWadmG8J)
[![Telegram](https://img.shields.io/badge/-Telegram-2CA5E0?style=flat&logo=telegram&logoColor=white)](https://t.me/everypin)

</div>

---

## Overview

HardPy allows you to:

* Create test benches for devices using [pytest](https://docs.pytest.org/);
* Use a browser to view, start, stop, and interact with tests;
* Store test results in the [CouchDB](https://couchdb.apache.org/) database or to simple JSON files;
* Store test results on the [StandCloud](https://standcloud.io/) analytics platform.

<h1 align="center">
    <img src="https://raw.githubusercontent.com/everypinio/hardpy/main/docs/img/hardpy_panel.gif" alt="hardpy panel" style="width:550px;">
</h1>

## To Install

```bash
pip install hardpy
```

## Getting Started

### With CouchDB

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
5. View the latest test report: http://localhost:5984/_utils

    Login and password: **dev**, database - **runstore**.

### Without a database

1. Create your first test bench.
```bash
hardpy init --no-create-database --storage-type json
```
2. Launch HardPy operator panel.
```bash
hardpy run
```
3. View operator panel in browser: http://localhost:8000/

## Examples

For more examples of using **HardPy**, see the [examples](https://github.com/everypinio/hardpy/tree/main/examples) folder and the [documentation](https://everypinio.github.io/hardpy/examples/).

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
