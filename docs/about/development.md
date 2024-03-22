# Development

## Environment

### Requirements

* **python** version must be equal to or greater than  **3.10**;
* **yarn** version must be equal to or greater than **3.4.1**;
* **node.js** version must be equal to or greater than **16.10.0**;
* **CouchDB** version must be equal to or greater than **3.2.0**;

### Conda

Create a conda.yaml file if you prefer to work through **Anaconda** or **Miniconda**:

```yaml
name: hardpy
channels:
  - defaults
  - conda-forge
dependencies:
  - python=3.10
  - pip>=22
  - nodejs=20
  - yarn=4.0.1
  - pip:
      - -r requirements.txt
      - -r requirements-doc.txt
```

create environment:

```bash
conda env create -f conda.yaml
```

Activate:

```bash
conda activate hardpy
```

### venv

If you prefer to work through **venv**:

```bash
python -m venv venv
```

Activate:

```bash
source venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
pip install -r requirements-doc.txt
```

## Frontend building

**node.js** and **yarn** are required to build the frontend.

Use the `compile_front.sh` script from `scripts` folder
or run the scripts manually:

```bash
pip3 install -r requirements.txt
python3 -m build
```

For frontend rebuilding use the `recompile_front.sh` from `scripts` folder
or run the scripts manually:

```bash
pip3 uninstall $PRJ -y

rm -rf hardpy/hardpy_panel/frontend/dist
rm -rf hardpy/hardpy_panel/frontend/node_modules
rm -rf *.egg-info
rm -rf dist
rm -rf __pycache__

pip3 install -r requirements.txt
python3 -m build
```

## Launch

1. Install dependencies or create environment.
2. Compile frontend if it's the first launch.
3. Launch **CouchDB** instance.
4. Launch `hardpy-panel` with path to tests folder.

Addresses:

- HardPy panel: http://localhost:8000/
- Fauxton CouchDB: http://127.0.0.1:5984/_utils/

## Documentation

### Server

Documentation server command is:

```bash
mkdocs serve
```

Documentation address: http://127.0.0.1:8000/

### Build

Documentation building command is:

```bash
mkdocs build
```

The result is in the folder `public`.
