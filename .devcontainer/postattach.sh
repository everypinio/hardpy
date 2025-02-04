pip3 install --upgrade pip

pip3 install -e .[dev]
cd hardpy/hardpy_panel/frontend 
corepack enable
corepack prepare yarn@4.0.1 --activate
yarn set version 4.0.1
corepack yarn install
