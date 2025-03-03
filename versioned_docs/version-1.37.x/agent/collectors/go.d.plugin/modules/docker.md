---
title: "Docker monitoring with Netdata"
description: "Monitor Docker containers health metrics and data usage metrics."
custom_edit_url: null
sidebar_label: "Docker"
---



[Docker Engine](https://docs.docker.com/engine/) is an open source containerization technology for building and
containerizing your applications.

This module monitors one or more Docker Engine instances, depending on your configuration.

## Metrics

All metrics have "docker." prefix.

| Metric               | Scope  |        Dimensions        |   Units    |
|----------------------|:------:|:------------------------:|:----------:|
| containers_state     | global | running, paused, stopped | containers |
| healthy_containers   | global |         healthy          | containers |
| unhealthy_containers | global |        unhealthy         | containers |
| images               | global |     active, dangling     |   images   |
| images_size          | global |           size           |     B      |

## Configuration

Edit the `go.d/docker.conf` configuration file using `edit-config` from the
Netdata [config directory](/docs/configure/nodes), which is typically at `/etc/netdata`.

```bash
cd /etc/netdata # Replace this path with your Netdata config directory
sudo ./edit-config go.d/docker.conf
```

```yaml
jobs:
  - name: local
    address: 'unix:///var/run/docker.sock'

  - name: remote
    address: 'tcp://203.0.113.10:2375'
```

For all available options see
module [configuration file](https://github.com/netdata/go.d.plugin/blob/master/config/go.d/docker.conf).

## Troubleshooting

To troubleshoot issues with the `docker` collector, run the `go.d.plugin` with the debug option enabled. The output
should give you clues as to why the collector isn't working.

First, navigate to your plugins' directory, usually at `/usr/libexec/netdata/plugins.d/`. If that's not the case on your
system, open `netdata.conf` and look for the setting `plugins directory`. Once you're in the plugin's directory, switch
to the `netdata` user.

```bash
cd /usr/libexec/netdata/plugins.d/
sudo -u netdata -s
```

You can now run the `go.d.plugin` to debug the collector:

```bash
./go.d.plugin -d -m docker
```
