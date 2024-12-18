# StandCloud

## About StandCloud

**StandCloud** is a cloud management tool for electronics manufacturing.
Test data is crucial for evaluating performance.
StandCloud allows you to explore data patterns, create visualizations, and gain insights.
This helps in identifying potential trends and opportunities.
It allows you to identify potential limitations.

For more information, visit the **StandCloud** [website](https://everypin.io/standcloud).

## StandCloud and HardPy integration

**HardPy** allows test result data to be stored in the **StandCloud**.
For an example of StandCloud and HardPy integration,
see [StandCloud example](../examples/stand_cloud.md).

To authorize in **StandCloud**, you need to know 2 addresses:
The API address and the authorization address.
To get them, contact **info@everypin.io**.

Both addresses must be added to **hardpy.toml**.

You need to run the command.

```bash
hardpy sc-register <tests_path>
```
where <tests_path> is the real tests path.
Then go to the authorization link in the terminal and open the link to the browser.
You will need to enter your StandCloud login and password.
After successful authorization, you should press the `Confirm` button,
after which a page will appear in the browser informing about successfully issued token.
Otherwise, an error message will appear on the page.
The browser can be closed.
The `Registration completed` message should appear in the terminal with
the start of the registration.

To check the **StandCloud** connection status, run the command.

```bash
hardpy sc-register --check <tests_path>
```

The **StandCloud** authentication time is updated each time you interact with **StandCloud**.
If you do not use StandCloud services, the authentication will be canceled and the
`hardpy sc-register` function must be called again.
To clarify and edit your authentication time case, you can contact **info@everypin.io**.
