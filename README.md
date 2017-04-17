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
Example
```
[SMA-EM]
# serials of sma-ems the daemon should take notice
# seperated by space
serials=123456 1900204522
# measurement values
values=pregard psurplus qsurplus ssurplus

[DAEMON]
pidfile=/run/smaemd.pid
```

## Routing
maybe you have to add a route (example: on hosts with more than one interface) <br>
```
sudo ip route add 224.0.0.0/4 dev interfacename
```

## Install / Copy
```
apt install python3 cl-py-configparser
mkdir /opt/smaem/
mkdir /etc/smaemd/
cp daemon3x.py sma-daemon.py  smaem.py /opt/smaem/
cp systemd-settings /etc/systemd/system/smaemd.service
```
create a /etc/smaemd/config - file <br>
update systemd
```
systemctl daemon-reload
systemctl enable smaemd.service
systemctl start smaemd.service
```
feel lucky
