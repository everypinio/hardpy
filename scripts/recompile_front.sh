#!/bin/bash

PRJ=jig
DEBUG_FRONTEND=0
cd ..

# Uninstall package
pip uninstall $PRJ -y

# Clean artifacts
rm -rf $PRJ/jig_panel/frontend/dist
rm -rf $PRJ/jig_panel/frontend/node_modules
rm -rf *.egg-info
rm -rf dist
rm -rf __pycache__

# Build
pip install -r requirements.txt
python -m build
