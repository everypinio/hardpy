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
│ --create-database      --no-create-database             Create CouchDB database.                           │
│                                                         [default: create-database]                         │
│ --database-user                                TEXT     Specify a database user. [default: dev]            │
│ --database-password                            TEXT     Specify a database user password. [default: dev]   │
│ --database-host                                TEXT     Specify a database host. [default: localhost]      │
│ --database-port                                INTEGER  Specify a database port. [default: 5984]           │
│ --frontend-port                                INTEGER  Specify a frontend port. [default: 8000]           │
│ --frontend-host                                TEXT     Specify a frontend host. [default: localhost]      │
│ --socket-host                                  TEXT     Specify a socket host. [default: localhost]        │
│ --socket-port                                  INTEGER  Specify a socket port. [default: 6525]             │
│ --sc-address                                   TEXT     Specify a StandCloud address.                      │
│                                                         [default: everypin.standcloud.localhost]           │
│ --sc-connection-only --no-sc-connection-only            Check StandCloud service availability before start.│
|                                                         [default: check-stand-cloud]                       │
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

## sc-register

The `hardpy sc-register` command is used to register in **StandCloud**.
By default, it registers **HardPy** tests from the current directory.

You can run the `hardpy sc-register <tests_directory>` command, where `<tests_directory>`
is the path to the directory with your tests.

```bash
 Usage: hardpy sc-register [OPTIONS] [TESTS_DIR]

 Register HardPy in StandCloud.

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
hardpy sc-register --help
```

## sc-unregister

The `hardpy sc-unregister` command is used to unregister from **StandCloud**.

```bash
 Usage: hardpy sc-unregister [OPTIONS]

 Unregister HardPy from StandCloud.
 Unregister HardPy from all StandCloud accounts.

╭─ Options ──────────────────────────────────────────────────────────────────────────────────────────────────╮
│ --help          Show this message and                                                                      │
╰────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
```

```bash
hardpy sc-unregister --help
```
