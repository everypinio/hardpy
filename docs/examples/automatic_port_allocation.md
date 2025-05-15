# Automatic port allocation

In **HardPy**, the frontend service automatically handles port allocation when running the operator panel.
This feature ensures the service starts even if the configured port is unavailable.

## Configuration examples

### 1. With specified port

When a port is defined in `hardpy.toml`, **HardPy** will attempt to use that exact port:

```toml
title = "HardPy TOML config"
tests_dir = "minute_parity"

[database]
user = "dev"
password = "dev"
host = "localhost"
port = 5984

[frontend]
host = "localhost"
port = 8000  # HardPy will try to use port 8000
```

**Output:**

```
Launch the HardPy operator panel...
http://localhost:8000
```

### 2. With specified port (port occupied)

When the specified port is in use:

```toml
[frontend]
host = "localhost"
port = 8000
```

**Output:**

```
Launch the HardPy operator panel...
Error: Specified port 8000 is already in use
```

The `hardpy run` command will terminate in this case.

### 3. Without specified port (automatic selection)

When no port is specified, **HardPy** automatically selects an available port.

```toml
[frontend]
host = "localhost"
```

**Output:**

```
Launch the HardPy operator panel...
Automatically selected port 47903
http://localhost:47903
```
