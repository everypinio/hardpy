# Critical Test Marker

This is example of using the **critical** marker in **pytest-hardpy** to control test execution flow.

## Overview

The `@pytest.mark.critical` marker allows you to designate tests or entire modules as critical.
If a critical test fails or is skipped, all subsequent tests in the current and following modules will be skipped.

## How to Use

1. Launch `hardpy init critical_test`.
2. Launch [CouchDH instance](../documentation/database.md#couchdb-instance).
3. Modify the files described below.
4. Launch `hardpy run critical_test`.

## Examples

### Example 1: critical test failure

```python
# test_critical.py
import pytest

@pytest.mark.critical
def test_core_feature():
    assert False  # This will fail

def test_secondary_feature():
    assert True  # This will be skipped
```

Output:

- `test_core_feature`: Failed
- `test_secondary_feature`: Skipped

### Example 2: critical module

```python
# test_module_a.py
import pytest

pytestmark = pytest.mark.critical

def test_a1():
    assert False  # Fails

def test_a2():
    assert True  # Skipped
```

```python
# test_module_b.py
def test_b1():
    assert True  # Skipped because module_a failed
```

Output:

- `test_a1`: Failed
- `test_a2`: Skipped
- `test_b1`: Skipped
