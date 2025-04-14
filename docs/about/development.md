# Development

## Environment

### Requirements

* **python** version must be equal to or greater than  **3.10**;
* **yarn** version must be equal to 4.0.1;
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

## Frontend

### Overview

The frontend of the project can be developed, debugged, and built using Visual Studio Code (VSCode) or command-line tools.
Below are the steps to run, debug, and build the frontend application.

**node.js** and **yarn** are required to build the frontend.

### 1. Running the frontend for Hardpy debugging

To run the frontend application for debugging purposes, you can use the **Run Frontend** configuration in VSCode or execute commands manually.

#### Using VSCode

1. Open the "Run and Debug" in VSCode.
2. Select the **Run Frontend** configuration.
3. Click the "Run" button (or press `F5`).

This will:

- Launch `yarn`.
- Start the frontend application in development mode with debugging enabled.

#### Manually

Navigate to the frontend directory and run the following commands:

```bash
npm install && npm run dev
```

You can specify your own port by adding it as an environment variable:

```bash
PORT=4000
```

By default, the frontend opens on port 3000 at the address [http://localhost:3000/](http://localhost:3000/).

### 2. Debugging the frontend

To debug the frontend application in the Chrome browser, use the **Debug Frontend** configuration in VSCode.

#### Using VSCode

1. Ensure the frontend is running (use the **Run Frontend** configuration or manually start it).
2. Open the "Run and Debug" in VSCode.
3. Select the **Debug Frontend** configuration.
4. Click the "Run" button (or press `F5`).

This will:

- Launch Chrome and attach the debugger to the running frontend application at `http://localhost:3000`.
- Enable source maps for easier debugging.

#### Manually

1. Start the frontend application (as described in the **Run Frontend** section).
2. Open Chrome and navigate to `http://localhost:3000`.
3. Use Chrome DevTools (`F12`) to debug the application.

### 3. Building the frontend for Hardpy package

To build the frontend and include it in the Hardpy package, you can use the provided scripts or run the commands manually.

Use the `compile_front.sh` script from `scripts` folder
or run the scripts manually:

```bash
pip install -r requirements.txt
python -m build
```

For frontend rebuilding use the `recompile_front.sh` from `scripts` folder
or run the scripts manually:

```bash
pip uninstall $PRJ -y

rm -rf hardpy/hardpy_panel/frontend/dist
rm -rf hardpy/hardpy_panel/frontend/node_modules
rm -rf *.egg-info
rm -rf dist
rm -rf __pycache__

pip install -r requirements.txt
python -m build
```

### 4. Setting the `DEBUG_FRONTEND` variable

To enable debugging for the frontend application, you must set the `DEBUG_FRONTEND` environment variable.
Without this variable, the frontend will not run in debug mode, and the **Run Frontend** and **Debug Frontend** configurations will not work as expected.

#### Option 1: setting `DEBUG_FRONTEND` in VSCode configuration

You can specify the `DEBUG_FRONTEND` variable directly in the VSCode launch configuration.
Here's an example of how to include it in a test configuration:

```json
{
    "name": "Python: Example Dialog box",
    "type": "debugpy",
    "request": "launch",
    "module": "hardpy.cli.cli",
    "console": "integratedTerminal",
    "env": {
        "DEBUG_FRONTEND": "1"
    },
    "args": [
        "run",
        "examples/dialog_box"
    ]
}
```

This configuration ensures that the frontend runs in debug mode when the test is executed.

#### Option 2: setting `DEBUG_FRONTEND` in `.env` file

Alternatively, you can define the `DEBUG_FRONTEND` variable in a `.env` file located in the root of your project. 

1. Create a `.env` file in the root directory of your project (if it doesn't already exist).
2. Add the following line to the `.env` file:

```env
DEBUG_FRONTEND=1
```

3. Ensure your VSCode or runtime environment loads the `.env` file. Many tools and frameworks (e.g., `python-dotenv`) automatically load variables from `.env`.

## Launch

1. Install dependencies or create environment.
2. Compile frontend if it's the first launch.
3. Launch `hardpy init` with path to tests folder.
4. Launch **CouchDB** instance.
5. Launch `hardpy run` with path to tests folder.

Addresses:

- HardPy panel: http://localhost:8000/
- CouchDB: http://localhost:5984/_utils/

## Documentation

### Server

Documentation server command is:

```bash
mkdocs serve
```

Documentation address: http://localhost:8000/

### Build

Documentation building command is:

```bash
mkdocs build
```

The result is in the folder `public`.
