#!/bin/bash

PRJ=hardpy

cd ..

# Uninstall package
pip3 uninstall $PRJ -y

# Clean artifacts
rm -rf $PRJ/hardpy_panel/frontend/dist
rm -rf $PRJ/hardpy_panel/frontend/node_modules
rm -rf *.egg-info
rm -rf dist
rm -rf __pycache__

# Build
pip3 install -r requirements.txt
python3 -m build
