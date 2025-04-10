# Enabling mobile device access to the frontend

To allow other devices to connect to the frontend remotely, follow these steps:

## 1. Determine IP address

Determine your computer's IP address. For Linux, you can use the `ifconfig` command:

```bash
ifconfig | grep "inet "
```

Look for an address in the format `192.168.x.x` or `10.x.x.x` (this is your local network IP).

## 2. Configure ports in project files

### `hardpy.toml` configuration

Edit the file to include your computer's network address:

```toml
[database]
user = "dev"
password = "dev"
host = "{YOUR_COMPUTER_NETWORK_ADDRESS}"  # Replace with address from step 2
port = 5984

[frontend]
host = "{YOUR_COMPUTER_NETWORK_ADDRESS}"  # Replace with the address from step 2 or insert "0.0.0.0"
port = 8000
```

## 3. Launch the frontend

You can start the frontend using either method:

### Option 1: via bash script

```bash
hardpy run
```

### Option 2: through debug mode

Run the project in your IDE's debug mode with the configured settings.

## Verification steps

1. On your mobile device, ensure it's connected to the same network as your computer
2. Open a browser and navigate to: `http://[YOUR_COMPUTER_ADDRESS]:8000`
3. Verify you can see the frontend interface

## Troubleshooting

- If connection fails:
  - Open required ports on your computer.
  - Verify firewall settings (`sudo ufw status`).
  - Check all services are running (CouchDB, frontend).
  - Ensure no other devices are using the same ports.
  - Verify your mobile device and computer are on the same network.

### Open required ports on your computer

#### For Linux (using `ufw` firewall)

Run the following commands in your terminal:

```bash
sudo ufw allow 5984  # Allows CouchDB connections
sudo ufw allow 8000  # Allows frontend access
sudo ufw enable     # Enable the firewall if not already active
sudo ufw status     # Verify the ports are open
```
