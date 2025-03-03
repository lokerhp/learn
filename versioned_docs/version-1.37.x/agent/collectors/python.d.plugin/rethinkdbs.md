---
title: "RethinkDB monitoring with Netdata"
custom_edit_url: null
sidebar_label: "RethinkDB"
---



Collects database server and cluster statistics.

Following charts are drawn:

1.  **Connected Servers**

    -   connected
    -   missing

2.  **Active Clients**

    -   active

3.  **Queries** per second

    -   queries

4.  **Documents** per second

    -   documents

## Configuration

Edit the `python.d/rethinkdbs.conf` configuration file using `edit-config` from the Netdata [config
directory](/docs/configure/nodes), which is typically at `/etc/netdata`.

```bash
cd /etc/netdata   # Replace this path with your Netdata config directory, if different
sudo ./edit-config python.d/rethinkdbs.conf
```

```yaml
localhost:
  name     : 'local'
  host     : '127.0.0.1'
  port     : 28015
  user     : "user"
  password : "pass"
```

When no configuration file is found, module tries to connect to `127.0.0.1:28015`.

---


