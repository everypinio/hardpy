# Hello hardpy

This is the simplest example of using **HardPy**.

### how to start

1. Launch [CouchDH instance](../documentation/database.md#couchdb-instance).
2. Create a directory `<dir_name>` with the files described below.
3. Launch `hardpy-panel <dir_name>`.

### conftest.py

Registering the HardPy plugin in pytest_configure.

```python
import pytest
from hardpy import HardpyPlugin

def pytest_configure(config: pytest.Config):
    config.pluginmanager.register(HardpyPlugin())
```

### test_simple.py

Contains the simplest example of a valid test.

```python
import pytest

def test_one():
    assert True
```
