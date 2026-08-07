# Full capabilities

A single test bench that exercises every feature the operator panel can display.
It is meant as the playground for new features: add a test case here and it shows
up in the panel next to the existing ones.

## How to start

```bash
poetry run example full_capabilities
```

Then open [http://localhost:8000](http://localhost:8000) and press **Start**.

No database is needed. The run state is stored as JSON files in `.hardpy`, and the
report of each finished run is written to `reports`.

## What it covers

| Module | Features |
| --- | --- |
| `test_1_identification.py` | stand, DUT, sub units, instruments and process attributes, `setup` group, `critical` marker |
| `test_2_measurements.py` | numeric and string measurements, limits, comparisons, values recorded without a verdict, case and module artifacts |
| `test_3_charts.py` | single and multi series charts, logarithmic axis |
| `test_4_operator_interaction.py` | every dialog box widget, images, HTML, pass/fail buttons, error codes |
| `test_5_flow_control.py` | retried tests with `attempt`, dependencies inside and across modules |
| `test_6_teardown.py` | `teardown` group, run artifacts, reading the report from a test |

The `Operator interaction` module waits for the operator, every other module runs
on its own against the simulated device in `simulated_device.py`.
