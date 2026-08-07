# Command line interface

**Jig** uses the CLI (command line interface) as an entry point.

For more information use:

```bash
jig --help
```

## jig init

The `jig init` command is used to create a test bench.
By default, it creates the `tests` directory.

It consists of:

* `test_1.py` - a pytest file with a simple test;
* `conftest.py` - the pytest conftest file;
* `pytest.ini` - pytest configuration .ini file for pytest;
* `jig.toml` - **Jig** configuration file;
* `docker-compose.yaml` - docker-compose file for running the database;
* `database` - CouchDB database directory;
* `couchdb.ini` - the couchdb configuration .ini file in the database directory;

You can run `jig init <test_bench_name>`, where `<test_bench_name>` is the name of your test bench.

The `jig init` command allows you to change the initial **Jig** settings.
More info in [jig config](./jig_config.md).

```bash
 Usage: jig init [OPTIONS] [TESTS_DIR]

 Initialize Jig tests directory.

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
│ --storage-type                                TEXT      Specify a storage type. [default: couchdb]         |
│ --help                                                  Show this message and exit.                        │
╰────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
```

To obtain this information, use:

```bash
jig init --help
```

## jig run

The `jig run` command is used to start the operator panel server.
By default, it starts **Jig** in the current directory.

You can run the `jig run <tests_directory>` command, where `<tests_directory>`
is the path to the directory with your tests.

```bash
 Usage: jig run [OPTIONS] [TESTS_DIR]

 Run Jig server.

╭─ Arguments ────────────────────────────────────────────────────────────────────────────────────────────────╮
│   tests_dir      [TESTS_DIR]  [default: None]                                                              │
╰────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Options ──────────────────────────────────────────────────────────────────────────────────────────────────╮
│ --help          Show this message and exit.                                                                │
╰────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
```

To obtain this information, use:

```bash
jig run --help
```

## jig start

The `jig start` command is used to launch **Jig** tests while the **Jig** opener panel is running.
By default, it starts tests in the current directory.

```bash
 Usage: jig start [OPTIONS] [TESTS_DIR]

 Usage with arguments: jig start --arg test_mode=debug --arg device_id=DUT-007

 Start Jig tests.

╭─ Arguments ────────────────────────────────────────────────────────────────────────────────────────────────╮
│   tests_dir      [TESTS_DIR]  [default: None]                                                              │
╰────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Options ──────────────────────────────────────────────────────────────────────────────────────────────────╮
│ --arg  -a        TEXT  Dynamic start arguments (format: key=value) [multiple]                              │
│ --help           Show this message and exit.                                                               │
╰────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
```

## jig stop

The `jig stop` command is used to stop **Jig** tests while the **Jig** opener panel is running.
By default, it stops tests in the current directory.

```bash
 Usage: jig stop [OPTIONS] [TESTS_DIR]

 Stop Jig tests.

╭─ Arguments ────────────────────────────────────────────────────────────────────────────────────────────────╮
│   tests_dir      [TESTS_DIR]  [default: None]                                                              │
╰────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Options ──────────────────────────────────────────────────────────────────────────────────────────────────╮
│ --help          Show this message and exit.                                                                │
╰────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
```

## jig status

The `jig status` command is used to get **Jig** tests launch status.

```bash
 Usage: jig status [OPTIONS] [TESTS_DIR]

 Get Jig test launch status.

╭─ Arguments ────────────────────────────────────────────────────────────────────────────────────────────────╮
│   tests_dir      [TESTS_DIR]  [default: None]                                                              │
╰────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Options ──────────────────────────────────────────────────────────────────────────────────────────────────╮
│ --help          Show this message and exit.                                                                │
╰────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
```

## sc-login

The `jig sc-login` command is used to login in **StandCloud**.

You can run the `jig sc-login <stand_cloud_address>` command, where `<stand_cloud_address>`
is the **StandCloud** service address.

```bash
 Usage: jig sc-login [OPTIONS] [TESTS_DIR]

 Login Jig in StandCloud.

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
jig sc-login --help
```

## sc-logout

The `jig sc-logout` command is used to logout from **StandCloud**.

```bash
 Usage: jig sc-logout [OPTIONS]

 Logout Jig from StandCloud.
╭─ Arguments ────────────────────────────────────────────────────────────────────────────────────────────────╮
│   address   TEXT  [default: None] [required]                                                               │
╰────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Options ──────────────────────────────────────────────────────────────────────────────────────────────────╮
│ --help          Show this message and exit.                                                                │
╰────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
```

```bash
jig sc-logout --help
```
