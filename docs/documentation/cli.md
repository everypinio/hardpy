# Command line interface

**HardPy** uses the CLI (command line interface) as an entry point.

For more information use:

```bash
hardpy --help
```

## hardpy init

The `hardpy init` command is used to create a test bench.
By default, it creates the `tests` directory.

It consists of:

* `test_1.py` - a pytest file with a simple test;
* `conftest.py` - the pytest conftest file;
* `pytest.ini` - pytest configuration .ini file for pytest;
* `hardpy.toml` - **HardPy** configuration file;
* `docker-compose.yaml` - docker-compose file for running the database;
* `database` - CouchDB database directory;
* `couchdb.ini` - the couchdb configuration .ini file in the database directory;

You can run `hardpy init <test_bench_name>`, where `<test_bench_name>` is the name of your test bench.

The `hardpy init` command allows you to change the initial **HardPy** settings.
More info in [hardpy config](./hardpy_config.md).

```bash
 Usage: hardpy init [OPTIONS] [TESTS_DIR]

 Initialize HardPy tests directory.

╭─ Arguments ────────────────────────────────────────────────────────────────────────────────────────────────╮
│   tests_dir      [TESTS_DIR]  [default: None]                                                              │
╰────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Options ──────────────────────────────────────────────────────────────────────────────────────────────────╮
│ --tests-name                                   TEXT     Specify a tests suite name.                        │
│ --create-database      --no-create-database             Create CouchDB database.                           │
│                                                         [default: create-database]                         │
│ --database-user                                TEXT     Specify a database user. [default: dev]            │
│ --database-password                            TEXT     Specify a database user password. [default: dev]   │
│ --database-host                                TEXT     Specify a database host. [default: localhost]      │
│ --database-port                                INTEGER  Specify a database port. [default: 5984]           │
│ --frontend-port                                INTEGER  Specify a frontend port. [default: 8000]           │
│ --frontend-host                                TEXT     Specify a frontend host. [default: localhost]      │
│ --sc-address                                   TEXT     Specify a StandCloud address.                      │
│ --sc-connection-only --no-sc-connection-only            Check StandCloud service availability before start.│
|                                                         [default: no-sc-connection-only]                   │
│ --sc-autosync        --no-sc-autosync                   Enable StandCloud auto syncronization.             | 
|                                                         [default: no-sc-autosync]                          │
|                                                         [default: check-stand-cloud]                       │
│ --sc-api-key                                  TEXT      Specify a StandCloud API key.                      │
│ --help                                                  Show this message and exit.                        │
╰────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
```

To obtain this information, use:

```bash
hardpy init --help
```

## hardpy run

The `hardpy run` command is used to start the operator panel server.
By default, it starts **HardPy** in the current directory.

You can run the `hardpy run <tests_directory>` command, where `<tests_directory>`
is the path to the directory with your tests.

```bash
 Usage: hardpy run [OPTIONS] [TESTS_DIR]

 Run HardPy server.

╭─ Arguments ────────────────────────────────────────────────────────────────────────────────────────────────╮
│   tests_dir      [TESTS_DIR]  [default: None]                                                              │
╰────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Options ──────────────────────────────────────────────────────────────────────────────────────────────────╮
│ --help          Show this message and exit.                                                                │
╰────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
```

To obtain this information, use:

```bash
hardpy run --help
```

## hardpy start

The `hardpy start` command is used to launch **HardPy** tests while the **HardPy** opener panel is running.
By default, it starts tests in the current directory.

```bash
 Usage: hardpy start [OPTIONS] [TESTS_DIR]

 Usage with arguments: hardpy start --arg test_mode=debug --arg device_id=DUT-007

 Start HardPy tests.

╭─ Arguments ────────────────────────────────────────────────────────────────────────────────────────────────╮
│   tests_dir      [TESTS_DIR]  [default: None]                                                              │
╰────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Options ──────────────────────────────────────────────────────────────────────────────────────────────────╮
│ --arg  -a        TEXT  Dynamic start arguments (format: key=value) [multiple]                              │
│ --help           Show this message and exit.                                                               │
╰────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
```

## hardpy stop

The `hardpy stop` command is used to stop **HardPy** tests while the **HardPy** opener panel is running.
By default, it stops tests in the current directory.

```bash
 Usage: hardpy stop [OPTIONS] [TESTS_DIR]

 Stop HardPy tests.

╭─ Arguments ────────────────────────────────────────────────────────────────────────────────────────────────╮
│   tests_dir      [TESTS_DIR]  [default: None]                                                              │
╰────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Options ──────────────────────────────────────────────────────────────────────────────────────────────────╮
│ --help          Show this message and exit.                                                                │
╰────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
```

## hardpy status

The `hardpy status` command is used to get **HardPy** tests launch status.

```bash
 Usage: hardpy status [OPTIONS] [TESTS_DIR]

 Get HardPy test launch status.

╭─ Arguments ────────────────────────────────────────────────────────────────────────────────────────────────╮
│   tests_dir      [TESTS_DIR]  [default: None]                                                              │
╰────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Options ──────────────────────────────────────────────────────────────────────────────────────────────────╮
│ --help          Show this message and exit.                                                                │
╰────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
```

## sc-login

The `hardpy sc-login` command is used to login in **StandCloud**.

You can run the `hardpy sc-login <stand_cloud_address>` command, where `<stand_cloud_address>`
is the **StandCloud** service address.

```bash
 Usage: hardpy sc-login [OPTIONS] [TESTS_DIR]

 Login HardPy in StandCloud.

╭─ Arguments ────────────────────────────────────────────────────────────────────────────────────────────────╮
│   address   TEXT  [default: None] [required]                                                               │
╰────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Options ──────────────────────────────────────────────────────────────────────────────────────────────────╮
│ --check         --no-check           Check StandCloud connection. [default: no-check]                      │
│ --help                               Show this message and exit.                                           │
╰────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
```

To obtain this information, use:

```bash
hardpy sc-login --help
```

## sc-logout

The `hardpy sc-logout` command is used to logout from **StandCloud**.

```bash
 Usage: hardpy sc-logout [OPTIONS]

 Logout HardPy from StandCloud.
╭─ Arguments ────────────────────────────────────────────────────────────────────────────────────────────────╮
│   address   TEXT  [default: None] [required]                                                               │
╰────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Options ──────────────────────────────────────────────────────────────────────────────────────────────────╮
│ --help          Show this message and exit.                                                                │
╰────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
```

```bash
hardpy sc-logout --help
```
