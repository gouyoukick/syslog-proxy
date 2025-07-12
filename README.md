Syslog Buffer Proxy – UDP to TCP Reliable Forwarder

This is a lightweight Python application designed as a buffer and forwarding proxy for BSD-style Syslog messages. It receives logs over UDP, updates their timestamps, and forwards them via TCP to a remote logging server with delivery guarantees.

Features
-Listens for Syslog messages on UDP port 6666
-Updates the timestamp of each message upon reception
-Forwards messages over TCP port 6666 to a remote server
-Stores messages locally if delivery fails, and retries automatically
-Deletes expired messages based on a configurable TTL

Configuration of remote server IP, TCP port, and retention duration via a config.txt file


Requirements
-Python 3.x
-rsyslog

Typical Use Case
Acts as a bridge between network equipment (such as Cisco or Netgear switches) that sends Syslog over UDP, and centralized logging platforms that require reliable TCP input (e.g., Graylog, ELK stack, Grafana Loki). Ensures message delivery and acts as a buffer in case of network or destination outages.
