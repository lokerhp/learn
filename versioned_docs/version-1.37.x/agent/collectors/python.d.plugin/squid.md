---
title: "Squid monitoring with Netdata"
custom_edit_url: null
sidebar_label: "Squid"
---



Monitors one or more squid instances depending on configuration.

It produces following charts:

1.  **Client Bandwidth** in kilobits/s

    -   in
    -   out
    -   hits

2.  **Client Requests** in requests/s

    -   requests
    -   hits
    -   errors

3.  **Server Bandwidth** in kilobits/s

    -   in
    -   out

4.  **Server Requests** in requests/s

    -   requests
    -   errors

## Configuration

Edit the `python.d/squid.conf` configuration file using `edit-config` from the Netdata [config
directory](/docs/configure/nodes), which is typically at `/etc/netdata`.

```bash
cd /etc/netdata   # Replace this path with your Netdata config directory, if different
sudo ./edit-config python.d/squid.conf
```

```yaml
priority     : 50000

local:
  request : 'cache_object://localhost:3128/counters'
  host    : 'localhost'
  port    : 3128
```

Without any configuration module will try to autodetect where squid presents its `counters` data

---


