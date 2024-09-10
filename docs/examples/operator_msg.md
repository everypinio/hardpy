# Operator message

The [set_operator_msg](./../documentation/pytest_hardpy.md/#set_operator_msg) function is intended for sending messages to the operator.
Operator messages are required to promptly inform the operator of problems if they occur before the test begins or after the test is completed.

![operator_msg](../img/operator_msg.png)

### how to start

1. Launch [CouchDH instance](../documentation/database.md#couchdb-instance).
2. Create a directory `<dir_name>` with the files described below.
3. Launch `hardpy-panel <dir_name>`.

### description

The operator_msg function is used to send a message to the operator, which is stored in the statestore database. 
This function is primarily intended for events that occur outside of the testing environment. 
For messages during testing, please use the run_dialog_box function.

To use:

- Call method `set_operator_msg()` if you want a message to appear in the operator panel for the operator when the condition you specify is met.


## example:

```Python
import hardpy

def my_function():
    # Some code that might trigger an error
    try:
        # ...
    except Exception as e:
        hardpy.set_operator_msg(msg=str(e), title="Important Notice")
```

