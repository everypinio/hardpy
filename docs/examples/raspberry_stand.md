# Hardpy Installation Guide for Raspberry Pi

This document provides a step-by-step guide for installing and running Hardpy on a Raspberry Pi.  
It assumes a fresh installation of Raspberry Pi OS.
All the files for this guideline can be seen inside the hardpy package
[Raspberry](https://github.com/everypinio/hardpy/tree/main/examples/raspberry).

## Prerequisites

* A Raspberry Pi 4/5.
* A microSD card (at least 8GB recommended).
* A computer with internet access to download the Raspberry Pi OS image.
* A microSD card reader/writer.


## Installation Steps

1. **Install Raspberry Pi OS:**
    * Download the Raspberry Pi OS Imager from the official Raspberry Pi website: [https://www.raspberrypi.com/software/](https://www.raspberrypi.com/software/)
    * Choose the appropriate OS image (e.g., Raspberry Pi OS Lite or Raspberry Pi OS with Desktop).  
    Python on the selected OS must be at least 3.10.
    Lite is recommended for headless server setups.
    * Set up login/password, login/password for WiFi, enable SSH.
    * Flash the chosen image onto your microSD card using the Imager.
    * Insert the microSD card into your Raspberry Pi and boot it up. 
    Follow the on-screen instructions for initial setup (setting username, password, hostname, etc.).

2. **Connect to Raspberry Pi via SSH:**
* Find the IP address of your Raspberry Pi:
  - If you are on the same network, you can use tools like `nmap` or check your router's connected devices list.
  - Alternatively, use a network scanner app on your smartphone.
* Copy files for script before launching:
  ```bash
  scp /file/path/script.sh [login]@<RASPBERRY_PI_IP_ADDRESS>:/home/[login]/
  scp /file/path/local.ini [login]@<RASPBERRY_PI_IP_ADDRESS>:/home/[login]/
  scp /file/path/default.ini [login]@<RASPBERRY_PI_IP_ADDRESS>:/home/[login]/
  ```
* Open your SSH client and connect to the Raspberry Pi:
  ```bash
  ssh [login]@<RASPBERRY_PI_IP_ADDRESS>
  ```
* Once logged in, update the system:
  ```bash
  sudo apt update && sudo apt upgrade -y
  ```
* Make the script executable: `chmod +x /home/[login]/script.sh`


3. **Prepare the Installation Script without SSH:**

    * Create a directory for your Hardpy installation.
    * Inside this directory, create the `script.sh` file and paste the provided script content into it.
    * Create `local.ini` and `default.ini` files in the same directory, 
    also populated with the provided example configurations. 
    These configure CouchDB to bind to all interfaces (0.0.0.0), 
    and set the default username and password to `dev`/`dev`.  
    **Important:**  For production, change the default password!
    * Make the script executable: `chmod +x script.sh`

4. **Run the Installation Script:**

    * Open a terminal on your Raspberry Pi (either directly or via SSH).
    * Navigate to the directory containing the script.
    * Execute the script: `bash script.sh`
    * The script will install necessary dependencies (CouchDB, ufw), configure CouchDB, install Hardpy, and set up firewall rules.  
    During the CouchDB installation, you'll be prompted for a "Magic Cookie."  
    Enter any value (e.g., "1").  
    For other prompts, pressing Enter will accept the default values.
    * The script will ask if you want to reboot.  
    Choose "yes" to complete the installation.

5. **Initialize and Run Hardpy:**

    * After rebooting, log in to your Raspberry Pi.
    * Navigate to the directory where you want to create your Hardpy project.
    * Initialize Hardpy: `hardpy init --database-host raspberrypi --frontend-host 0.0.0.0 --socket-host 0.0.0.0 test` (replace `test` with your project name).  
    The `--database-host` is set to the hostname of your Raspberry Pi.  
    The other hosts are set to 0.0.0.0 to make the services accessible from any device on the network.
    * Change directory to the newly created project: `cd test`
    * Run Hardpy: `hardpy run`

## Accessing Hardpy

* **CouchDB:** Accessible from any device on the network at `raspberrypi:5984` (or `raspberrypi.local:5984` from some systems).
* **Hardpy Frontend:** Accessible from any device on the network at `raspberrypi:8000` (or `raspberrypi.local:8000` from some systems).

## Script Explanation (`script.sh`)

The script performs the following actions:

* **Updates package lists and installs dependencies:** Installs `curl`, `apt-transport-https`, `gnupg`, CouchDB, and ufw.
* **Configures CouchDB:** Creates a shared memory directory for CouchDB and copies the provided `default.ini` and `local.ini` configuration files.  
These files configure CouchDB to bind to all network interfaces and set the initial username and password (which should be changed for production).
* **Installs Hardpy:** Installs the Hardpy package using `pip3`. 
The `--break-system-packages` is included to bypass any potential conflicts.
* **Reboots the system:**  Reboots the Raspberry Pi to ensure all changes are applied.

## Changing the Raspberry Pi Hostname

You can change the hostname of your Raspberry Pi using the `raspi-config` utility: `sudo raspi-config`.  
This allows you to access it more easily on your local network using the new hostname (e.g., `raspberrypi.local`).

## Running a Database in RAM

To keep the database data in RAM and clear it on reboot:

1. Create a folder to store the database data in RAM and give it the necessary permissions:

```bash
sudo mkdir -p /dev/shm/couchdb && sudo chmod 777 /dev/shm/couchdb
```

2. Correct the `database_dir` parameter in the `opt/couchdb/etc/default.ini` file:

```ini
[couchdb]
database_dir = ./../../dev/shm/couchdb
```

3. Restart the database

