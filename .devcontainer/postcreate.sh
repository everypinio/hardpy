#!/bin/bash

sudo chown $(whoami):$(whoami) /workspaces

sudo apt update
sudo apt install -y \
	curl \
	apt-transport-https \
	gnupg 
	
curl https://couchdb.apache.org/repo/keys.asc | \
	gpg --dearmor | \
	sudo tee /usr/share/keyrings/couchdb-archive-keyring.gpg > /dev/null 2>&1 
	
. /etc/os-release

echo "deb [signed-by=/usr/share/keyrings/couchdb-archive-keyring.gpg] https://apache.jfrog.io/artifactory/couchdb-deb/ ${VERSION_CODENAME} main" \
	| sudo tee /etc/apt/sources.list.d/couchdb.list > /dev/null

sudo apt update

sudo apt-get install -y couchdb

sudo cp .devcontainer/couchdb.ini /opt/couchdb/etc/local.ini

sudo service couchdb start

sudo service couchdb stop



