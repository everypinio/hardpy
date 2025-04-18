# Skip test

This is an example of using the **pytest-hardpy** functions with a test dependency
on another test and skipping tests.

### how to start

1. Launch `hardpy init skip_test`.
2. Launch [CouchDH instance](../documentation/database.md#couchdb-instance).
3. Modify the files described below.
4. Launch `hardpy run skip_test`.

### description

If a test case/module that a test case/module depends on fails, errors or is skipped, the dependent test case/module will also be skipped.
A module is considered passed only if all module tests passed.
If these dependencies are incorrect, the tests will not run.

To use:

- Add the line `@pytest.mark.dependency()` before independent tests.
- Add the line `@pytest.mark.dependency(test_1::test_one)` before the dependent test,
if a test that a test depends on is in the same file.
- Add the line `@pytest.mark.dependency(test_1)`
before the dependent test, if the test depends on the module.

Test/module name formats:

- `test_1` - if depends on the test module
- `test_1::test_one` - if depends on the test case

#### case by case dependence

```python
import pytest

def test_one():
    assert False

@pytest.mark.dependency("test_1::test_one")
def test_two():
    assert False
```

`test_one` is marked as a dependency for `test_two` using `@pytest.mark.dependency("test_1::test_one")`.
If `test_one`, then `test_two` will be skipped.

#### module by module dependence

##### test_1.py

```python
def test_one():
    assert False
```

##### test_2.py

```python
import pytest

pytestmark = pytest.mark.dependency("test_1")

def test_one():
    assert True
```

Module `test_2` depends on module `test_1`.
If an error occurs in module `test_1`, all tests in module `test_2` will be skipped.

#### multiple test dependencies example

You can specify multiple dependencies for a single test or module.
The test will only run if ALL specified dependencies are successful.
If any dependency fails, the test will be skipped.

```python
import pytest

def test_one():
    assert True

def test_two():
    assert False

@pytest.mark.dependency("test_1::test_one")
@pytest.mark.dependency("test_1::test_two")
def test_three():
    assert True
```

In this case, `test_three` depends on two other tests.
Since `test_two` fails, `test_three` will be skipped.

#### multiple module dependencies example

##### test_1.py

```python
def test_one():
    assert True
```

##### test_2.py

```python
def test_two():
    assert False
```

##### test_3.py

```python
import pytest

pytestmark = [
    pytest.mark.dependency("test_1"),
    pytest.mark.dependency("test_2"),
]

def test_three():
    assert True
```

Here, the entire `test_3` module depends on both `test_1` and `test_2` modules.
Since `test_2` fails, all tests in `test_3` will be skipped.
