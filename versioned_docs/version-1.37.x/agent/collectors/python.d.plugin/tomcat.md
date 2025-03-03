---
title: "Apache Tomcat monitoring with Netdata"
custom_edit_url: null
sidebar_label: "Tomcat"
---



Presents memory utilization of tomcat containers.

Charts:

1.  **Requests** per second

    -   accesses

2.  **Volume** in KB/s

    -   volume

3.  **Threads**

    -   current
    -   busy

4.  **JVM Free Memory** in MB

    -   jvm

## Configuration

Edit the `python.d/tomcat.conf` configuration file using `edit-config` from the Netdata [config
directory](/docs/configure/nodes), which is typically at `/etc/netdata`.

```bash
cd /etc/netdata   # Replace this path with your Netdata config directory, if different
sudo ./edit-config python.d/tomcat.conf
```

```yaml
localhost:
  name : 'local'
  url  : 'http://127.0.0.1:8080/manager/status?XML=true'
  user : 'tomcat_username'
  pass : 'secret_tomcat_password'
```

Without configuration, module attempts to connect to `http://localhost:8080/manager/status?XML=true`, without any credentials.
So it will probably fail.

---


