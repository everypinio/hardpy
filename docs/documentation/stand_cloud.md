# StandCloud

## About StandCloud

**StandCloud** is a cloud management tool for electronics manufacturing.
Test data is crucial for evaluating performance.
StandCloud allows you to explore data patterns, create visualizations, and gain insights.
This helps in identifying potential trends and opportunities.
It allows you to identify potential limitations.

For more information, visit the **StandCloud** [website](https://everypin.io/standcloud).

## StandCloud and HardPy integration

**HardPy** allows test result data to be stored in the **StandCloud** and
read them from the **StandCloud**.
For an example of StandCloud and HardPy integration,
see [StandCloud example](../examples/stand_cloud.md) and
[StandCloud readed example](../examples/stand_cloud_reader.md).

To authorize in **StandCloud** you need to know the address of your **StandCloud** service.
To obtain one, contact **info@everypin.io**.

Address must be added to **hardpy.toml** in `stand_cloud` section:

```toml
[stand_cloud]
address = "demo.standcloud.io"
```

You need to run the command:

```bash
hardpy sc-login <stand_cloud_address>
```
where <stand_cloud_address> is the **StandCloud** service address.
StandCloud uses OAuth2 device authorization grant -
[RFC8628](https://datatracker.ietf.org/doc/html/rfc8628).
Then go to the authorization link in the terminal and open the link to the browser.
You will need to enter your StandCloud login and password.
After successful authorization, you should press the `Accept` button.

<h1 align="center">
    <img src="https://raw.githubusercontent.com/everypinio/hardpy/main/docs/img/stand_cloud/stand_cloud_auth.png" alt="stand_cloud_auth" style="width:300px;">
</h1>

To check the **StandCloud** connection status, run the command:

```bash
hardpy sc-login --check <stand_cloud_address>
```

The **StandCloud** authentication time is updated each time you interact with **StandCloud**.
If you do not use StandCloud services, the authentication will be canceled and the
`hardpy sc-login` function must be called again.
To clarify and edit your authentication time case, you can contact **info@everypin.io**.

To logout from **StandCloud** service run the command:

```bash
hardpy sc-logout <stand_cloud_address>
```

Third party applications can authorize in **StandCloud**.
This process is described in the
[StandCloud third party authorization example](./../examples/stand_cloud_thirdparty_auth.md).

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
