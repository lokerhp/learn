---
title: "APC UPS monitoring with Netdata"
custom_edit_url: null
sidebar_label: "APC UPS"
---



Monitors different APC UPS models and retrieves status information using `apcaccess` tool.

## Configuration

Edit the `charts.d/apcupsd.conf` configuration file using `edit-config` from the Netdata [config
directory](/docs/configure/nodes), which is typically at `/etc/netdata`.

```bash
cd /etc/netdata   # Replace this path with your Netdata config directory, if different
sudo ./edit-config charts.d/apcupsd.conf
```


