# Minimal example 

This is the simplest example of using **Jig**.
This code shows how to convert any **pytest** tests into a **Jig** project. 
To achieve this, a `jig.toml` file containing the minimum required information must be added. 
Data from this project will be saved in a JSON document in the **.jig/runstore** directory.

The code for this example can be seen inside the jig package [Minimal example](https://github.com/everypinio/jig/tree/main/examples/minimal_example).

### how to start

1. Install the jig from pypi: 
  ```
  pip install pytest-jig
  ```
2. Copy the jig.toml file to the tests directory.
3. Launch **Jig**:
   ```bash
   jig run <tests_directory>
   ```
4. Open `http://localhost:8000/` 

### test_1.py

```python
def test_one():
    assert True
```

### jig.toml

```toml
[database]
storage_type = "json"

[frontend]
host = "localhost"
port = 8000
```
