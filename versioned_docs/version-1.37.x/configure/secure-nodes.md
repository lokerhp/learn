---
title: "Secure your nodes"
description: "Your data and systems are safe with Netdata, but we recommend a few easy ways to improve the security of your infrastructure."
custom_edit_url: null
---



Upon installation, the Netdata Agent serves the **local dashboard** at port `19999`. If the node is accessible to the
internet at large, anyone can access the dashboard and your node's metrics at `http://NODE:19999`. We made this decision
so that the local dashboard was immediately accessible to users, and so that we don't dictate how professionals set up
and secure their infrastructures. 

Despite this design decision, your [data](/docs/agent/netdata-security#your-data-is-safe-with-netdata) and your
[systems](/docs/agent/netdata-security#your-systems-are-safe-with-netdata) are safe with Netdata. Netdata is read-only,
cannot do anything other than present metrics, and runs without special/`sudo` privileges. Also, the local dashboard
only exposes chart metadata and metric values, not raw data.

While Netdata is secure by design, we believe you should [protect your
nodes](/docs/agent/netdata-security#why-netdata-should-be-protected). If left accessible to the internet at large, the
local dashboard could reveal sensitive information about your infrastructure. For example, an attacker can view which
applications you run (databases, webservers, and so on), or see every user account on a node. 

Instead of dictating how to secure your infrastructure, we give you many options to establish security best practices
that align with your goals and your organization's standards.

-   [Disable the local dashboard](#disable-the-local-dashboard): **Simplest and recommended method** for those who have
    added nodes to Netdata Cloud and view dashboards and metrics there.
-   [Restrict access to the local dashboard](#restrict-access-to-the-local-dashboard): Allow local dashboard access from
    only certain IP addresses, such as a trusted static IP or connections from behind a management LAN. Full support for
    Netdata Cloud.
-   [Use a reverse proxy](#use-a-reverse-proxy): Password-protect a local dashboard and enable TLS to secure it. Full
    support for Netdata Cloud.

## Disable the local dashboard

This is the _recommended method for those who have connected their nodes to Netdata Cloud_ and prefer viewing real-time
metrics using the War Room Overview, Nodes view, and Cloud dashboards.

You can disable the local dashboard (and API) but retain the encrypted Agent-Cloud link ([ACLK](/docs/agent/aclk)) that
allows you to stream metrics on demand from your nodes via the Netdata Cloud interface. This change mitigates all
concerns about revealing metrics and system design to the internet at large, while keeping all the functionality you
need to view metrics and troubleshoot issues with Netdata Cloud.

Open `netdata.conf` with `./edit-config netdata.conf`. Scroll down to the `[web]` section, and find the `mode =
static-threaded` setting, and change it to `none`.

```conf
[web]
    mode = none
```

Save and close the editor, then [restart your Agent](/docs/configure/start-stop-restart) using `sudo systemctl
restart netdata`. If you try to visit the local dashboard to `http://NODE:19999` again, the connection will fail because
that node no longer serves its local dashboard.

> See the [configuration basics doc](/docs/configure/nodes) for details on how to find `netdata.conf` and use
> `edit-config`.

## Restrict access to the local dashboard

If you want to keep using the local dashboard, but don't want it exposed to the internet, you can restrict access with
[access lists](/docs/agent/web/server#access-lists). This method also fully retains the ability to stream metrics
on-demand through Netdata Cloud.

The `allow connections from` setting helps you allow only certain IP addresses or FQDN/hostnames, such as a trusted
static IP, only `localhost`, or connections from behind a management LAN. 

By default, this setting is `localhost *`. This setting allows connections from `localhost` in addition to _all_
connections, using the `*` wildcard. You can change this setting using Netdata's [simple
patterns](/docs/agent/libnetdata/simple_pattern).

```conf
[web]
    # Allow only localhost connections
    allow connections from = localhost

    # Allow only from management LAN running on `10.X.X.X`
    allow connections from = 10.*

    # Allow connections only from a specific FQDN/hostname
    allow connections from = example*
```

The `allow connections from` setting is global and restricts access to the dashboard, badges, streaming, API, and
`netdata.conf`, but you can also set each of those access lists more granularly if you choose:

```conf
[web]
    allow connections from = localhost *
    allow dashboard from = localhost *
    allow badges from = *
    allow streaming from = *
    allow netdata.conf from = localhost fd* 10.* 192.168.* 172.16.* 172.17.* 172.18.* 172.19.* 172.20.* 172.21.* 172.22.* 172.23.* 172.24.* 172.25.* 172.26.* 172.27.* 172.28.* 172.29.* 172.30.* 172.31.*
    allow management from = localhost
```

See the [web server](/docs/agent/web/server#access-lists) docs for additional details about access lists. You can take
access lists one step further by [enabling SSL](/docs/agent/web/server#enabling-tls-support) to encrypt data from local
dashboard in transit. The connection to Netdata Cloud is always secured with TLS.

## Use a reverse proxy

You can also put Netdata behind a reverse proxy for additional security while retaining the functionality of both the
local dashboard and Netdata Cloud dashboards. You can use a reverse proxy to password-protect the local dashboard and
enable HTTPS to encrypt metadata and metric values in transit.

We recommend Nginx, as it's what we use for our [demo server](https://london.my-netdata.io/), and we have a guide
dedicated to [running Netdata behind Nginx](/docs/agent/running-behind-nginx).

We also have guides for [Apache](/docs/agent/running-behind-apache), [Lighttpd](/docs/agent/running-behind-lighttpd),
[HAProxy](/docs/agent/running-behind-haproxy), and [Caddy](/docs/agent/running-behind-caddy).

## What's next?

Read about [Netdata's security design](/docs/agent/netdata-security) and our [blog
post](https://www.netdata.cloud/blog/netdata-agent-dashboard/) about why the local Agent dashboard is both open and
secure by design.

Next up, learn about [collectors](/docs/collect/how-collectors-work) to ensure you're gathering every essential
metric about your node, its applications, and your infrastructure at large.


