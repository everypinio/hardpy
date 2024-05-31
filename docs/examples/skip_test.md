# Skip test

This is an example of using the **pytest-hardpy** functions with a test dependency
on another test and skipping tests.

### how to start

1. Launch [CouchDH instance](../documentation/database.md#couchdb-instance).
2. Create a directory `<dir_name>` with the files described below.
3. Specify the dependency in the file `pyproject.toml`
4. Launch `hardpy-panel <dir_name>`.

### pytest.ini

Enable the pytest-hardpy plugin.

```ini
# pytest.ini
[pytest]
addopts = --hardpy-pt
```

### pytest-dependency

If a test case/module that a test case/module depends on fails or is skipped, the dependent test case/module will also be skipped.
A module is considered passed only if all module tests passed.

To use:

- Add the line `@pytest.mark.dependency()` before independent tests.
- Add the line `@pytest.mark.dependency(test_1::test_one)` before the dependent test,
if a test that a test depends on is in the same file.
- Add the line `@pytest.mark.dependency(test_1)`
before the dependent test, if the test depends on the module.

Test/module name formats:

- `test_1` - if depends on the test module
- `test_1::test_one` - if depends on the test case

In our example, the tests depend on each other as follows:

- If test A fails, skip test B.

#### test_a.py

```python
import pytest

def test_one():
    assert False
```

#### test_b.py

```python
import pytest

@pytest.mark.dependency("test_a::test_one")
def test_one():
    assert True
```
