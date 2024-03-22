# Storing CouchDB Database in RAM

When using one of the methods below, the database data will be saved to a folder in temporary storage, and after the computer is turned off, the data will be deleted.

## linux with binary packages

- Create a CouchDB folder in the temporary file storage:

```bash
sudo mkdir /dev/shm/couchdb
```

- Add editing rights to this folder:

```bash
sudo chmod 777 /dev/shm/couchdb
```

- Edit the database_dir parameter in the database configuration file `/opt/couchdb/etc/default.ini`:

```ini
[couchdb]
database_dir = ./../../dev/shm/couchdb
```

- Restart the couchdb service:

```bash
sudo service couchdb restart
```

## linux with docker-compose.yaml

Example of `docker-compose.yaml` file with saving files in RAM:

```yaml
version: "3.8"

services:
  couchserver:
    image: couchdb:3.3.2
    ports:
      - "5984:5984"
    environment:
      COUCHDB_USER: dev
      COUCHDB_PASSWORD: dev
    volumes:
      - /dev/shm/couchdb:/opt/couchdb/data
      - ./docker/couchdb.ini:/opt/couchdb/etc/local.ini
```

## windows

### ram disc creation

- Open the command prompt using `Win+R`, type `diskmgmt.msc`, and press `Enter`.
- Click Action > Create Virtual Hard Disk.
- Specify any Location, set Size (e.g., 30 MB), choose VHD type and Fixed size.
- Right-click the created disk (left pane), select Initialize Disk, choose GUID Partition Table.
- Right-click the created disk (right pane), select New Simple Volume, Assign drive letter (e.g., `K`), click Next twice, then Finish.
- Create a folder named `couchdb` in the created drive (`K` in our case) using File Explorer.

### database_dir in binary couchdb settings

- Open the file located at `C:/CouchDB/etc/default.ini` as administrator.
- Set the value of the database_dir parameter to `K:/couchdb`.
- Save and close the file.
- Open the Services console using `Win+R`, type `services.msc`, and press `Enter`.
- Locate the Apache CouchDB service and restart it.

### database_dir in docker compose couchdb settings

In `docker-compose.yaml` file in `volumes` find the string:

```yaml
./docker/dbdata:/opt/couchdb/data
```

Replace this string with next value:

```yaml
K:/couchdb:/opt/couchdb/data
```