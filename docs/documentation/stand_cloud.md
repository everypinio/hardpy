# StandCloud

## About StandCloud

**StandCloud** is a cloud management tool for electronics manufacturing.
Test data is crucial for evaluating performance.
StandCloud allows you to explore data patterns, create visualizations, and gain insights.
This helps in identifying potential trends and opportunities.
It allows you to identify potential limitations.

For more information, visit the **StandCloud** [website](https://standcloud.everypin.io).

## StandCloud and HardPy integration

**HardPy** allows test result data to be stored in the **StandCloud** and
read them from the **StandCloud**.
For an example of StandCloud and HardPy integration,
see [StandCloud example](../examples/stand_cloud.md) and
[StandCloud readed example](../examples/stand_cloud_reader.md).

## API key via .env file

The **StandCloud** API key can be provided through a `.env` file
instead of being stored in the `hardpy.toml` configuration file.
The `.env` file must be located in the root of the working project.
The variable name is `HARDPY_SC_API_KEY`.
An example file is available in the root of the **HardPy** repository
under the name `.env.example`.
If the `HARDPY_SC_API_KEY` environment variable is defined,
its value takes priority over the `api_key` value
specified in the `hardpy.toml` file.

Example of the `.env` file content:

```bash
HARDPY_SC_API_KEY=your_api_key_here
```

## HardPy rules

### General guidelines

Some tips for getting the best analytics in **StandCloud**.

1. Use the [set_dut_serial_number](./pytest_hardpy.md#set_dut_serial_number)
   to store DUT serial number.
   The serial number allows you to distinguish between units with
   the same part number. It also allows you to analyze the
   number of attempts to test a device.
2. Use the [set_dut_part_number](./pytest_hardpy.md#set_dut_part_number)
   to store DUT part number.
   The part number is an identifier that allows you to clearly 
   identify the product.   
3. Use the [set_case_artifact](./pytest_hardpy.md#set_case_artifact),
   [set_module_artifact](./pytest_hardpy.md#set_module_artifact),
   and [set_run_artifact](./pytest_hardpy.md#set_run_artifact)
   to store important information, that cannot be accommodated in other structured fields
   such as [set_case_measurement](./pytest_hardpy.md#set_case_measurement)
   and [set_case_chart](./pytest_hardpy.md#set_case_measurement).
4. Use the [case_name](./pytest_hardpy.md#case_name)
   and [module_name](./pytest_hardpy.md#module_name)
   markers for human-readable names.
   They make it easier to analyze the tests.
