---
title: "CEPH monitoring with Netdata"
custom_edit_url: null
sidebar_label: "CEPH"
---



Monitors the ceph cluster usage and consumption data of a server, and produces:

-   Cluster statistics (usage, available, latency, objects, read/write rate)
-   OSD usage
-   OSD latency
-   Pool usage
-   Pool read/write operations
-   Pool read/write rate
-   number of objects per pool

## Requirements

-   `rados` python module
-   Granting read permissions to ceph group from keyring file

```shell
# chmod 640 /etc/ceph/ceph.client.admin.keyring
```

## Configuration

Edit the `python.d/ceph.conf` configuration file using `edit-config` from the Netdata [config
directory](/docs/configure/nodes), which is typically at `/etc/netdata`.

```bash
cd /etc/netdata   # Replace this path with your Netdata config directory, if different
sudo ./edit-config python.d/ceph.conf
```

Sample:

```yaml
local:
  config_file: '/etc/ceph/ceph.conf'
  keyring_file: '/etc/ceph/ceph.client.admin.keyring'
```

---


