# Enabling Mobile Device Access to the Frontend

To allow other devices to connect to the frontend remotely, follow these steps:

## 1. Open Required Ports on Your Computer

### For Linux (using `ufw` firewall)

Run the following commands in your terminal:

```bash
sudo ufw allow 5984  # Allows CouchDB connections
sudo ufw allow 8000  # Allows frontend access
sudo ufw enable     # Enable the firewall if not already active
sudo ufw status     # Verify the ports are open
```

## 2. Find Your Computer's Network Address

Use the `ifconfig` command to find your local IP address:

```bash
ifconfig | grep "inet "
```

Look for an address in the format `192.168.x.x` or `10.x.x.x` (this is your local network IP).

## 3. Configure Ports in Project Files

### `hardpy.toml` Configuration

Edit the file to include your computer's network address:

```toml
[database]
user = "dev"
password = "dev"
host = "{YOUR_COMPUTER_NETWORK_ADDRESS}"  # Replace with address from step 2
port = 5984

[frontend]
host = "0.0.0.0"  # Allows connections from any network interface
port = 8000
```

### `pytest.ini` Configuration

Update the database URL:

```ini
[pytest]
addopts = --hardpy-db-url http://dev:dev@0.0.0.0:5984/
```

### `couchdb.ini` Configuration

Ensure CouchDB is accessible:

```ini
[chttpd]
port = 5984
bind_address = 0.0.0.0  # Makes CouchDB accessible from network
```

## 4. Launch the Frontend

You can start the frontend using either method:

### Option 1: Via Bash Script

```bash
./recompile_front.sh
hardpy run
```

### Option 2: Through Debug Mode

Run the project in your IDE's debug mode with the configured settings.

## Verification Steps

1. On your mobile device, ensure it's connected to the same network as your computer
2. Open a browser and navigate to: `http://[YOUR_COMPUTER_ADDRESS]:8000`
3. Verify you can see the frontend interface

## Troubleshooting

- If connection fails:
  - Verify firewall settings (`sudo ufw status`)
  - Check all services are running (CouchDB, frontend)
  - Ensure no other devices are using the same ports
  - Verify your mobile device and computer are on the same network
