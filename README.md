# sys-stats

An open-source Python library to provide system stats over a web interface

![Python](https://img.shields.io/badge/Python-3.8%2B-blue.svg)

## Table of Contents

- [Introduction](#introduction)
- [Features](#features)
- [Installation](#installation)
- [Development](#development)
- [License](#license)

### Introduction

This Python package allows you to monitor various system statistics through a simple web interface. Whether you're a
developer, a sysadmin, or just curious about how your system is performing, this package makes it easy to access and
visualize system metrics.

### Why System Stats Web Interface?

One would definitely question -- "why develop another monitoring tool?"
Well, there are quite a few tools that I have tried but they either needed some effort to setup or lacked one or more
features.

While there are numerous monitoring tools available for different purposes, I needed a solution that was very simple. A
tool that's easy to
install, involves almost no effort to set up, and offers a simple and clean web UI for visualizing essential system
metrics.

PS: I'd appreciate if someone can point me to some good tools that suit the above stated goal! I'd be happy
to take a look at it.

The development of that thought, resulted in a tool that is:

- **Easy To Install:** Install the package using pip and get started with just a few commands.
- **Has a Web Interface:** Access system statistics through a simple, clean and user-friendly web interface.
- **Has Real-Time Monitoring:** Monitor CPU usage, memory usage, disk space, and more in real time.
- **Has Cross-Platform support:** Compatible with various operating systems, including macOS, and Linux.

### Where can I run this?

While it can be run practically on any *nix systems, it's best suited for running on systems that run headless (server/non-windowed mode) or remotely which need monitoring over the web.
For example:
- you can set it up on docker containers which need to be monitored remotely.
- if you have multiple on-prem servers in a private network that need monitoring at individual host level, you can host this tool on each server and access it over web interface.

  The possibilities are endless. The tool will evolve over time to get better.

### Features

- List running processes
- Show hardware metrics - CPU/Memory usage, etc
- Port bindings [WIP]

### Installation

To install the package, use the following pip command:

```bash
pip install sys-stats
```

Then run,

```bash
sysstats start
```

The process starts up with the following logs:

```shell
INFO:root:Starting web server on 0.0.0.0:8070
INFO:root:HTTP gateway timeout is set to 180 seconds.
INFO:root:API Docs at: http://0.0.0.0:8070/docs
INFO:root:ReDoc at: http://0.0.0.0:8070/redoc
INFO:     Started server process [3388]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://0.0.0.0:8070 (Press CTRL+C to quit)
```

Now, access the web interface at http://localhost:8070

To specify a different port, run:

```bash
sysstats start --port 8055
```

### Screenshots
![](https://raw.githubusercontent.com/amithkoujalgi/sys-stats/54bcf6dd8a5513c5d8982c3cdff3d724e6c8f740/images/processes.png)
![](https://raw.githubusercontent.com/amithkoujalgi/sys-stats/54bcf6dd8a5513c5d8982c3cdff3d724e6c8f740/images/resources.png)

### Development

#### Building from source

Run:

```bash
bash build.sh
```

#### Get Involved

I welcome contributions!
Whether it's reporting a bug, proposing an enhancement, or helping with code, please refer to the contribution
guidelines to get started.

### License

The project is released under the MIT License. For more details, consult the LICENSE file.


