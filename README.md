# Syslog Buffer Proxy – UDP to TCP Reliable Forwarder

This project implements a lightweight and reliable Syslog proxy, designed to receive logs over UDP from network devices (e.g., Cisco, Netgear) and forward them over TCP to a remote log server. The system ensures message delivery by buffering unsent logs and retrying transmission until successful or expired.

## Overview

The proxy is deployed on a dedicated Ubuntu server equipped with two network interfaces:
- One interface receives Syslog messages from network equipment (UDP)
- The other forwards logs to a remote logging server (TCP)

The system uses:
- **rsyslog** to collect and buffer messages
- A **custom Python script** to manage delivery, retry, and TTL-based deletion

## Features

- Listens for incoming Syslog messages on UDP port 6666
- Cleans and re-timestamps messages at reception
- Buffers messages to a local file for durability
- Forwards messages to a remote server using TCP port 6666
- Automatically deletes expired or successfully transmitted messages
- Runs periodically via `cron`
- Fully configurable via `syslog-relay-config.txt`

## Architecture
[Network Devices]
↓ UDP:6666
[Syslog Proxy Server]
↳ rsyslog → buffer-relay.log
↳ Python script → TCP:6666
↓
[Remote Syslog Collector]


## Configuration

Edit the `syslog-relay-config.txt` file to define:
- The IP address of the remote Syslog server
- TCP port to use for delivery
- Message retention period (in seconds)

Example:
SERVER_IP=192.168.1.100
SERVER_PORT=6666
MESSAGE_TTL=3600


## Installation and Setup

All installation and configuration steps are documented in the following file:

➡️ **[proxy_syslog_setup.doc](docs/proxy_syslog_setup.doc)**

Please refer to it for:
- rsyslog installation and configuration
- File and folder setup with permissions
- TFTP transfer instructions (optional)
- Python script integration
- Scheduling with cron
- NTP synchronization (chrony)

## Usage

To manually run the forwarding process:

sudo python3 /opt/syslog-relay/syslog-relay.py

To monitor the incoming log buffer:

tail -f /opt/syslog-relay/buffer-relay.log

License
MIT License

Author
Julien Gaulier
Gravity Media – Audio Broadcast & DevOps
julien.gaulier@gravitymedia.com

