# SMA-EM
SMA Energymeter measurement
sma-em-measurement.py: Python3 loop dieplay SMA Energymeter measurement values

sma-daemon.py: Python3 daemon writing regard and surplus values to /run/shm/em-[serial]-[value]

create a config file in /etc/smaemd/config
Example content


[SMA-EM]
# serials of sma-ems the daemon should take notice
# seperated by space
serials=123456 1900204522
# measurement values
values=pregard psurplus qsurplus ssurplus

[DAEMON]
pidfile=/run/smaemd.pid

