# syslog-proxy
a ubuntu app to convert and manage local syslog before sending

in a network, a ubuntu server receive syslog with rsyslog and write them on a buffer file. This script in pyhton will read the buffer file to try to manage the buffer and send syslog message to a syslog server in TCP.
A config .txt file let you manage some settings like server IP, port, time before erase syslog
