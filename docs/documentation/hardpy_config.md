# HardPy config

**HardPy** uses the `hardpy.toml` file for configuration.
The user can change the fields at creation by using [hardpy init](./cli.md#hardpy-init).

???+ note
    All **HardPy** project must have `hardpy.toml` file.

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
```

## Maximum configuration file

```toml
title = "HardPy TOML config"
tests_dir = "tests"
tests_name = "My tests"

[database]
user = "dev"
password = "dev"
host = "localhost"
port = 5984

[frontend]
host = "localhost"
port = 8000
language = "en"

[stand_cloud]
address = "demo.standcloud.io"
connection_only = true
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

#### tests_name

Tests name. The default is [tests_dir](#tests_dir).
The user can change this value with the `hardpy init --tests-name` argument.

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

#### language

Language of operator panel. The default is `en`.
Available languages are [there](hardpy_panel.md#languages).

### stand_cloud

[StandCloud](./stand_cloud.md) settings.

```toml
[stand_cloud]
address = "demo.standcloud.localhost"
connection_only = true
```

#### address

**StandCloud** service address.
To obtain one, contact **info@everypin.io**.

#### connection_only

Boolean variable, if set to `true`, **HardPy** will check the connection
to the **StandCloud** service at each startup before running tests.
The default value is `false`.

If the connection fails, the tests will not run.
