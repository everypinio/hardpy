# HardPy config

**HardPy** uses the `hardpy.toml` file for configuration.
The user can change the fields at creation by using [hardpy init](./cli.md#hardpy-init).

???+ note
    All **HardPy** project must have `hardpy.toml` file.

## Minimal configuration file

```toml
title = "HardPy TOML config"

[database]
user = "dev"
password = "dev"
host = "localhost"
port = 5984

[frontend]
host = "localhost"
port = 8000
```

## Full configuration file

```toml
title = "HardPy TOML config"
tests_name = "My tests"
current_test_config = ""

[database]
user = "dev"
password = "dev"
host = "localhost"
port = 5984

[frontend]
host = "localhost"
port = 8000
language = "en"
full_size_button = false
sound_on = false
measurement_display = true
manual_collect = false

[frontend.modal_result]
enable = false
auto_dismiss_pass = true
auto_dismiss_timeout = 5

[stand_cloud]
address = "standcloud.io"
connection_only = true
autosync = true
autosync_timeout = 30
api-key = "1234567890"
```

## Configuration fields description

### common

Common settings.

#### title

Configuration file header.
The value is always `HardPy TOML config`.

#### tests_name

Tests name. The user can change this value with the `hardpy init --tests-name` argument.

#### current_test_config

Tests file configuration name. 
An example of its use can be found on page [Multiple configs](./../examples/multiple_configs.md).

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

#### full_size_button

Enable full-size start/stop button layout in operator panel.
When set to `true`, the button will be displayed in full-size layout with larger dimensions and centered positioning.
Default is `false`.

#### sound_on

Enable or disable test completion sound notifications.
When set to `true`, sound will play when test execution completes (PASS/FAIL/STOP status).
Default is `false`.

#### measurement_display

Enable or disable measurement display in the operator panel.
When set to `true`, measurements created using `set_case_measurement` will be displayed as tags 
showing name, value, and unit information.
Default is `true`.

#### manual_collect

Enable or disable manual test collection mode in the [operator panel](./hardpy_panel.md#manual-test-selection).
When set to `true`, users can selectively choose which tests to run by checking individual test cases,
and only the selected tests will be executed when starting the test run.
When set to `false`, all discovered tests will run automatically as before.
Default is `false`.

#### modal_result

Modal result windows settings for test completion display.

```toml
[frontend.modal_result]
enable = false
auto_dismiss_pass = true
auto_dismiss_timeout = 5
```

##### enable

Enable or disable test completion modal result windows.
When set to `true`, modal windows will display test completion status (PASS/FAIL/STOP) at the end of test execution.
Default is `false`.

##### auto_dismiss_pass

Automatically dismiss PASS result modals after the timeout period.
When set to `true`, PASS results will automatically close without requiring user interaction.
FAIL and STOP results always require manual dismissal.
Default is `true`.

##### auto_dismiss_timeout

Timeout in seconds for auto-dismissing PASS result modals.
Applies only when `auto_dismiss_pass = true`.
Default is `5` seconds.

### stand_cloud

[StandCloud](./stand_cloud.md) settings.

```toml
[stand_cloud]
address = "demo.standcloud.localhost"
connection_only = true
autosync = true
autosync_timeout = 30
api-key = "1234567890"
```

#### address

**StandCloud** service address.
To obtain one, contact **info@everypin.io**.

#### connection_only

Boolean variable, if set to `true`, **HardPy** will check the connection
to the **StandCloud** service at each startup before running tests.
The default value is `false`.

If the connection fails, the tests will not run.

#### autosync

Boolean variable, if set to `true`, **HardPy** will automatically send data 
to **StandCloud** upon completion of testing.

The default value is `false`.

#### autosync_timeout

This is an integer variable greater than 1, representing the time interval 
in minutes between StandCloud synchronization attempts.

The default value is `30`.

#### api-key

**StandCloud** API key.

### test_configs

Test configurations describes using the `[[test_configs]]` table array. 

#### name

A user-friendly name for the configuration.

#### file

The path to the `pytest.ini` file that defines the specific pytest arguments and test selection for this configuration.

#### description

An optional field to provide a more detailed explanation of the configuration.
