## ASA AAF5 focuser daemon

`aaf5_focusd` interfaces with and wraps an ASA AAF5 focuser and exposes it via Pyro.

`focus` is a commandline utility for controlling the focuser.

### Configuration

Configuration is read from json files that are installed by default to `/etc/focusd`.
A configuration file is specified when launching the server, and the `focus` frontend will search this location when launched.

The configuration options are:
```python
{
  "daemon": "halfmetre_focuser", # Run the server as this daemon. Daemon types are registered in `rockit.common.daemons`.
  "log_name": "focusd@halfmetre", # The name to use when writing messages to the observatory log.
  "control_machines": ["HalfMetreTCS"], # Machine names that are allowed to control (rather than just query) state. Machine names are registered in `rockit.common.IP`.
  "serial_port": "/dev/focuser", # Serial FIFO for communicating with the focuser
  "serial_baud": 38400, # Serial baud rate (always 38400)
  "serial_timeout": 5, # Serial comms timeout
  "nominal_focus_position": 3000, # Position to move to after homing
  "max_position": 70000, # Maximum allowable position
  "moving_loop_delay": 0.5, # Delay in seconds between focuser status polls when moving
  "move_timeout": 180, # Maximum time expected for a focus movement
}

```

## Initial Installation


The automated packaging scripts will push 4 RPM packages to the observatory package repository:

| Package                       | Description                                                                  |
|-------------------------------|------------------------------------------------------------------------------|
| rockit-focuser-aaf5-server    | Contains the `aaf5_focusd` server and systemd service file.                  |
| rockit-focuser-aaf5-client    | Contains the `focus` commandline utility for controlling the focuser server. |
| python3-rockit-focuser-aaf5   | Contains the python module with shared code.                                 |
| rockit-focuser-aaf5-data-h400 | Contains the json configuration for the H400 test telescope.                 |

After installing packages, the systemd service should be enabled:

```
sudo systemctl enable --now aaf5_focusd@<config>
```

where `config` is the name of the json file for the appropriate telescope.

Now open a port in the firewall:
```
sudo firewall-cmd --zone=public --add-port=<port>/tcp --permanent
sudo firewall-cmd --reload
```
where `port` is the port defined in `rockit.common.daemons` for the daemon specified in the config.

### Upgrading Installation

New RPM packages are automatically created and pushed to the package repository for each push to the `master` branch.
These can be upgraded locally using the standard system update procedure:
```
sudo yum clean expire-cache
sudo yum update
```

The daemon should then be restarted to use the newly installed code:
```
sudo systemctl restart aaf5_focusd@<config>
```

### Testing Locally

The camera server and client can be run directly from a git clone:
```
aaf5_focusd test.json
FOCUSD_CONFIG_PATH=./test.json ./focus status
```
