# SMA-EM

## SMA Energymeter measurement
sma-em-measurement.py: Python3 loop display SMA Energymeter measurement values

sma-daemon.py: Python3 daemon writing regard and surplus values to /run/shm/em-[serial]-[value]

## Requirements
python3
sys
time
configparser (SafeConfigParser)
signal


## Configuration
create a config file in /etc/smaemd/config<br>
Use UTF-8 encoded configfile<br>
Example:
```
[SMA-EM]
# serials of sma-ems the daemon should take notice
# seperated by space
serials=123456 1900204522
# measurement values
values=pregard psurplus qsurplus ssurplus

[DAEMON]
pidfile=/run/smaemd.pid
# listen on an interface with the given ip
# use 0.0.0.0 for any interface
ipbind=192.168.8.15
# multicast ip and port of sma-datagrams
# defaults
mcastgrp=239.12.255.254
mcastport=9522

```

## Routing
maybe you have to add a route (example: on hosts with more than one interface) <br>
```
sudo ip route add 224.0.0.0/4 dev interfacename
```

## Install / Copy (tested on Raspbian 9.1)
```
apt install git
apt install python3 cl-py-configparser
mkdir /opt/smaemd/
mkdir /etc/smaemd/
cd /opt/smaemd/
git clone https://github.com/datenschuft/SMA-EM.git .
cp systemd-settings /etc/systemd/system/smaemd.service
```
create a /etc/smaemd/config - file (see example above)<br>
update systemd
```
systemctl daemon-reload
systemctl enable smaemd.service
systemctl start smaemd.service
```
feel lucky and read /run/shm/em-<serial>-<value>
