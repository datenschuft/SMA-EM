# SMA-EM

a detailed german description could be found here
https://www.unifox.at/software/sma-em-daemon/

translated by google 
https://translate.google.com/translate?sl=de&tl=en&u=https://www.unifox.at/software/sma-em-daemon/


## SMA Energymeter / Homemanager measurement
sma-em-measurement.py: Python3 loop display SMA Energymeter measurement values

sma-daemon.py: Python3 daemon writing consume and supply values to /run/shm/em-[serial]-[value]

```
# HINT #
Sma homemanager version 2.3.4R added 8 Byte of measurement data.
This version trys to detect the measurement values on obis ids, so it should be save if new values were added or removed.
```

## Requirements
python3
sys
time
configparser (SafeConfigParser)
signal

```
apt install python3-pip
```
Feature pvdata reqires pymodbus
```
sudo pip install pymodbus
```
or
```
sudo pip3 install pymodbus
```

## Configuration
create a config file in /etc/smaemd/config<br>
Use UTF-8 encoded configfile<br>
Example:
```
[SMA-EM]
# serials of sma-ems the daemon should take notice
# seperated by space
serials=30028xxxxx
# features could filter serials to, but wouldn't see serials if these serials was not defines in SMA-EM serials
# list of features to load/run
features=simplefswriter sample

[DAEMON]
pidfile=/run/smaemd.pid
# listen on an interface with the given ip
# use 0.0.0.0 for any interface
ipbind=192.168.8.15
# multicast ip and port of sma-datagrams
# defaults
mcastgrp=239.12.255.254
mcastport=9522

# each feature/plugin has its own section
# called FEATURE-[featurename]
# the feature section is required if a feature is listed in [SMA-EM]features

[FEATURE-simplefswriter]
# list serials simplefswriter notice
serials=1900204522
# measurement vars simplefswriter should write to filesystem (only from smas with serial in serials)
values=pconsume psupply qsupply ssupply

[FEATURE-sample]
nothing=here

```

## Routing
maybe you have to add a route (example: on hosts with more than one interface) <br>
```
sudo ip route add 224.0.0.0/4 dev interfacename
```

## Install / Copy (tested on Raspbian 9.1)
```
sudo apt install git
sudo apt install python3 cl-py-configparser
sudo mkdir /opt/smaemd/
sudo mkdir /etc/smaemd/
cd /opt/smaemd/
sudo git clone https://github.com/datenschuft/SMA-EM.git .
sudo cp systemd-settings /etc/systemd/system/smaemd.service
```

Create a /etc/smaemd/config file
```
sudo cp /opt/smaemd/config.sample /etc/smaemd/config
```
Edit the /etc/smaemd/config file and customize it to suit your needs (e.g. set SMA energy meter serial number, IP address, enable features)
```
sudo nano /etc/smaemd/config
```

Update systemd
```
sudo systemctl daemon-reload
sudo systemctl enable smaemd.service
sudo systemctl start smaemd.service
```
feel lucky and read /run/shm/em-<serial>-<value>



## Testing
sma-em-capture-package - trys to capture a SMA-EM or SMA-homemanager Datagram and display hex and ascii package-info and all recogniced measurement values.
Cloud be helpful on package/software changes.

## Docker

SMA-EM can be run as a dockerized application, which is very useful if you're unable to use the sma homeassistant add-on, but still want this functionality without polluting your host operating system with bespoke python modules, git repos etc.

The simplest way to build and run SMA-EM in docker is to use docker-compose, like so:

```shell
docker-compose up -d
```

Attention: This requires a working configuration file at `./smaemd/config` - this can of course be changed in `docker-compose.yml`.

If you want to be more manual about this, build the SMA-EM docker container yourself:

```shell
docker build -t sma-em .
```

To run, a minimal command line looks like this:

```shell
docker run --network=host -v ./smaemd:/etc/smaemd sma-em
```
