---
title: "HAProxy monitoring with Netdata"
custom_edit_url: null
sidebar_label: "HAProxy"
---



Monitors frontend and backend metrics such as bytes in, bytes out, sessions current, sessions in queue current.
And health metrics such as backend servers status (server check should be used).

Plugin can obtain data from URL or Unix socket.

Requirement:

- Socket must be readable and writable by the `netdata` user.
- URL must have `stats uri <path>` present in the haproxy config, otherwise you will get HTTP 503 in the haproxy logs.

It produces:

1. **Frontend** family charts

    - Kilobytes in/s
    - Kilobytes out/s
    - Sessions current
    - Sessions in queue current

2. **Backend** family charts

    - Kilobytes in/s
    - Kilobytes out/s
    - Sessions current
    - Sessions in queue current

3. **Health** chart

    - number of failed servers for every backend (in DOWN state)

## Configuration

Edit the `python.d/haproxy.conf` configuration file using `edit-config` from the Netdata [config
directory](/docs/configure/nodes), which is typically at `/etc/netdata`.

```bash
cd /etc/netdata   # Replace this path with your Netdata config directory, if different
sudo ./edit-config python.d/haproxy.conf
```

Sample:

```yaml
via_url:
  user: 'username' # ONLY IF stats auth is used
  pass: 'password' # # ONLY IF stats auth is used
  url: 'http://ip.address:port/url;csv;norefresh'
```

OR

```yaml
via_socket:
  socket: 'path/to/haproxy/sock'
```

If no configuration is given, module will fail to run.

---
