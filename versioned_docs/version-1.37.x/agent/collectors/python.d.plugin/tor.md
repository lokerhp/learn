---
title: "Tor monitoring with Netdata"
custom_edit_url: null
sidebar_label: "Tor"
---



Connects to the Tor control port to collect traffic statistics.

## Requirements

-   `tor` program
-   `stem` python package

It produces only one chart:

1.  **Traffic**

    -   read
    -   write

## Configuration

Edit the `python.d/tor.conf` configuration file using `edit-config` from the Netdata [config
directory](/docs/configure/nodes), which is typically at `/etc/netdata`.

```bash
cd /etc/netdata   # Replace this path with your Netdata config directory, if different
sudo ./edit-config python.d/tor.conf
```

Needs only `control_port`.

Here is an example for local server:

```yaml
update_every : 1
priority     : 60000

local_tcp:
 name: 'local'
 control_port: 9051
 password: <password> # if required

local_socket:
 name: 'local'
 control_port: '/var/run/tor/control'
 password: <password> # if required
```

### prerequisite

Add to `/etc/tor/torrc`:

```
ControlPort 9051
```

For more options please read the manual.

Without configuration, module attempts to connect to `127.0.0.1:9051`.

---


