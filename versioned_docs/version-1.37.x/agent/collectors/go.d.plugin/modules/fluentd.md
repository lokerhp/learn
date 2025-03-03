---
title: "Fluentd monitoring with Netdata"
description: "Monitor the health and performance of Fluentd servers with zero configuration, per-second metric granularity, and interactive visualizations."
custom_edit_url: null
sidebar_label: "Fluentd"
---



[`Fluentd`](https://www.fluentd.org/) is an open source data collector for unified logging layer.

This module will monitor one or more `Fluentd` servers, depending on your configuration. It gathers metrics from plugin
endpoint provided by [in_monitor plugin](https://docs.fluentd.org/v1.0/articles/monitoring-rest-api).

## Requirements

- `fluentd` with enabled monitoring agent

## Metrics

All metrics have "fluentd." prefix.

| Metric                   | Scope  |          Dimensions           |    Units     |
|--------------------------|:------:|:-----------------------------:|:------------:|
| retry_count              | global | <i>a dimension per plugin</i> |    count     |
| buffer_queue_length      | global | <i>a dimension per plugin</i> | queue_length |
| buffer_total_queued_size | global | <i>a dimension per plugin</i> | queued_size  |

## Configuration

Edit the `go.d/fluentd.conf` configuration file using `edit-config` from the
Netdata [config directory](/docs/configure/nodes), which is typically at `/etc/netdata`.

```bash
cd /etc/netdata # Replace this path with your Netdata config directory
sudo ./edit-config go.d/fluentd.conf
```

Needs only `url`. Here is an example for 2 servers:

```yaml
jobs:
  - name: local
    url: http://127.0.0.1:24220

  - name: local_with_filtering
    url: http://127.0.0.1:24220
    permit_plugin_id: '!monitor_agent !dummy *'

  - name: remote
    url: http://203.0.113.10:24220
```

By default this module collects statistics for all plugins. Filter plugins
syntax: [simple patterns](https://docs.netdata.cloud/libnetdata/simple_pattern/).

For all available options please see
module [configuration file](https://github.com/netdata/go.d.plugin/blob/master/config/go.d/fluentd.conf).

## Troubleshooting

To troubleshoot issues with the `fluentd` collector, run the `go.d.plugin` with the debug option enabled. The output
should give you clues as to why the collector isn't working.

- Navigate to the `plugins.d` directory, usually at `/usr/libexec/netdata/plugins.d/`. If that's not the case on
  your system, open `netdata.conf` and look for the `plugins` setting under `[directories]`.

  ```bash
  cd /usr/libexec/netdata/plugins.d/
  ```

- Switch to the `netdata` user.

  ```bash
  sudo -u netdata -s
  ```

- Run the `go.d.plugin` to debug the collector:

  ```bash
  ./go.d.plugin -d -m fluentd
  ```

