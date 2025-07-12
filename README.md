Syslog Buffer Proxy – UDP to TCP Reliable Forwarder

This is a lightweight Python application designed as a buffer and forwarding proxy for BSD-style Syslog messages. It receives logs over UDP, updates their timestamps, and forwards them via TCP to a remote logging server with delivery guarantees.

Features
Listens for Syslog messages on UDP port 6666

Updates the timestamp of each message upon reception

Forwards messages over TCP port 6666 to a remote server

Stores messages locally if delivery fails, and retries automatically

Deletes expired messages based on a configurable TTL

Configuration of remote server IP, TCP port, and retention duration via a config.txt file

Configuration
Sample config.txt:

SERVER_IP=192.168.1.100
SERVER_PORT=6666
MESSAGE_TTL=3600
SERVER_IP: IP address of the remote Syslog server

SERVER_PORT: TCP port on the remote server

MESSAGE_TTL: maximum time in seconds to keep undelivered messages before deletion


Requirements
Python 3.x
rsyslog (only if you need to forward local system logs to the proxy)

Typical Use Case
Acts as a bridge between network equipment (such as Cisco or Netgear switches) that sends Syslog over UDP, and centralized logging platforms that require reliable TCP input (e.g., Graylog, ELK stack, Grafana Loki). Ensures message delivery and acts as a buffer in case of network or destination outages.
