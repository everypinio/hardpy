#!/bin/bash

sudo apt update && sudo apt install -y curl apt-transport-https gnupg
curl https://couchdb.apache.org/repo/keys.asc | gpg --dearmor | sudo tee /usr/share/keyrings/couchdb-archive-keyring.gpg >/dev/null 2>&1
source /etc/os-release && echo "deb [signed-by=/usr/share/keyrings/couchdb-archive-keyring.gpg] https://apache.jfrog.io/artifactory/couchdb-deb/ ${VERSION_CODENAME} main" | sudo tee /etc/apt/sources.list.d/couchdb.list >/dev/null

sudo apt update && sudo apt install -y couchdb
sudo mkdir -p /dev/shm/couchdb && sudo chmod 777 /dev/shm/couchdb

sudo cp ./default.ini /opt/couchdb/etc/default.ini && sudo cp ./local.ini /opt/couchdb/etc/local.ini

sudo apt install -y ufw && sudo ufw enable
sudo ufw allow 5984/tcp
sudo ufw allow 8000/tcp
sudo ufw allow 6525/tcp

sudo service couchdb restart

pip3 install hardpy --break-system-packages

read -p "Do you want to reboot system? (yes/no): " choice
case "$choice" in
  yes) echo "Rebooting system..." && sudo reboot ;;
  no) echo "Cancel" ;;
  *) echo "Incorrect input." ;;
esac
