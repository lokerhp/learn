---
title: "SpigotMC monitoring with Netdata"
custom_edit_url: null
sidebar_label: "SpigotMC"
---



Performs basic monitoring for Spigot Minecraft servers.

It provides two charts, one tracking server-side ticks-per-second in
1, 5 and 15 minute averages, and one tracking the number of currently
active users.

This is not compatible with Spigot plugins which change the format of
the data returned by the `tps` or `list` console commands.

## Configuration

Edit the `python.d/spigotmc.conf` configuration file using `edit-config` from the Netdata [config
directory](/docs/configure/nodes), which is typically at `/etc/netdata`.

```bash
cd /etc/netdata   # Replace this path with your Netdata config directory, if different
sudo ./edit-config python.d/spigotmc.conf
```

```yaml
host: localhost
port: 25575
password: pass
```

By default, a connection to port 25575 on the local system is attempted with an empty password.

---


