---
title: "Enable an exporting connector"
description: "Learn how to enable and configure any connector using examples to start exporting metrics to external time-series databases in minutes."
custom_edit_url: null
---



Now that you found the right connector for your [external time-series
database](/docs/export/external-databases#supported-databases), you can now enable the exporting engine and the
connector itself. We'll walk through the process of enabling the exporting engine itself, followed by two examples using
the OpenTSDB and Graphite connectors.

> When you enable the exporting engine and a connector, the Netdata Agent exports metrics _beginning from the time you
> restart its process_, not the entire [database of long-term metrics](/docs/store/change-metrics-storage).

Once you understand the process of enabling a connector, you can translate that knowledge to any other connector.

## Enable the exporting engine

Use `edit-config` from your [Netdata config directory](/docs/configure/nodes#the-netdata-config-directory) to open
`exporting.conf`:

```bash
sudo ./edit-config exporting.conf
```

Enable the exporting engine itself by setting `enabled` to `yes`:

```conf
[exporting:global]
    enabled = yes
```

Save the file but keep it open, as you will edit it again to enable specific connectors.

## Example: Enable the OpenTSDB connector

Use the following configuration as a starting point. Copy and paste it into `exporting.conf`.

```conf
[opentsdb:http:my_opentsdb_http_instance]
    enabled = yes
    destination = localhost:4242
```

Replace `my_opentsdb_http_instance` with an instance name of your choice, and change the `destination` setting to the IP
address or hostname of your OpenTSDB database.

Restart your Agent with `sudo systemctl restart netdata`, or the [appropriate
method](/docs/configure/start-stop-restart) for your system, to begin exporting to your OpenTSDB database. The
Netdata Agent exports metrics _beginning from the time the process starts_, and because it exports as metrics are
collected, you should start seeing data in your external database after only a few seconds.

Any further configuration is optional, based on your needs and the configuration of your OpenTSDB database. See the
[OpenTSDB connector doc](/docs/agent/exporting/opentsdb) and [exporting engine
reference](/docs/agent/exporting#configuration) for details.

## Example: Enable the Graphite connector

Use the following configuration as a starting point. Copy and paste it into `exporting.conf`.

```conf
[graphite:my_graphite_instance]
    enabled = yes
    destination = 203.0.113.0:2003
```

Replace `my_graphite_instance` with an instance name of your choice, and change the `destination` setting to the IP
address or hostname of your Graphite-supported database.

Restart your Agent with `sudo systemctl restart netdata`, or the [appropriate
method](/docs/configure/start-stop-restart) for your system, to begin exporting to your Graphite-supported database.
Because the Agent exports metrics as they're collected, you should start seeing data in your external database after
only a few seconds.

Any further configuration is optional, based on your needs and the configuration of your Graphite-supported database.
See [exporting engine reference](/docs/agent/exporting#configuration) for details.

## What's next?

If you want to further configure your exporting connectors, see the [exporting engine
reference](/docs/agent/exporting#configuration).

For a comprehensive example of using the Graphite connector, read our guide: [_Export and visualize Netdata metrics in
Graphite_](/guides/export/export-netdata-metrics-graphite). Or, start [using host
labels](/guides/using-host-labels) on exported metrics.

### Related reference documentation

-   [Exporting engine reference](/docs/agent/exporting)
-   [OpenTSDB connector](/docs/agent/exporting/opentsdb)
-   [Graphite connector](/docs/agent/exporting/graphite)


