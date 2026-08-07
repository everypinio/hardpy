# Hello jig

This is the simplest example of using **Jig** with **CouchDB**.
The code for this example can be seen inside the jig package [Hello Jig](https://github.com/everypinio/jig/tree/main/examples/hello_jig).

### how to start

1. Launch `jig init hello_jig`.
2. Launch [CouchDB instance](../documentation/database.md#couchdb-instance).
3. Launch `jig run hello_jig`.

### test_1.py

Contains the simplest example of a valid test.

```python
def test_one():
    assert True
```
