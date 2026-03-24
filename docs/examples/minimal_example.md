# Minimal example 

This is the simplest example of using **HardPy**.
This code shows how to convert any **pytest** tests into a **HardPy** project. 
To achieve this, a `hardpy.toml` file containing the minimum required information must be added. 
Data from this project will be saved in a JSON document in the **.hardpy/runstore** directory.

The code for this example can be seen inside the hardpy package [Minimal example](https://github.com/everypinio/hardpy/tree/main/examples/minimal_example).

### how to start

1. Install the hardpy from pypi: 
  ```
  pip install hardpy
  ```
2. Copy the hardpy.toml file to the tests directory.
3. Launch **HardPy**:
   ```bash
   hardpy run <tests_directory>
   ```
4. Open `http://localhost:8000/` 

### test_1.py

```python
def test_one():
    assert True
```

### hardpy.toml

```toml
[database]
storage_type = "json"

[frontend]
host = "localhost"
port = 8000
```
