# Operator message

Function set_operator_msg designed to send messages to an operator via a database. 
Operator messages are needed to promptly inform the operator about problems that arise during testing, if problems arise before the start of testing or after its completion.

![operator_msg](../img/operator_msg.png)

## Purpose:

The operator_msg function is used to send a message to the operator, which is stored in the statestore database. 
This function is primarily intended for events that occur outside of the testing environment. 
For messages during testing, please use the run_dialog_box function.

## Arguments:

- `msg (str)`: The message to be displayed. This argument is required.
- `title (str, optional)`: An optional title for the message. If not provided, a default title of "Message" will be used.

## Example:

```Python
import hardpy

def my_function():
    # Some code that might trigger an error
    try:
        # ...
    except Exception as e:
        hardpy.set_operator_msg(f"An error occurred: {str(e)}", "Error Notification")
```

## Behavior:

When set_operator_msg is called, a notification will be displayed to the operator.
This notification will contain the specified message and title. 
Testing will be stopped by dismissing the notification.
