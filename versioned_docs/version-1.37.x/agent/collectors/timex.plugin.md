---
title: "timex.plugin"
description: "Monitor the system clock synchronization state."
custom_edit_url: null
---



This plugin monitors the system kernel clock synchronization state.

This plugin creates the following charts:

- System clock synchronization state according to the system kernel
- System clock status which gives the value of the `time_status` variable in the kernel
- Computed time offset between local system and reference clock

This is obtained from the information provided by the [ntp_adjtime()](https://man7.org/linux/man-pages/man2/adjtimex.2.html) system call.
An unsynchronized clock may indicate a hardware clock error, or an issue with UTC synchronization.

## Configuration

Edit the `netdata.conf` configuration file using [`edit-config`](/docs/configure/nodes#use-edit-config-to-edit-configuration-files) from the [Netdata config directory](/docs/configure/nodes#the-netdata-config-directory), which is typically at `/etc/netdata`.

Scroll down to the `[plugin:timex]` section to find the available options:

```ini
[plugin:timex]
    # update every = 1
    # clock synchronization state = yes
    # time offset = yes
```
