# Auto-scroll demo

This example demonstrates the optional `auto_scroll` flag in `hardpy.toml`.
When enabled, the operator panel auto-expands a suite when one of its cases
starts running, scrolls the running case into view, and auto-closes the
suite once it finishes (unless it has a failed case).

The code for this example can be seen inside the hardpy package
[auto_scroll_demo](https://github.com/everypinio/hardpy/tree/main/examples/auto_scroll_demo).

### how to start

1. Launch `hardpy init auto_scroll_demo`.
2. Launch [CouchDB instance](../documentation/database.md#couchdb-instance).
3. Set `auto_scroll = true` under `[frontend]` in `hardpy.toml`.
4. Launch `hardpy run auto_scroll_demo`.

### what to watch for

The demo includes five modules that exercise the four coordinated behaviors
the `auto_scroll` flag turns on:

- **Setup** — three slow (~2 s) all-pass cases. Lets the operator scroll
  freely while watching the running case stay centered.
- **Smoke** — eight fast (~0.15 s) cases. Stresses the scroll debounce and
  the user-scroll suppression window: `runningIndex` changes about six
  times a second.
- **Burst** — one case that streams 42 measurements at 0.5 s intervals.
  The row grows downward without `runningIndex` changing, so the panel
  uses `block: 'end'` to keep the newest sample visible. With
  `measurement_display = true` in `hardpy.toml` (the default), each
  sample shows up as a tag as it comes in.
- **Measurements** — four cases with a mid-run failure. The failure
  triggers an auto-expand and keeps the suite open afterward.
- **Functional** — four cases with a late failure. Exercises the new-run
  reset on the next run start.

### `hardpy.toml`

```toml
title = "HardPy TOML config"
tests_name = "Auto-scroll demo"

[database]
storage_type = "couchdb"
user = "dev"
password = "dev"
host = "localhost"
port = 5984

[frontend]
host = "localhost"
port = 8000
language = "en"
auto_scroll = true
```

### user-scroll suppression

Auto-scroll suppresses itself for three seconds after any operator-driven
scroll event. The events watched are `wheel`, `touchmove`, and the keys
`PageUp`, `PageDown`, `Home`, `End`, `ArrowUp`, `ArrowDown`. This means an
operator can scroll back to inspect an earlier suite without the next
state update yanking the viewport back to the running case.
