---
title: "Collect application metrics with Netdata"
sidebar_label: "Application metrics"
description: "Monitor and troubleshoot every application on your infrastructure with per-second metrics, zero configuration, and meaningful charts."
custom_edit_url: null
---



Netdata instantly collects per-second metrics from many different types of applications running on your systems, such as
web servers, databases, message brokers, email servers, search platforms, and much more. Metrics collectors are
pre-installed with every Netdata Agent and usually require zero configuration. Netdata also collects and visualizes
resource utilization per application on Linux systems using `apps.plugin`.

[**apps.plugin**](/docs/agent/collectors/apps.plugin) looks at the Linux process tree every second, much like `top` or
`ps fax`, and collects resource utilization information on every running process. By reading the process tree, Netdata
shows CPU, disk, networking, processes, and eBPF for every application or Linux user. Unlike `top` or `ps fax`, Netdata
adds a layer of meaningful visualization on top of the process tree metrics, such as grouping applications into useful
dimensions, and then creates per-application charts under the **Applications** section of a Netdata dashboard, per-user
charts under **Users**, and per-user group charts under **User Groups**.

Our most popular application collectors:

- [Prometheus endpoints](/docs/agent/collectors/go.d.plugin/modules/prometheus): Gathers
  metrics from one or more Prometheus endpoints that use the OpenMetrics exposition format. Auto-detects more than 600
  endpoints.
- [Web server logs (Apache, NGINX)](/docs/agent/collectors/go.d.plugin/modules/weblog/):
  Tail access logs and provide very detailed web server performance statistics. This module is able to parse 200k+
  rows in less than half a second.
- [MySQL](/docs/agent/collectors/go.d.plugin/modules/mysql/): Collect database global,
  replication, and per-user statistics.
- [Redis](/docs/agent/collectors/go.d.plugin/modules/redis): Monitor database status by
  reading the server's response to the `INFO` command.
- [Apache](/docs/agent/collectors/go.d.plugin/modules/apache/): Collect Apache web server
  performance metrics via the `server-status?auto` endpoint.
- [Nginx](/docs/agent/collectors/go.d.plugin/modules/nginx/): Monitor web server status
  information by gathering metrics via `ngx_http_stub_status_module`.
- [Postgres](/docs/agent/collectors/go.d.plugin/modules/postgres): Collect database health
  and performance metrics.
- [ElasticSearch](/docs/agent/collectors/go.d.plugin/modules/elasticsearch): Collect search
  engine performance and health statistics. Optionally collects per-index metrics.
- [PHP-FPM](/docs/agent/collectors/go.d.plugin/modules/phpfpm/): Collect application summary
  and processes health metrics by scraping the status page (`/status?full`).

Our [supported collectors list](/docs/agent/collectors/collectors#service-and-application-collectors) shows all Netdata's
application metrics collectors, including those for containers/k8s clusters.

## Collect metrics from applications running on Windows

Netdata is fully capable of collecting and visualizing metrics from applications running on Windows systems. The only
caveat is that you must [install Netdata](/docs/get-started) on a separate system or a compatible VM because there
is no native Windows version of the Netdata Agent.

Once you have Netdata running on that separate system, you can follow the [enable and configure
doc](/docs/collect/enable-configure) to tell the collector to look for exposed metrics on the Windows system's IP
address or hostname, plus the applicable port.

For example, you have a MySQL database with a root password of `my-secret-pw` running on a Windows system with the IP
address 203.0.113.0. you can configure the [MySQL
collector](/docs/agent/collectors/go.d.plugin/modules/mysql) to look at `203.0.113.0:3306`:

```yml
jobs:
  - name: local
    dsn: root:my-secret-pw@tcp(203.0.113.0:3306)/
```

This same logic applies to any application in our [supported collectors
list](/docs/agent/collectors/collectors#service-and-application-collectors) that can run on Windows.

## What's next?

If you haven't yet seen the [supported collectors list](/docs/agent/collectors/collectors) give it a once-over for any
additional applications you may want to monitor using Netdata's native collectors, or the [generic Prometheus
collector](/docs/agent/collectors/go.d.plugin/modules/prometheus).

Collecting all the available metrics on your nodes, and across your entire infrastructure, is just one piece of the
puzzle. Next, learn more about Netdata's famous real-time visualizations by [seeing an overview of your
infrastructure](/docs/visualize/overview-infrastructure) using Netdata Cloud.


