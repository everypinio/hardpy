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

Tests are skipped using the `pytest-dependency` plugin.
You can read more in the [documentation.](https://pytest-dependency.readthedocs.io/en/stable/index.html)
If a test that a test depends on fails or is skipped, the dependent test will also be skipped.

To use:

- Install `pytest-dependency` package (e.g. pytest-dependency==0.6.0).
- Add the line `@pytest.mark.dependency()` before independent tests.
- Add the line `@pytest.mark.dependency(depends=["test_one"])` before the dependent test,
if a test that a test depends on is in the same file.
- Add the line `@pytest.mark.dependency(depends=["test_a.py::test_one"], scope='session')`
before the dependent test, if a test that a test depends on is in the other file.
- Specify the file path regardless of the launch method.

Test/module name formats:

- `test_one` - test in the current module
- `test_file.py::test_one` - test in another module
- `test_file.py` - another module

In our example, the tests depend on each other as follows:

- If test A fails, skip test B.

#### test_a.py

```python
import pytest

@pytest.mark.dependency()
def test_one():
    assert False
```

#### test_b.py

```python
import pytest

@pytest.mark.dependency(
    depends=["test_a.py::test_one"],
    scope='session'
)
def test_one():
    assert True
```


### pytest-depends

Tests are skipped using the `pytest-depends` plugin.
You can read more in the [documentation](https://pypi.org/project/pytest-depends/)
The package can be used on Python versions 3.8 and lower.
If a test/module that a test depends on fails or is skipped, the dependent test/module will also be skipped.

To use:

- Install `pytest-depends` package (e.g. pytest-depends==1.0.1).
- Add the line `@pytest.mark.depends(on=['test_name'])` before the dependent test,
or `pytestmark = pytest.mark.depends(on="test_name")` at the beginning of the module.
- Specify the file path relative to the root folder regardless of the launch method.

Test/module name formats:

- `test_one` - test in the current module
- `test_file.py::test_one` - test in another module
- `test_file.py` - another module

In our example, the tests depend on each other as follows:

- If test A fails, skip test B.

#### test_a.py

```python
import pytest

def test_one():
    assert True

def test_two():
    assert False
```

#### test_b.py

```python
import pytest

pytestmark = [
    pytest.mark.depends(on="test_a.py::test_two"),
]

def test_one():
    assert True
```

### pytest.skipif

Alternatively, you can use the `skip` and `skipif` decorators.
You can read more in the [documentation](https://docs.pytest.org/en/latest/how-to/skipping.html#skipping-test-functions)
