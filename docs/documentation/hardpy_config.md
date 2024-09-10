# HardPy config

**HardPy** uses the `hardpy.toml` file for configuration.
The user can change the fields at creation by using [hardpy init](./cli.md#hardpy-init)

## Default config

```toml
title = "HardPy TOML config"
tests_dir = "tests"

[database]
user = "dev"
password = "dev"
host = "localhost"
port = 5984

[frontend]
host = "localhost"
port = 8000

[socket]
host = "localhost"
port = 6525
```

## Configuration fields description

### common

Common settings.

#### title

Configuration file header.
The value is always `HardPy TOML config`.

#### tests_dir

Tests directory. The default is `tests`.
The user can change this value with the `hardpy init` argument.

### database

Database settings.

#### user

Database user name. The default is `dev`.
The user can change this value with the `hardpy init --database-user` option.

#### password

Database password. The default is `dev`.
The user can change this value with the `hardpy init --database-password` option.

#### host

Database host name. The default is `localhost`.
The user can change this value with the `hardpy init --database-host` option.

#### port 

Database port number. The default is `5984`.
The user can change this value with the `hardpy init --database-port` option.

### frontend

Frontend (operator panel) settings.

#### host

Operator panel host name. The default is `localhost`.
The user can change this value with the `hardpy init --frontend-host` option.

#### port 

Operator panel port number. The default is `8000`.
The user can change this value with the `hardpy init --frontend-port` option.

### socket

Socket settings.
Internal socket port for passing backend data (such as a dialog box) to running pytest tests.

#### host

Socket host name. The default is `localhost`.
The user can change this value with the `hardpy init --socket-host` option.

#### port 

Socket port number. The default is `6525`.
The user can change this value with the `hardpy init --socket-port` option.